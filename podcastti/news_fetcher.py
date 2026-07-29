import re
import urllib.request
import feedparser

FEEDS = [
    {"name": "freeCodeCamp PT", "url": "https://www.freecodecamp.org/portuguese/news/rss/"},
    {"name": "Blog Alura", "url": "https://www.alura.com.br/artigos/rss"},
    {"name": "TabNews", "url": "https://www.tabnews.com.br/rss"},
]

def clean_html(text: str) -> str:
    cleaned = re.sub(r'<[^>]+>', '', text)
    return cleaned.strip()[:300]

import ssl

def fetch_feed_data(url: str, timeout: int = 3) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PodCastTIBot/1.0"}
    )
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
        return resp.read()

def fetch_tech_news(max_items=4):
    """
    Coleta notícias de feeds RSS confiáveis sobre TI e programação com timeout seguro.
    """
    articles = []
    
    for feed_info in FEEDS:
        try:
            raw_data = fetch_feed_data(feed_info["url"], timeout=3)
            feed = feedparser.parse(raw_data)
            for entry in feed.entries[:3]:
                title = clean_html(entry.get("title", ""))
                if not title:
                    continue
                link = entry.get("link", feed_info["url"])
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                
                articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary if summary else title,
                    "source": feed_info["name"]
                })
        except Exception as e:
            print(f"[!] Aviso: erro ao buscar feed '{feed_info['name']}': {e}")
            
    if not articles:
        print("[!] Nenhum feed RSS respondeu a tempo. Utilizando tópicos essenciais de TI como fallback.")
        articles = [
            {
                "title": "Fundamentos de Python e Lógica de Programação para Iniciantes",
                "link": "https://www.freecodecamp.org/portuguese/news/",
                "summary": "Estruturas condicionais, laços e boas práticas de código limpo para quem está começando na faculdade.",
                "source": "PodCastTI Educação"
            },
            {
                "title": "SQL e Banco de Dados: Primeiros Passos com Queries e Filtros",
                "link": "https://www.alura.com.br/artigos/",
                "summary": "Aprenda a consultar tabelas, filtrar dados com WHERE e fazer junções com JOIN de forma didática.",
                "source": "PodCastTI Dados"
            }
        ]
            
    return articles[:max_items]

