import os
import sys
import json
import xml.etree.ElementTree as ET

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_suite():
    print("=" * 60)
    print("🧪 EXECUTANDO SUÍTE DE TESTES DO PODCAST TI")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = 6
    
    # TESTE 1: Integridade do Registro JSON (data/episodes.json)
    print("\n[Teste 1/6] Verificando data/episodes.json...")
    json_path = os.path.join(BASE_DIR, "data", "episodes.json")
    try:
        assert os.path.exists(json_path), "Arquivo data/episodes.json não existe!"
        with open(json_path, "r", encoding="utf-8") as f:
            episodes = json.load(f)
        assert isinstance(episodes, list), "O conteúdo de episodes.json deve ser uma lista!"
        if len(episodes) > 0:
            ep = episodes[0]
            assert "audio_url" in ep, "URL do áudio inválida no episódio!"
            assert "description" in ep, "Descrição ausente no episódio!"
            print(f"  ✅ APROVADO: {len(episodes)} episódio(s) no histórico. Último: '{ep.get('title')}'")
        else:
            print("  ✅ APROVADO: Registro JSON pronto (lista vazia para início do projeto).")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 2: Validação da Sintaxe do Feed XML (rss.xml)
    print("\n[Teste 2/6] Verificando sintaxe e tags de rss.xml...")
    rss_path = os.path.join(BASE_DIR, "rss.xml")
    try:
        assert os.path.exists(rss_path), "Arquivo rss.xml não existe!"
        tree = ET.parse(rss_path)
        root = tree.getroot()
        assert root.tag == "rss", "Tag raiz não é <rss>!"
        channel = root.find("channel")
        assert channel is not None, "Tag <channel> ausente!"
        title = channel.find("title").text
        assert "PodCastTI" in title, "Título do canal incorreto!"
        items = channel.findall("item")
        print(f"  ✅ APROVADO: Feed RSS válido. Canal: '{title}', Episódios listados: {len(items)}")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 3: Verificação do Diretório e Arquivos de Áudio (episodes/)
    print("\n[Teste 3/6] Verificando estrutura do diretório de episódios...")
    episodes_dir = os.path.join(BASE_DIR, "episodes")
    try:
        assert os.path.exists(episodes_dir), "Diretório 'episodes' não existe!"
        mp3_files = [f for f in os.listdir(episodes_dir) if f.endswith(".mp3")]
        if mp3_files:
            for mp3_name in mp3_files:
                mp3_path = os.path.join(episodes_dir, mp3_name)
                file_size = os.path.getsize(mp3_path)
                assert file_size > 100000, f"Arquivo {mp3_name} suspeitamente pequeno ({file_size} bytes)!"
            print(f"  ✅ APROVADO: Diretório válido com {len(mp3_files)} arquivo(s) MP3.")
        else:
            print("  ✅ APROVADO: Diretório 'episodes/' estruturado e limpo, pronto para o episódio 1.")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 4: Teste do Módulo de Notícias (podcastti/news_fetcher.py)
    print("\n[Teste 4/6] Testando módulo de busca de notícias (RSS Fetcher)...")
    try:
        from podcastti.news_fetcher import fetch_tech_news
        news = fetch_tech_news(max_items=2)
        assert len(news) > 0, "Nenhuma notícia retornada pelos feeds!"
        print(f"  ✅ APROVADO: {len(news)} notícias coletadas em tempo real. Ex: '{news[0]['title'][:40]}...'")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 5: Teste do Gerador de Roteiro (podcastti/script_generator.py)
    print("\n[Teste 5/6] Testando gerador de roteiro...")
    try:
        from podcastti.script_generator import generate_script_with_ai
        sample_news = [{"title": "Teste Python", "source": "fCC", "link": "http://example.com", "summary": "Resumo"}]
        res = generate_script_with_ai(sample_news)
        assert "title" in res and "script" in res, "Estrutura do roteiro inválida!"
        print(f"  ✅ APROVADO: Roteiro gerado com sucesso. Título: '{res['title']}'")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 6: Verificação do Módulo de Entrada Principal (main.py e imports)
    print("\n[Teste 6/6] Verificando integridade de main.py e podcastti...")
    try:
        import main
        from podcastti.pipeline import run_pipeline
        assert callable(run_pipeline), "Função run_pipeline não é invocável!"
        print("  ✅ APROVADO: Módulo main.py e pacote podcastti validados sem erros de importação.")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    print("\n" + "=" * 60)
    print(f"📊 RESULTADO FINAL DA AUDITORIA: {passed_tests}/{total_tests} TESTES APROVADOS")
    print("=" * 60)

if __name__ == "__main__":
    run_suite()
