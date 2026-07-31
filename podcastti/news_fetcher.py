import re
import ssl
import urllib.request
import feedparser
from podcastti.config_loader import load_config

def clean_html(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r'<[^>]+>', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()[:350]

def fetch_feed_data(url: str, timeout: int = 4) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TicoTechBot/2.0"}
    )
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
        return resp.read()

def fetch_tech_news(max_items: int = 4, exclude_links: list = None) -> list:
    """
    Coleta e filtra notícias de feeds RSS sobre TI, dados e programação
    usando as configurações de podcast_config.json. Evita links já citados.
    """
    if exclude_links is None:
        exclude_links = []

    cfg = load_config()
    feeds = cfg.get("feeds", [])
    keywords = [kw.lower() for kw in cfg.get("keywords", [])]

    articles = []
    seen_links = set(exclude_links)
    
    for feed_info in feeds:
        try:
            raw_data = fetch_feed_data(feed_info["url"], timeout=4)
            feed = feedparser.parse(raw_data)
            for entry in feed.entries[:5]:
                link = entry.get("link", feed_info["url"])
                if link in seen_links:
                    continue

                title = clean_html(entry.get("title", ""))
                if not title:
                    continue

                summary = clean_html(entry.get("summary", entry.get("description", "")))
                full_text = f"{title} {summary}".lower()

                # Verifica relevância técnica
                if not keywords or any(kw in full_text for kw in keywords):
                    seen_links.add(link)
                    articles.append({
                        "title": title,
                        "link": link,
                        "summary": summary if summary else title,
                        "source": feed_info.get("name", "Fonte Tech")
                    })
                    if len(articles) >= max_items:
                        break
        except Exception as e:
            print(f"[!] Aviso: erro ao buscar feed '{feed_info.get('name', 'RSS')}': {e}")
            
    # Fallback se nenhum feed trouxer itens suficientes
    if len(articles) < 2:
        print("[!] Poucas notícias em tempo real. Adicionando tópicos essenciais de TI como fallback.")
        fallback_topics = [
            {
                "title": "Fundamentos de Python e Lógica de Programação para Iniciantes",
                "link": "https://www.freecodecamp.org/portuguese/news/python-logica-iniciantes",
                "summary": "Conceitos fundamentais de variáveis, estruturas condicionais e laços de repetição explicados com analogias do dia a dia.",
                "source": "Tico & Tech Educação"
            },
            {
                "title": "SQL e Bancos de Dados Relacionais: Dominando SELECT, WHERE e JOIN",
                "link": "https://www.alura.com.br/artigos/sql-banco-de-dados-iniciantes",
                "summary": "Guia prático para consultar tabelas de e-commerce, filtrar dados relevantes e realizar junções entre tabelas sem complicação.",
                "source": "Tico & Tech Dados"
            }
        ]
        for fb in fallback_topics:
            if fb["link"] not in seen_links and len(articles) < max_items:
                articles.append(fb)
                seen_links.add(fb["link"])
            
    return articles[:max_items]
