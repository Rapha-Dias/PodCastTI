import feedparser
import re

FEEDS = [
    {"name": "freeCodeCamp PT", "url": "https://www.freecodecamp.org/portuguese/news/rss/"},
    {"name": "Blog Alura", "url": "https://www.alura.com.br/artigos/rss"},
    {"name": "TabNews", "url": "https://www.tabnews.com.br/rss"},
]

def clean_html(text: str) -> str:
    cleaned = re.sub(r'<[^>]+>', '', text)
    return cleaned.strip()[:300]

def fetch_tech_news(max_items=4):
    articles = []
    
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:3]:
                title = clean_html(entry.title)
                link = entry.link
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                
                # Filtra apenas notícias com temas relevantes para iniciantes se possível
                articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary if summary else title,
                    "source": feed_info["name"]
                })
        except Exception as e:
            print(f"[!] Erro ao buscar feed {feed_info['name']}: {e}")
            
    # Retorna os primeiros max_items
    return articles[:max_items]

if __name__ == "__main__":
    news = fetch_tech_news()
    print(f"Coletadas {len(news)} notícias:")
    for n in news:
        print(f"- [{n['source']}] {n['title']} ({n['link']})")
