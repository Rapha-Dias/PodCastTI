import re
import feedparser

FEEDS = [
    {"name": "freeCodeCamp PT", "url": "https://www.freecodecamp.org/portuguese/news/rss/"},
    {"name": "Blog Alura", "url": "https://www.alura.com.br/artigos/rss"},
    {"name": "TabNews", "url": "https://www.tabnews.com.br/rss"},
]

def clean_html(text: str) -> str:
    cleaned = re.sub(r'<[^>]+>', '', text)
    return cleaned.strip()[:300]

def fetch_tech_news(max_items=4):
    """
    Coleta notícias de feeds RSS confiáveis sobre TI e programação.
    """
    articles = []
    
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:3]:
                title = clean_html(entry.title)
                link = entry.link
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                
                articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary if summary else title,
                    "source": feed_info["name"]
                })
        except Exception as e:
            print(f"[!] Erro ao buscar feed {feed_info['name']}: {e}")
            
    return articles[:max_items]
