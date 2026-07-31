import os
import re
import edge_tts
from podcastti.config_loader import load_config

cfg = load_config()
hosts_cfg = cfg.get("hosts", {})
VOICE_TICO = hosts_cfg.get("host_1", {}).get("voice", "pt-BR-AntonioNeural")
VOICE_TECH = hosts_cfg.get("host_2", {}).get("voice", "pt-BR-FranciscaNeural")
VOICE_LEO = VOICE_TICO
VOICE_SARA = VOICE_TECH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "episodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text_for_speech(text: str) -> str:
    """
    Limpa rigorosamente o texto do roteiro antes de enviar para a síntese de voz TTS.
    Garante que URLs, tags HTML, marcas de tempo, colchetes, formatações Markdown
    e códigos nunca sejam lidos como fala pelo sintetizador de voz.
    """
    if not text:
        return ""
    
    # 1. Remove blocos de código Markdown (```...```)
    clean = re.sub(r'```[\s\S]*?```', '', text)
    # 2. Remove URLs completas (http, https, www, etc.)
    clean = re.sub(r'https?://\S+|www\.\S+', '', clean)
    # 3. Remove marcas de tempo tipo [00:00], [04:30], [18:00]
    clean = re.sub(r'\[\d{1,2}:\d{2}\]', '', clean)
    # 4. Remove colchetes e chaves com qualquer conteúdo
    clean = re.sub(r'\[[^\]]*\]|\{[^\}]*\}', '', clean)
    # 5. Remove tags HTML/XML
    clean = re.sub(r'<[^>]+>', '', clean)
    # 6. Remove marcações parentéticas de expressão (ex: (Risos), (Pausa))
    clean = re.sub(r'\([^\)]+\)', '', clean)
    # 7. Remove caracteres de formatação Markdown (*, _, `, #, ~, >)
    clean = re.sub(r'[\*\`\_\#\~\>]', '', clean)
    # 8. Limpa entidades HTML e substitui & por 'e' para prevenir falhas de SSML/XML no TTS
    clean = clean.replace("&quot;", '"').replace("&amp;", 'e').replace("&lt;", '').replace("&gt;", '')
    clean = clean.replace("&", "e")
    # 9. Normaliza múltiplos espaços e quebras de linha
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def strip_id3(data: bytes) -> bytes:
    """
    Remove cabeçalhos ID3v2 do áudio sintetizado para manter o fluxo MP3 100% limpo e válido.
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
    
    # Parâmetros de voz natural e expressiva
    rate = "+2%" if voice == VOICE_LEO else "+0%"
    pitch = "+1Hz" if voice == VOICE_LEO else "-1Hz"
    
    communicate = edge_tts.Communicate(clean_text, voice, rate=rate, pitch=pitch)
    audio_bytes = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.extend(chunk["data"])
                
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
            
        speaker_match = re.match(r'^(?:\*\*|\*)?\s*(Tico|Tech|Léo|Leo|Sara)\s*(?:\*\*|\*)?\s*:\s*(.*)', line, re.IGNORECASE)
        if speaker_match:
            raw_speaker = speaker_match.group(1).lower()
            if "tico" in raw_speaker or "léo" in raw_speaker or "leo" in raw_speaker:
                speaker = "Tico"
            else:
                speaker = "Tech"
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
    filename = f"ep{ep_id:02d}_podcastti_v2.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    print(f"\n[+] Sintetizando áudio limpo de alta fidelidade para o Episódio {ep_id}: {ep['title']}...")
    
    sections = parse_sections(ep["script"])
    full_audio = bytearray()
    
    current_time_seconds = 0.0
    dynamic_chapters = []
    BYTES_PER_SECOND = 6000.0  # 48 kbps mono MP3 do edge-tts = 6000 bytes/segundo
    
    for idx, (section_title, dialogues) in enumerate(sections, 1):
        timestamp_str = format_time(current_time_seconds)
        clean_title = re.sub(r'^(INTRODUÇÃO|BLOCO \d+:|ENCERRAMENTO E DICAS)\s*', '', section_title, flags=re.IGNORECASE).strip()
        if not clean_title:
            clean_title = section_title
        
        dynamic_chapters.append((timestamp_str, clean_title))
        section_bytes = 0
        
        print(f"  - Marcador [{timestamp_str}] Cap {idx:02d}: {clean_title}")
        for speaker, text in dialogues:
            voice = VOICE_TICO if speaker == "Tico" else VOICE_TECH
            chunk_audio = await synthesize_speech(text, voice)
            if chunk_audio:
                full_audio.extend(chunk_audio)
                section_bytes += len(chunk_audio)
            
        current_time_seconds += (section_bytes / BYTES_PER_SECOND)
        
    with open(filepath, "wb") as f:
        f.write(full_audio)
        
    file_size = len(full_audio)
    total_seconds = file_size / BYTES_PER_SECOND
    duration_str = format_duration_hhmmss(total_seconds)
    
    print(f"[OK] Áudio MP3 limpo gerado com sucesso: {filepath} ({file_size} bytes, Duração: {duration_str})")
    
    ep["audio_url"] = f"https://rapha-dias.github.io/PodCastTI/episodes/{filename}"
    ep["audio_bytes"] = file_size
    ep["duration"] = duration_str
    ep["local_audio_path"] = filepath
    ep["chapters"] = dynamic_chapters
    
    # Atualiza as show notes do episódio sem tags ou lixo de código
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
