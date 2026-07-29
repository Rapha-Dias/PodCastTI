import os
import edge_tts

VOICE_LEO = "pt-BR-AntonioNeural"
VOICE_SARA = "pt-BR-FranciscaNeural"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "episodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def synthesize_speech(text: str, voice: str) -> bytes:
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.extend(chunk["data"])
    return bytes(audio_bytes)

def parse_script(script_text: str):
    lines = script_text.strip().split("\n")
    dialogues = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("[") and "]" in line and ":" not in line:
            continue
            
        if line.startswith("Léo:") or line.startswith("Léo :"):
            text = line.split(":", 1)[1].strip()
            dialogues.append(("Léo", text))
        elif line.startswith("Sara:") or line.startswith("Sara :"):
            text = line.split(":", 1)[1].strip()
            dialogues.append(("Sara", text))
            
    return dialogues

async def generate_audio_for_episode(ep):
    ep_id = ep["id"]
    filename = f"ep{ep_id:02d}_podcastti.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    print(f"\n[+] Gerando áudio para o Episódio {ep_id}: {ep['title']}...")
    
    dialogues = parse_script(ep["script"])
    full_audio = bytearray()
    
    for speaker, text in dialogues:
        voice = VOICE_LEO if speaker == "Léo" else VOICE_SARA
        print(f"  - [{speaker}]: {text[:50]}...")
        chunk_audio = await synthesize_speech(text, voice)
        full_audio.extend(chunk_audio)
        
    with open(filepath, "wb") as f:
        f.write(full_audio)
        
    file_size = len(full_audio)
    print(f"[OK] Arquivo de áudio salvo com sucesso: {filepath} ({file_size} bytes)")
    
    ep["audio_url"] = f"https://rapha-dias.github.io/PodCastTI/episodes/{filename}"
    ep["audio_bytes"] = file_size
    ep["local_audio_path"] = filepath
    return filepath, file_size
