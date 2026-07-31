import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "podcast_config.json")

def load_config():
    """Carrega as configurações personalizadas do arquivo podcast_config.json"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Erro ao ler {CONFIG_PATH}: {e}. Usando padrões.")
            
    # Configuração fallback padrão se o arquivo não existir
    return {
        "podcast": {
            "title": "Tico & Tech - Tudo sobre Python, SQL & Lógica Descomplicada",
            "tagline": "Tudo sobre Python, SQL & Lógica Descomplicada",
            "description": "O podcast diário que traduz o 'tecniquês' em conversas leves sobre Python, SQL e Lógica de Programação com Tico e Tech. Novos episódios diariamente às 07:00 da manhã.\n\n🎙️ Criado por Raphael Dias e Thiago Santis\n🌐 Acesse nosso site oficial: https://rapha-dias.github.io/PodCastTI/",
            "author": "Tico & Tech",
            "creator": "Raphael Dias e Thiago Santis",
            "email": "rdias@live.com",
            "link": "https://rapha-dias.github.io/PodCastTI",
            "spotify_link": "https://open.spotify.com/show/033XEfH7nMak9XeKKyUXmG",
            "category": "Technology",
            "language": "pt-br",
            "schedule_time_brt": "07:00 da manhã"
        },
        "hosts": {
            "host_1": {
                "name": "Tico",
                "voice": "pt-BR-AntonioNeural",
                "role": "O estudante curioso de tecnologia."
            },
            "host_2": {
                "name": "Tech",
                "voice": "pt-BR-FranciscaNeural",
                "role": "A especialista e tutora de dados."
            },
            "mascot": {
                "name": "Robô de IA",
                "role": "Assistente virtual de automação."
            }
        },
        "feeds": [
            {"name": "freeCodeCamp PT", "url": "https://www.freecodecamp.org/portuguese/news/rss/"},
            {"name": "Blog Alura", "url": "https://www.alura.com.br/artigos/rss"},
            {"name": "TabNews", "url": "https://www.tabnews.com.br/rss"}
        ],
        "keywords": ["python", "sql", "logica", "programacao", "banco de dados", "git", "github", "dados", "algoritmo", "desenvolvimento", "codigo", "ia"]
    }
