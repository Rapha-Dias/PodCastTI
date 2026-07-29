import os
import sys
import glob
import json
import asyncio

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from podcastti.rss_generator import add_new_episode, save_episodes, generate_rss_xml
from podcastti.audio_generator import generate_audio_for_episode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EPISODES_DIR = os.path.join(BASE_DIR, "episodes")
DATA_DIR = os.path.join(BASE_DIR, "data")
EPISODES_FILE = os.path.join(DATA_DIR, "episodes.json")

async def expand_and_rebuild_ep1():
    print("=" * 60)
    print("🎙️ RECRIANDO O EPISÓDIO 1 COM DIÁLOGO EXPANDIDO E MARCAS DE TEMPO DINÂMICAS")
    print("=" * 60)
    
    os.makedirs(EPISODES_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    
    for mp3 in glob.glob(os.path.join(EPISODES_DIR, "*.mp3")):
        os.remove(mp3)
        
    save_episodes([])
    
    title = "Python vs SQL: O Guia de Sobrevivência para Iniciantes em TI"
    summary = (
        "No episódio de estreia do PodCastTI, Léo e Sara traduzem o 'tecniquês' "
        "para quem está começando em Análise de Dados e TI. Explicamos o que são variáveis em Python, "
        "como o SQL se comunica com bancos de dados e como praticar direto no navegador com o Kaggle Learn!"
    )
    
    script_text = """
[00:00] INTRODUÇÃO E O DRAMA DO LÉO
Léo: Olá, pessoal! Bem-vindos ao episódio de estreia do nosso PodCastTI! Eu sou o Léo, e hoje eu tô daquele jeito: totalmente perdido no começo da faculdade.
Sara: (Risos) E aí, gente! Eu sou a Sara. Léo, não precisa ter medo! Eu tô aqui pra traduzir o tecniquês pra você. Qual é o drama de hoje?
Léo: Sara, imagina a cena: a pessoa acabou de entrar na faculdade de Análise de Dados ou TI. Na primeira semana, começam a chover palavras estranhas: Python, SQL, Banco de Dados, Lógica de Programação... Eu confesso que me sinto olhando pra aquela tela preta cheia de letras verdes caindo, tipo no filme Matrix! Por onde a gente começa a respirar?
Sara: (Risos) É super normal esse susto inicial, Léo! Todo programador experiente já passou por esse mesmo momento. Mas a chave é entender o conceito por trás das ferramentas antes de se assustar com a sintaxe.

[01:00] PYTHON E VARIÁVEIS NA PRÁTICA
Léo: Maravilha! Então vamos para a primeira notícia do dia, lá do freeCodeCamp: o Guia de Python para Iniciantes. Sara, por que todo mundo diz que o Python é a melhor linguagem pra quem tá começando?
Sara: Porque o Python foi desenhado desde o primeiro dia para ser legível por seres humanos! É praticamente como escrever instruções em um inglês muito simples. Sabe quando você vai fazer um bolo e segue o passo a passo da receita?
Léo: Sei! Bater os ovos, juntar a farinha, colocar no forno...
Sara: Exato! Na lógica de programação, o algoritmo é a receita. O Python é só o idioma que você usa pra passar essa receita pro computador. E a primeira coisa que a gente aprende são as 'variáveis'.
Léo: E o que diabo é uma variável, Sara?
Sara: Pensa em potinhos de plástico na sua cozinha. Em um potinho você escreve o rótulo 'Açúcar' e guarda açúcar dentro. No outro, escreve 'Farinha'. Em Python, uma variável é esse potinho digital: você dá um nome pra ela, tipo 'idade' ou 'nome_usuario', e guarda um valor lá dentro pra usar depois!
Léo: Nossa, sensacional! Então criar uma variável é só dar um nome e guardar um dado no potinho!

[02:30] O QUE É SQL E BANCOS DE DADOS
Léo: Entendi o Python e a receita do bolo. Mas e esse tal de SQL que todo mundo fala? A matéria da Alura diz que é a linguagem dos bancos de dados. Se eu já tenho o Python, por que eu preciso de outra linguagem?
Sara: Excelente pergunta! Pensa comigo: o Python é a ferramenta de processar e analisar dados. Mas onde estão guardados os milhões de dados das empresas, dos clientes e dos produtos?
Léo: Em um arquivo gigante?
Sara: Exatamente! Eles ficam armazenados em Grandes Arquivos Digitais chamados Bancos de Dados Relacionais. O SQL não é uma linguagem para criar programas, é uma linguagem de consulta! É o idioma que você usa pra ir até o arquivo e conversar com ele.
Léo: Como assim conversar com o arquivo?
Sara: Você chega pro banco de dados e diz: "SELECT nome, e-mail FROM clientes WHERE compras > 100". Traduzindo: "Selecione o nome e o e-mail de todos os clientes onde o valor das compras foi maior que 100 reais".
Léo: Caramba, é literalmente uma pergunta! O SELECT diz o que você quer ver, e o WHERE é o filtro do que você quer encontrar!

[04:00] PRÁTICA NO NAVEGADOR COM KAGGLE LEARN
Léo: Genial! Mas Sara, só ler teoria não fixa na cabeça. Eu aprendo muito mais colocando a mão na massa.
Sara: E é por isso que trouxemos a terceira dica de hoje: o Kaggle Learn! O legal do Kaggle é que você aprende direto no navegador, sem precisar instalar nenhum programa pesado no seu computador.
Léo: Sério? Não preciso instalar nada?
Sara: Nada! Você abre o site, lê um trecho bem explicativo sobre Python ou SQL e do lado tem uma tela interativa pra você digitar o código. Se você errar, a plataforma te dá uma dica na hora. É a melhor ferramenta pra treinar entre as aulas da faculdade.

[05:00] RECAPITULAÇÃO E DICAS FINAIS
Léo: Perfeito! Já salvei todos esses links aqui no meu navegador!
Sara: É isso aí! E pra todos que estão ouvindo o PodCastTI: não tenham medo de errar o código. O erro na tela é só o computador pedindo pra você explicar a receita de um jeito melhor!
Léo: Com certeza! Os links de todas as matérias de hoje estão aqui nas nossas Show Notes. Valeu demais, Sara!
Sara: Valeu, Léo! Até o próximo episódio, pessoal! Bons estudos e boas linhas de código!
"""

    sources = [
        ("freeCodeCamp - Guia de Python para Iniciantes", "https://www.freecodecamp.org/portuguese/news/o-guia-de-python-para-iniciantes/"),
        ("Alura - O que é SQL?", "https://www.alura.com.br/artigos/o-que-e-sql"),
        ("Kaggle Learn - Python na Prática", "https://www.kaggle.com/learn/python")
    ]

    dummy_audio_url = "https://rapha-dias.github.io/PodCastTI/episodes/ep01_podcastti.mp3"
    
    print("\n[+] Registrando Episódio 01 Expandido...")
    ep1 = add_new_episode(
        title=title,
        summary=summary,
        script_text=script_text,
        audio_url=dummy_audio_url,
        chapters=[],
        sources=sources
    )
    
    print("\n[+] Sintetizando áudio neural e calculando marcas de tempo reais...")
    filepath, file_size = await generate_audio_for_episode(ep1)
    
    with open(EPISODES_FILE, "r", encoding="utf-8") as f:
        episodes = json.load(f)
        
    generate_rss_xml(episodes)
    
    print("\n" + "=" * 60)
    print("🎉 EPISÓDIO 01 COM MARCAS DE TEMPO DINÂMICAS CONCLUÍDO!")
    print(f"📁 Áudio MP3: {filepath} ({file_size} bytes)")
    print(f"⏱️ Duração Exata: {episodes[0]['duration']}")
    print(f"📡 Feed RSS: {os.path.join(BASE_DIR, 'rss.xml')}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(expand_and_rebuild_ep1())
