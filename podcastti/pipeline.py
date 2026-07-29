import os
import sys
import asyncio

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from podcastti.news_fetcher import fetch_tech_news
from podcastti.script_generator import generate_script_with_ai
from podcastti.audio_generator import generate_audio_for_episode
from podcastti.rss_generator import add_new_episode, load_episodes, generate_rss_xml

async def run_pipeline():
    print("=" * 60)
    print("INICIANDO PIPELINE AUTOMÁTICO DO PODCAST TI")
    print("=" * 60)
    
    print("\n[Passo 1/4] Buscando matérias recentes em RSS feeds...")
    news = fetch_tech_news(max_items=3)
    if not news:
        print("[!] Nenhuma notícia foi encontrada. Interrompendo pipeline.")
        return
    print(f"[OK] {len(news)} notícias coletadas com sucesso.")
    
    print("\n[Passo 2/4] Criando roteiro para Léo & Sara...")
    script_data = generate_script_with_ai(news)
    print(f"[OK] Roteiro criado: '{script_data['title']}'")
    
    print("\n[Passo 3/4] Registrando episódio...")
    dummy_audio_url = "https://rapha-dias.github.io/PodCastTI/episodes/temp.mp3"
    new_ep = add_new_episode(
        title=script_data["title"],
        summary=script_data["summary"],
        script_text=script_data["script"],
        audio_url=dummy_audio_url,
        chapters=script_data["chapters"],
        sources=script_data["sources"]
    )
    
    print("\n[Passo 4/4] Sintetizando voz neural MP3...")
    filepath, file_size = await generate_audio_for_episode(new_ep)
    
    episodes = load_episodes()
    if episodes and episodes[0]["id"] == new_ep["id"]:
        episodes[0] = new_ep
    from podcastti.rss_generator import save_episodes
    save_episodes(episodes)
    generate_rss_xml(episodes)
    
    print("\n" + "=" * 60)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print(f"Episódio gerado: {new_ep['title']}")
    print(f"Áudio MP3: {filepath} ({file_size} bytes)")
    print("=" * 60)
