import os
import re
import json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from podcastti.config_loader import load_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
EPISODES_FILE = os.path.join(DATA_DIR, "episodes.json")
RSS_OUTPUT_FILE = os.path.join(BASE_DIR, "rss.xml")

os.makedirs(DATA_DIR, exist_ok=True)

def load_episodes():
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    old_file = os.path.join(BASE_DIR, "episodes.json")
    if os.path.exists(old_file):
        with open(old_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_episodes(episodes):
    # Limita o histórico mantendo apenas os 3 episódios mais recentes
    episodes = episodes[:3]
    with open(EPISODES_FILE, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

    # Remove arquivos MP3 antigos do diretório episodes/ que não estejam entre os 3 episódios mantidos
    episodes_dir = os.path.join(BASE_DIR, "episodes")
    if os.path.exists(episodes_dir):
        active_filenames = set()
        for ep in episodes:
            audio_url = ep.get("audio_url", "")
            if audio_url:
                active_filenames.add(os.path.basename(audio_url))
            local_path = ep.get("local_audio_path", "")
            if local_path:
                active_filenames.add(os.path.basename(local_path))
        
        for fname in os.listdir(episodes_dir):
            if fname.endswith(".mp3") and fname not in active_filenames:
                try:
                    os.remove(os.path.join(episodes_dir, fname))
                    print(f"[OK] Áudio antigo removido para manter apenas os últimos 3: {fname}")
                except Exception as e:
                    print(f"[!] Não foi possível remover áudio antigo {fname}: {e}")

def generate_rss_xml(episodes):
    # Garante no máximo os 3 episódios mais recentes no RSS
    episodes = episodes[:3]
    cfg = load_config()
    p = cfg["podcast"]
    podcast_title = p.get("title", "Tico & Tech")
    podcast_link = p.get("link", "https://rapha-dias.github.io/PodCastTI").rstrip("/")
    podcast_desc = p.get("description", "Podcast gerado com IA sobre Python e SQL")
    podcast_author = p.get("author", "Tico & Tech")
    podcast_email = os.environ.get("PODCAST_EMAIL", p.get("email", "rdias@live.com"))
    podcast_category = p.get("category", "Technology")
    podcast_language = p.get("language", "pt-br")
    podcast_image = f"{podcast_link}/cover.jpg"

    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
    })
    
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = podcast_title
    ET.SubElement(channel, "link").text = podcast_link
    ET.SubElement(channel, "description").text = podcast_desc
    ET.SubElement(channel, "language").text = podcast_language
    
    ET.SubElement(channel, "itunes:type").text = "episodic"
    ET.SubElement(channel, "itunes:author").text = podcast_author
    ET.SubElement(channel, "itunes:explicit").text = "no"

    owner = ET.SubElement(channel, "itunes:owner")
    ET.SubElement(owner, "itunes:name").text = podcast_author
    ET.SubElement(owner, "itunes:email").text = podcast_email

    ET.SubElement(channel, "managingEditor").text = f"{podcast_email} ({podcast_author})"
    
    # Imagem padrão RSS + itunes:image para compatibilidade total com Spotify & Apple Podcasts
    chan_img = ET.SubElement(channel, "image")
    ET.SubElement(chan_img, "url").text = podcast_image
    ET.SubElement(chan_img, "title").text = podcast_title
    ET.SubElement(chan_img, "link").text = podcast_link

    image = ET.SubElement(channel, "itunes:image")
    image.set("href", podcast_image)
    
    category = ET.SubElement(channel, "itunes:category")
    category.set("text", podcast_category)
    
    for ep in episodes:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep.get("title")
        ET.SubElement(item, "description").text = ep.get("description", "")
        ET.SubElement(item, "itunes:summary").text = ep.get("summary", ep.get("title"))
        ET.SubElement(item, "itunes:explicit").text = "no"
        
        guid_elem = ET.SubElement(item, "guid")
        guid_elem.text = ep.get("guid")
        guid_elem.set("isPermaLink", "false")
        
        ET.SubElement(item, "pubDate").text = ep.get("pubDate")
        ET.SubElement(item, "itunes:duration").text = ep.get("duration", "00:20:00")
        
        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", ep.get("audio_url", ""))
        enclosure.set("length", str(ep.get("audio_bytes", 25000000)))
        enclosure.set("type", "audio/mpeg")

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write(RSS_OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Feed RSS 2.0 atualizado com sucesso em: {RSS_OUTPUT_FILE}")

def add_new_episode(title, summary, script_text, audio_url, chapters, sources, audio_bytes=25000000):
    episodes = load_episodes()
    max_id = max([ep.get("id", 0) for ep in episodes], default=0)
    ep_num = max_id + 1
    today_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    guid = f"ticotech-ep{ep_num:03d}-{datetime.now().strftime('%Y%m%d')}"
    
    show_notes = f"🎙️ SOBRE ESTE EPISÓDIO:\n{summary}\n\n⏱️ CAPÍTULOS E MARCAS DE TEMPO:\n"
    for idx, (time_mark, ch_title) in enumerate(chapters, 1):
        clean_ch = re.sub(r'^(Bloco|Cap|Capítulo)\s*\d+:\s*', '', ch_title, flags=re.IGNORECASE)
        show_notes += f"• {time_mark} - Cap {idx:02d}: {clean_ch}\n"
        
    show_notes += "\n🔗 FONTES CITADAS E LINKS RECOMENDADOS:\n"
    for src_name, src_url in sources:
        show_notes += f"• {src_name}: {src_url}\n"
        
    final_title = title if re.match(r'^EP\d+', title, flags=re.IGNORECASE) else f"Ep {ep_num:02d}: {title}"
    new_ep = {
        "id": ep_num,
        "guid": guid,
        "title": final_title,
        "summary": summary,
        "description": show_notes,
        "audio_url": audio_url,
        "audio_bytes": audio_bytes,
        "pubDate": today_str,
        "duration": "00:20:00",
        "script": script_text,
        "sources": sources,
        "chapters": chapters
    }
    
    episodes.insert(0, new_ep)
    episodes = episodes[:3]
    save_episodes(episodes)
    generate_rss_xml(episodes)
    return new_ep
