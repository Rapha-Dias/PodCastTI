import os
import re
import json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

PODCAST_TITLE = "PodCastTI - Tecnologia e Dados para Iniciantes"
PODCAST_LINK = "https://rapha-dias.github.io/PodCastTI"
PODCAST_DESCRIPTION = "O podcast diário que traduz o 'tecniquês' em conversas leves sobre Python, SQL, Lógica de Programação e Ciência de Dados para quem está começando na faculdade ou transição de carreira."
PODCAST_AUTHOR = "Léo & Sara"
PODCAST_EMAIL = os.environ.get("PODCAST_EMAIL", "contato@podcastti.local")
PODCAST_IMAGE = "https://rapha-dias.github.io/PodCastTI/cover.jpg"
PODCAST_CATEGORY = "Technology"
PODCAST_LANGUAGE = "pt-br"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
EPISODES_FILE = os.path.join(DATA_DIR, "episodes.json")
RSS_OUTPUT_FILE = os.path.join(BASE_DIR, "rss.xml")

os.makedirs(DATA_DIR, exist_ok=True)

def load_episodes():
    # Tenta ler do diretório data/ ou da raiz (fallback)
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    old_file = os.path.join(BASE_DIR, "episodes.json")
    if os.path.exists(old_file):
        with open(old_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_episodes(episodes):
    with open(EPISODES_FILE, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

def generate_rss_xml(episodes):
    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
    })
    
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = PODCAST_TITLE
    ET.SubElement(channel, "link").text = PODCAST_LINK
    ET.SubElement(channel, "description").text = PODCAST_DESCRIPTION
    ET.SubElement(channel, "language").text = PODCAST_LANGUAGE
    
    ET.SubElement(channel, "itunes:author").text = PODCAST_AUTHOR
    ET.SubElement(channel, "itunes:explicit").text = "no"

    owner = ET.SubElement(channel, "itunes:owner")
    ET.SubElement(owner, "itunes:name").text = PODCAST_AUTHOR
    ET.SubElement(owner, "itunes:email").text = PODCAST_EMAIL

    ET.SubElement(channel, "managingEditor").text = f"{PODCAST_EMAIL} ({PODCAST_AUTHOR})"
    
    image = ET.SubElement(channel, "itunes:image")
    image.set("href", PODCAST_IMAGE)
    
    category = ET.SubElement(channel, "itunes:category")
    category.set("text", PODCAST_CATEGORY)
    
    for ep in episodes:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep.get("title")
        ET.SubElement(item, "description").text = ep.get("description", "")
        ET.SubElement(item, "guid").text = ep.get("guid")
        ET.SubElement(item, "pubDate").text = ep.get("pubDate")
        ET.SubElement(item, "itunes:duration").text = ep.get("duration", "00:20:00")
        
        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", ep.get("audio_url", ""))
        enclosure.set("length", str(ep.get("audio_bytes", 25000000)))
        enclosure.set("type", "audio/mpeg")

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write(RSS_OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Feed RSS atualizado com sucesso em: {RSS_OUTPUT_FILE}")

def add_new_episode(title, summary, script_text, audio_url, chapters, sources, audio_bytes=25000000):
    episodes = load_episodes()
    ep_num = len(episodes) + 1
    today_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    guid = f"podcastti-ep{ep_num:03d}-{datetime.now().strftime('%Y%m%d')}"
    
    show_notes = f"{summary}\n\n📌 CAPÍTULOS DESTE EPISÓDIO:\n"
    for idx, (time_mark, ch_title) in enumerate(chapters, 1):
        # Remove prefixos redundantes caso existam
        clean_ch = re.sub(r'^(Bloco|Cap|Capítulo)\s*\d+:\s*', '', ch_title, flags=re.IGNORECASE)
        show_notes += f"{time_mark} - Cap {idx:02d}: {clean_ch}\n"
        
    show_notes += "\n🔗 FONTES CITADAS:\n"
    for src_name, src_url in sources:
        show_notes += f"- {src_name}: {src_url}\n"
        
    new_ep = {
        "id": ep_num,
        "guid": guid,
        "title": f"Ep {ep_num:02d}: {title}",
        "summary": summary,
        "description": show_notes,
        "audio_url": audio_url,
        "audio_bytes": audio_bytes,
        "pubDate": today_str,
        "duration": "00:20:00",
        "script": script_text
    }
    
    episodes.insert(0, new_ep)
    save_episodes(episodes)
    generate_rss_xml(episodes)
    return new_ep
