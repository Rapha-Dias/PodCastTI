import os
import sys
import json
import xml.etree.ElementTree as ET
import urllib.request

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_suite():
    print("=" * 60)
    print("🧪 EXECUTANDO SUÍTE DE TESTES COMPLETA DO PODCAST TI")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = 6
    
    # TESTE 1: Integridade do Registro JSON (data/episodes.json)
    print("\n[Teste 1/6] Verificando data/episodes.json...")
    json_path = os.path.join(BASE_DIR, "data", "episodes.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            episodes = json.load(f)
        assert len(episodes) >= 1, "Array de episódios vazio!"
        ep = episodes[0]
        assert ep["id"] == 1, "ID do episódio não é 1!"
        assert "audio_url" in ep and "ep01_podcastti.mp3" in ep["audio_url"], "URL do áudio inválida!"
        assert "Cap 01" in ep["description"], "Marcador de capítulo Cap 01 ausente na descrição!"
        print(f"  ✅ APROVADO: Episódio '{ep['title']}' validado. (Duração: {ep.get('duration')})")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 2: Validação da Sintaxe do Feed XML (rss.xml)
    print("\n[Teste 2/6] Verificando sintaxe e tags de rss.xml...")
    rss_path = os.path.join(BASE_DIR, "rss.xml")
    try:
        tree = ET.parse(rss_path)
        root = tree.getroot()
        assert root.tag == "rss", "Tag raiz não é <rss>!"
        channel = root.find("channel")
        assert channel is not None, "Tag <channel> ausente!"
        title = channel.find("title").text
        assert "PodCastTI" in title, "Título do canal incorreto!"
        
        items = channel.findall("item")
        assert len(items) >= 1, "Nenhum <item> de episódio encontrado no RSS!"
        enclosure = items[0].find("enclosure")
        assert enclosure is not None, "Tag <enclosure> do áudio ausente no item!"
        print(f"  ✅ APROVADO: Feed RSS válido. Canal: '{title}', Enclosure URL: {enclosure.get('url')}")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    # TESTE 3: Verificação do Arquivo de Áudio MP3 (episodes/ep01_podcastti.mp3)
    print("\n[Teste 3/6] Verificando arquivo de áudio MP3...")
    mp3_path = os.path.join(BASE_DIR, "episodes", "ep01_podcastti.mp3")
    try:
        assert os.path.exists(mp3_path), "Arquivo MP3 não existe!"
        file_size = os.path.getsize(mp3_path)
        assert file_size > 1000000, f"Tamanho do MP3 suspeitamente pequeno ({file_size} bytes)!"
        
        # Valida cabeçalho ID3 / MP3 frame
        with open(mp3_path, "rb") as f:
            header = f.read(3)
            assert header == b'ID3' or header[:2] in [b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'], "Cabeçalho MP3 inválido!"
            
        print(f"  ✅ APROVADO: Arquivo MP3 válido com {file_size} bytes ({file_size / (1024*1024):.2f} MB).")
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
        print("  ✅ APROVADO: Módulo main.py e podcastti validados sem erros de importação.")
        passed_tests += 1
    except Exception as e:
        print(f"  ❌ FALHOU: {e}")

    print("\n" + "=" * 60)
    print(f"📊 RESULTADO FINAL DA AUDITORIA: {passed_tests}/{total_tests} TESTES APROVADOS")
    print("=" * 60)

if __name__ == "__main__":
    run_suite()
