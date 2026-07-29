import os
import re
import edge_tts

VOICE_LEO = "pt-BR-AntonioNeural"
VOICE_SARA = "pt-BR-FranciscaNeural"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "episodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Gera um buffer curto de silêncio de ~350ms em quadros MP3 silenciosos
SILENCE_MP3_CHUNK = b'\xff\xfb\x90\xc4\x00\x00\x00\x00\x00\x00\x00\x00' * 12

def clean_text_for_speech(text: str) -> str:
    clean = re.sub(r'```[\s\S]*?```', '', text)
    clean = re.sub(r'https?://\S+', '', clean)
    clean = re.sub(r'\((Risos|Pensativo|Pausa)\)', '...', clean, flags=re.IGNORECASE)
    clean = re.sub(r'\([^\)]+\)', '', clean)
    clean = re.sub(r'\[\d{1,2}:\d{2}\]', '', clean)
    clean = re.sub(r'<[^>]+>', '', clean)
    clean = re.sub(r'[\*\`\_]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def strip_id3(data: bytes) -> bytes:
    """
    Remove cabeçalhos ID3v2 do áudio sintetizado para evitar estalos ou metadata corrompida.
    """
    while data.startswith(b'ID3') and len(data) >= 10:
        size_bytes = data[6:10]
        tag_size = (
            (size_bytes[0] & 0x7F) << 21 |
            (size_bytes[1] & 0x7F) << 14 |
            (size_bytes[2] & 0x7F) << 7 |
            (size_bytes[3] & 0x7F)
        )
        total_id3_len = 10 + tag_size
        data = data[total_id3_len:]
        
    for i in range(min(len(data) - 1, 512)):
        if data[i] == 0xFF and (data[i+1] & 0xE0) == 0xE0:
            return data[i:]
            
    return data

async def synthesize_speech(text: str, voice: str) -> bytes:
    clean_text = clean_text_for_speech(text)
    if not clean_text:
        return b""
    
    # Parâmetros de modulação de voz diferenciada
    rate = "+2%" if voice == VOICE_LEO else "+0%"
    pitch = "+1Hz" if voice == VOICE_LEO else "-1Hz"
    
    communicate = edge_tts.Communicate(clean_text, voice, rate=rate, pitch=pitch)
    audio_bytes = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            raw_chunk = strip_id3(chunk["data"])
            audio_bytes.extend(raw_chunk)
                
    return strip_id3(bytes(audio_bytes))

def parse_sections(script_text: str):
    lines = script_text.strip().split("\n")
    sections = []
    current_title = "Intro"
    current_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        speaker_match = re.match(r'^(?:\*\*|\*)?\s*(Léo|Leo|Sara)\s*(?:\*\*|\*)?\s*:\s*(.*)', line, re.IGNORECASE)
        if speaker_match:
            raw_speaker = speaker_match.group(1).lower()
            speaker = "Léo" if ("léo" in raw_speaker or "leo" in raw_speaker) else "Sara"
            text = speaker_match.group(2).strip()
            if text:
                current_lines.append((speaker, text))
        elif line.startswith("[") and "]" in line:
            if current_lines:
                sections.append((current_title, current_lines))
                current_lines = []
            title_part = line.split("]", 1)[1].strip()
            current_title = title_part if title_part else "Bloco"
            
    if current_lines:
        sections.append((current_title, current_lines))
        
    return sections

def format_time(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def format_duration_hhmmss(seconds: float) -> str:
    hours = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

async def generate_audio_for_episode(ep):
    ep_id = ep["id"]
    filename = f"ep{ep_id:02d}_podcastti.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    print(f"\n[+] Sintetizando vozes neurais com pausas naturais para o Episódio {ep_id}: {ep['title']}...")
    
    sections = parse_sections(ep["script"])
    full_audio = bytearray()
    
    current_time_seconds = 0.0
    dynamic_chapters = []
    BYTES_PER_SECOND = 16000.0
    
    for idx, (section_title, dialogues) in enumerate(sections, 1):
        timestamp_str = format_time(current_time_seconds)
        clean_title = re.sub(r'^(INTRODUÇÃO|BLOCO \d+:|ENCERRAMENTO E DICAS)\s*', '', section_title, flags=re.IGNORECASE).strip()
        if not clean_title:
            clean_title = section_title
        
        dynamic_chapters.append((timestamp_str, clean_title))
        section_bytes = 0
        
        print(f"  - Marcador [{timestamp_str}] Cap {idx:02d}: {clean_title}")
        for speaker, text in dialogues:
            voice = VOICE_LEO if speaker == "Léo" else VOICE_SARA
            chunk_audio = await synthesize_speech(text, voice)
            if chunk_audio:
                full_audio.extend(chunk_audio)
                full_audio.extend(SILENCE_MP3_CHUNK) # Pausa natural entre turnos de fala
                section_bytes += len(chunk_audio) + len(SILENCE_MP3_CHUNK)
            
        current_time_seconds += (section_bytes / BYTES_PER_SECOND)
        
    with open(filepath, "wb") as f:
        f.write(full_audio)
        
    file_size = len(full_audio)
    total_seconds = file_size / BYTES_PER_SECOND
    duration_str = format_duration_hhmmss(total_seconds)
    
    print(f"[OK] Áudio gerado com sucesso: {filepath} ({file_size} bytes, Duração estimada: {duration_str})")
    
    ep["audio_url"] = f"https://rapha-dias.github.io/PodCastTI/episodes/{filename}"
    ep["audio_bytes"] = file_size
    ep["duration"] = duration_str
    ep["local_audio_path"] = filepath
    ep["chapters"] = dynamic_chapters
    
    # Atualiza as show notes do episódio
    show_notes = f"🎙️ SOBRE ESTE EPISÓDIO:\n{ep['summary']}\n\n⏱️ CAPÍTULOS E MARCAS DE TEMPO:\n"
    for idx, (time_mark, ch_title) in enumerate(dynamic_chapters, 1):
        show_notes += f"• {time_mark} - Cap {idx:02d}: {ch_title}\n"
        
    if "sources" in ep and ep["sources"]:
        show_notes += "\n🔗 FONTES CITADAS E LINKS RECOMENDADOS:\n"
        for src in ep["sources"]:
            if isinstance(src, (list, tuple)) and len(src) >= 2:
                show_notes += f"• {src[0]}: {src[1]}\n"
                
    ep["description"] = show_notes
    return filepath, file_size
