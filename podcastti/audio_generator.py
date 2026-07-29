import os
import re
import edge_tts

VOICE_LEO = "pt-BR-AntonioNeural"
VOICE_SARA = "pt-BR-FranciscaNeural"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "episodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_text_to_ssml(text: str, voice: str) -> str:
    clean_text = re.sub(r'\(Risos\)', '<break time="300ms"/>', text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\(Pensativo\)', '<break time="400ms"/>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\(Pausa\)', '<break time="500ms"/>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\([^\)]+\)', '', clean_text)
    
    rate = "+3%" if voice == VOICE_LEO else "+0%"
    pitch = "+1Hz" if voice == VOICE_LEO else "+0Hz"
    
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">
    <voice name="{voice}">
        <prosody rate="{rate}" pitch="{pitch}">
            {clean_text}
        </prosody>
    </voice>
</speak>"""
    return ssml

async def synthesize_speech(text: str, voice: str) -> bytes:
    ssml = preprocess_text_to_ssml(text, voice)
    communicate = edge_tts.Communicate(ssml, voice)
    audio_bytes = bytearray()
    
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.extend(chunk["data"])
    except Exception as e:
        print(f"  [!] Fallback SSML para texto simples: {e}")
        plain_text = re.sub(r'\([^\)]+\)', '', text)
        communicate = edge_tts.Communicate(plain_text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.extend(chunk["data"])
                
    return bytes(audio_bytes)

def parse_sections(script_text: str):
    """
    Divide o roteiro por seções/blocos [MM:SS] TÍTULO
    """
    lines = script_text.strip().split("\n")
    sections = []
    current_title = "Intro"
    current_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("[") and "]" in line and ":" not in line:
            if current_lines:
                sections.append((current_title, current_lines))
                current_lines = []
            # Extrai título da seção
            current_title = line.split("]", 1)[1].strip()
        elif line.startswith("Léo:") or line.startswith("Léo :"):
            text = line.split(":", 1)[1].strip()
            current_lines.append(("Léo", text))
        elif line.startswith("Sara:") or line.startswith("Sara :"):
            text = line.split(":", 1)[1].strip()
            current_lines.append(("Sara", text))
            
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
    
    print(f"\n[+] Gerando áudio expressivo (SSML) para o Episódio {ep_id}: {ep['title']}...")
    
    sections = parse_sections(ep["script"])
    full_audio = bytearray()
    
    current_time_seconds = 0.0
    dynamic_chapters = []
    
    # Estimativa de taxa de bits para edge-tts (128 kbps ~ 16000 bytes/sec)
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
            full_audio.extend(chunk_audio)
            section_bytes += len(chunk_audio)
            
        current_time_seconds += (section_bytes / BYTES_PER_SECOND)
        
    with open(filepath, "wb") as f:
        f.write(full_audio)
        
    file_size = len(full_audio)
    total_seconds = file_size / BYTES_PER_SECOND
    duration_str = format_duration_hhmmss(total_seconds)
    
    print(f"[OK] Áudio gerado: {filepath} ({file_size} bytes, Duração real: {duration_str})")
    
    # Atualiza marcas de tempo reais nas show notes do episódio
    ep["audio_url"] = f"https://rapha-dias.github.io/PodCastTI/episodes/{filename}"
    ep["audio_bytes"] = file_size
    ep["duration"] = duration_str
    ep["local_audio_path"] = filepath
    
    # Reconstrói a descrição com as marcas de tempo dinâmicas e reais
    show_notes = f"{ep['summary']}\n\n📌 CAPÍTULOS DESTE EPISÓDIO:\n"
    for idx, (time_mark, ch_title) in enumerate(dynamic_chapters, 1):
        show_notes += f"{time_mark} - Cap {idx:02d}: {ch_title}\n"
        
    if "sources" in ep and ep["sources"]:
        show_notes += "\n🔗 FONTES CITADAS:\n"
        for src in ep["sources"]:
            if isinstance(src, (list, tuple)) and len(src) >= 2:
                show_notes += f"- {src[0]}: {src[1]}\n"
                
    ep["description"] = show_notes
    return filepath, file_size
