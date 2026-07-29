import os
import sys
import asyncio

# Garante suporte a UTF-8 no console Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from news_fetcher import fetch_tech_news
from script_generator import generate_script_with_ai
from rss_generator import add_new_episode, load_episodes, generate_rss_xml
from generate_audio import generate_audio_for_episode

async def run_full_pipeline():
    print("=" * 60)
    print("INICIANDO PIPELINE AUTOMATICO DO PODCAST TI")
    print("=" * 60)
    
    # 1. Coleta Notícias Reais
    print("\n[Passo 1/4] Buscando matérias recentes em RSS feeds...")
    news = fetch_tech_news(max_items=3)
    if not news:
        print("[!] Nenhuma notícia foi encontrada. Interrompendo pipeline.")
        return
    print(f"[OK] {len(news)} notícias coletadas com sucesso.")
    
    # 2. Gera Roteiro Inteligente
    print("\n[Passo 2/4] Criando roteiro para Léo & Sara...")
    script_data = generate_script_with_ai(news)
    print(f"[OK] Roteiro criado: '{script_data['title']}'")
    
    # 3. Adiciona ao Registro de Episódios
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
    
    # 4. Sintetiza Áudio Neural em MP3
    print("\n[Passo 4/4] Sintetizando voz neural MP3...")
    filepath, file_size = await generate_audio_for_episode(new_ep)
    
    # Atualiza Feed XML Final
    episodes = load_episodes()
    generate_rss_xml(episodes)
    
    print("\n" + "=" * 60)
    print("PIPELINE CONCLUIDO COM SUCESSO!")
    print(f"Episódio gerado: {new_ep['title']}")
    print(f"Áudio MP3: {filepath} ({file_size} bytes)")
    print(f"Feed RSS: D:/01_Desenvolvimento/PodCastTI/rss.xml")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_full_pipeline())
