import os
import re
import edge_tts

VOICE_LEO = "pt-BR-AntonioNeural"
VOICE_SARA = "pt-BR-FranciscaNeural"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "episodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_text_to_ssml(text: str, voice: str) -> str:
    """
    Converte anotações de cena (ex: (Risos), (Pensativo)) em pausas expressivas SSML
    e ajusta a entonação (prosody) conforme o personagem.
    """
    # Substitui marcações entre parênteses por pausas curtas e naturais
    clean_text = re.sub(r'\(Risos\)', '<break time="300ms"/>', text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\(Pensativo\)', '<break time="400ms"/>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\(Pausa\)', '<break time="500ms"/>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\([^\)]+\)', '', clean_text) # Remove quaisquer outras anotações
    
    # Ajustes prosódicos específicos
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
        # Fallback para texto plano caso o SSML falhe em algum caracter especial
        print(f"  [!] Fallback SSML para texto simples: {e}")
        plain_text = re.sub(r'\([^\)]+\)', '', text)
        communicate = edge_tts.Communicate(plain_text, voice)
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
    
    print(f"\n[+] Gerando áudio expressivo (SSML) para o Episódio {ep_id}: {ep['title']}...")
    
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
    print(f"[OK] Áudio turbinado salvo com sucesso: {filepath} ({file_size} bytes)")
    
    ep["audio_url"] = f"https://rapha-dias.github.io/PodCastTI/episodes/{filename}"
    ep["audio_bytes"] = file_size
    ep["local_audio_path"] = filepath
    return filepath, file_size
