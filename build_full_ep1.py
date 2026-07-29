import os
import sys
import json
import asyncio

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from podcastti.rss_generator import save_episodes, generate_rss_xml
from podcastti.audio_generator import generate_audio_for_episode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EPISODES_DIR = os.path.join(BASE_DIR, "episodes")
DATA_DIR = os.path.join(BASE_DIR, "data")
EPISODES_FILE = os.path.join(DATA_DIR, "episodes.json")

os.makedirs(EPISODES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

title = "Ep 01: Guia Definitivo de TI & Dados: Python vs SQL, Algoritmos e Carreira para Iniciantes"
summary = "No episódio completo de estreia do PodCastTI (20 minutos), Léo e Sara traduzem tudo o que você precisa saber no início da faculdade ou transição de carreira: como funcionam as variáveis e algoritmos em Python, como estruturar consultas SQL sem medo, dicas práticas no Kaggle Learn e o mapa mental para construir seus primeiros projetos."

script_text = """[00:00] INTRODUÇÃO E O DESAFIO DO PRIMEIRO ANO EM TI
Léo: Olá, pessoal! Sejam muito bem-vindos ao episódio oficial de estreia do PodCastTI! Eu sou o Léo e hoje estou vivendo aquele clássico momento de desespero que todo estudante de TI ou Ciência de Dados passa quando entra na faculdade ou inicia uma transição de carreira.
Sara: Fala, pessoal! Que alegria estar aqui com vocês! Eu sou a Sara, especialista em dados e tutora de tecnologia. Léo, calma! Não precisa entrar em pânico! Respira fundo. Qual é o grande pesadelo da semana?
Léo: Sara, você não tem ideia! Na primeira aula o professor começa falando de lógica de programação, na terça já coloca uma tela preta com código em Python, na quarta fala de banco de dados relacional e consultas SQL... Parecem dez idiomas diferentes ao mesmo tempo! Eu olho pra tela e sinto que estou tentando decifrar hieróglifos do Egito Antigo!
Sara: (Risos) Léo, esse sentimento é 100% universal! Qualquer profissional sênior que hoje constrói inteligências artificiais ou sistemas de grande escala já sentiu exatamente esse frio na barriga no primeiro mês. O grande segredo no início é não tentar memorizar a sintaxe de cada comando de cabeça, mas sim entender o conceito prático e a lógica por trás de cada ferramenta.
Léo: Que alívio ouvir isso! Então hoje nós vamos desmistificar tudo isso passo a passo?
Sara: Com certeza! Vamos passar por Python, variáveis, lógica de algoritmos, SQL, bancos de dados e ferramentas práticas para você treinar sem precisar instalar nada pesado no computador.

[04:00] BLOCO 1: LÓGICA DE PROGRAMAÇÃO, PYTHON E VARIÁVEIS NA PRÁTICA
Léo: Maravilha! Sara, vamos começar pelo Python. Todo mundo na comunidade de tecnologia diz que o Python é a melhor linguagem para quem está começando. Por que ela ganhou tanta popularidade?
Sara: Excelente ponto, Léo! O Python foi projetado desde a sua criação por Guido van Rossum nos anos noventa com uma filosofia muito clara: código limpo e legível. Em muitas linguagens tradicionais, para imprimir uma simples mensagem na tela você precisa escrever cinco ou seis linhas de configurações técnicas com chaves e ponto e vírgula. Em Python, você escreve apenas print, abre parênteses, coloca o texto entre aspas e pronto!
Léo: É literalmente em inglês simples!
Sara: Exatamente! Mas antes do Python vem a famosa Lógica de Programação. E o que é lógica de programação? Nada mais é do que o passo a passo ordenado para resolver um problema. É exatamente como uma receita de bolo. Se na receita você mandar assar a massa antes de misturar a farinha e os ovos, o bolo não vai funcionar. No computador é a mesma coisa: ele segue estritamente a ordem das suas instruções.
Léo: Entedi! E onde entram as famosas variáveis nessa receita?
Sara: Pense nas variáveis como potinhos com etiquetas organizadas na armário da sua cozinha. Se você pega um pote de plástico, cola uma etiqueta chamada 'açúcar' e coloca açúcar dentro, aquele pote agora guarda esse ingrediente. Em Python, se você escreve idade igual a vinte, você acabou de criar um potinho chamado idade que armazena o número vinte!
Léo: Nossa, é muito mais simples do que parecia! E eu posso mudar o valor que está dentro desse potinho depois?
Sara: Com certeza! Por isso se chama 'variável', porque o valor contido no potinho pode variar ao longo da execução do seu programa. Por exemplo, quando o usuário faz aniversário, a variável idade recebe o valor antigo mais um!
Léo: Genial! Então variável é só uma caixinha na memória do computador para guardar números, textos ou informações que vamos usar depois!

[09:00] BLOCO 2: BANCOS DE DADOS E A LINGUAGEM SQL
Léo: Agora vamos para a segunda grande dúvida que tira o sono dos iniciantes: o SQL e os Bancos de Dados Relacionais. Sara, se eu já posso guardar dados no Python, por que as empresas usam bancos de dados e SQL?
Sara: Essa é uma dúvida brilhante! Imagine que você trabalha em um grande e-commerce como o Mercado Livre ou a Amazon. Eles possuem dezenas de milhões de clientes, milhões de produtos e histórico de vendas de vários anos. Se você tentasse carregar todas essas informações direto na memória RAM de um programa em Python toda vez que alguém clica em um produto, o sistema travaria na hora!
Léo: Caramba, verdade! Seriam gigabytes ou terabytes de informação!
Sara: Exatamente. Para resolver isso existem os Bancos de Dados Relacionais. Eles são sistemas de armazenamento extremamente otimizados e seguros, organizados em tabelas muito parecidas com planilhas do Excel, com linhas e colunas interligadas.
Léo: E o SQL é a linguagem para conversar com essas tabelas?
Sara: Perfeitamente! SQL significa Structured Query Language, ou Linguagem de Consulta Estruturada. Não é uma linguagem para criar programas de computador, mas sim o idioma universal para fazer perguntas e buscar informações dentro dos bancos de dados.
Léo: Me dá um exemplo de como seria essa conversa com o banco de dados em SQL!
Sara: É super intuitivo! Se você quer ver o nome e o e-mail de todos os clientes que moram em São Paulo, você escreve: SELECT nome, email FROM clientes WHERE estado igual a SP. Em português claro: Selecione as colunas nome e email da tabela clientes onde o estado seja SP!
Léo: Caramba! O SELECT diz quais colunas eu quero ver, o FROM diz em qual tabela buscar, e o WHERE filtra exatamente a condição que eu preciso! É como fazer uma busca avançada com filtro automático!
Sara: Você pegou a essência de primeira, Léo! E quando você junta o SQL para extrair os dados certos com o Python para analisar e gerar gráficos, você tem o combo perfeito para qualquer profissional de Análise de Dados ou Ciência de Dados!

[14:30] BLOCO 3: FERRAMENTAS PRÁTICAS, KAGGLE LEARN E METODOLOGIA DE ESTUDOS
Léo: Sara, eu entendi a teoria e achei incrível. Mas o meu maior medo é travar na hora de praticar. Qual é a melhor forma de treinar sem ter que passar horas instalando softwares complexos no meu computador?
Sara: A nossa recomendação de ouro para quem está começando é usar o Kaggle Learn e o Google Colab! O Kaggle é a maior comunidade de ciência de dados do mundo, e eles oferecem cursos 100% gratuitos com ambientes interativos direto no seu navegador.
Léo: Ou seja, não precisa instalar nada? É só abrir o site e começar a digitar?
Sara: Nada de instalações pesadas! Você abre a lição no navegador, lê uma explicação curtinha de dois minutos e ao lado já digita o código na prática. Se você cometer algum erro de digitação, a própria plataforma te dá uma dica em tempo real explicando o que corrigir.
Léo: Que ferramenta fantástica! E qual é a sua dica de ouro para organizar a rotina de estudos para quem tem pouco tempo por dia?
Sara: Consistência supera intensidade! É infinitamente melhor praticar 30 minutos todos os dias do que tentar estudar 8 horas seguidas no domingo. Programe pequenos hábitos: leia uma lição de Python, escreva três consultas em SQL e teste no navegador. Em três meses você estará criando seus próprios projetos com extrema confiança!

[18:30] RECAPITULAÇÃO, PROJETOS PRÁTICOS E ENCERRAMENTO
Léo: Que conversa sensacional, Sara! Vamos fazer uma recapitulação rápida para guardar na memória tudo o que aprendemos no episódio de hoje?
Sara: Com certeza! Vamos ao resumo de sobrevivência:
Primeiro: Lógica de Programação é a receita do bolo. O Python é o idioma simples e legível para dar as instruções ao computador.
Segundo: Variáveis são caixinhas com etiquetas para guardar números, textos e dados na memória.
Terceiro: Bancos de Dados guardam grandes volumes de informação organizados em tabelas, e o SQL é a linguagem de consulta para selecionar e filtrar esses dados com comandos como SELECT, FROM e WHERE.
Quarto: Pratique diariamente no navegador com Kaggle Learn e Google Colab sem medo de errar. O erro no código é apenas o computador te ensinando como ser mais claro!
Léo: Perfeito! Os links para o Kaggle Learn, documentações e guias recomendados estão aqui na descrição do episódio nas nossas Show Notes.
Sara: Muito obrigada pela companhia de todos vocês! Continuem praticando, mandem suas dúvidas e nos vemos no próximo episódio!
Léo: Um grande abraço a todos, bons estudos e até a próxima!"""

sources = [
    ["freeCodeCamp - Guia de Python para Iniciantes", "https://www.freecodecamp.org/portuguese/news/o-guia-de-python-para-iniciantes/"],
    ["Alura - O que é SQL?", "https://www.alura.com.br/artigos/o-que-e-sql"],
    ["Kaggle Learn - Cursos Gratuitos de Python e SQL", "https://www.kaggle.com/learn"]
]

async def main():
    print("=" * 60)
    print("🎙️ GERANDO EPISÓDIO 01 COMPLETO E EXPANDIDO (18-22 MINUTOS)")
    print("=" * 60)
    
    save_episodes([])
    
    ep1_draft = {
        "id": 1,
        "guid": "podcastti-ep001-20260729-full",
        "title": title,
        "summary": summary,
        "description": "",
        "audio_url": "https://rapha-dias.github.io/PodCastTI/episodes/ep01_podcastti.mp3",
        "audio_bytes": 25000000,
        "pubDate": "Wed, 29 Jul 2026 03:00:00 +0000",
        "duration": "00:20:00",
        "script": script_text,
        "sources": sources
    }
    
    print("\n[+] Sintetizando áudio expressivo e calculando marcas de tempo dinâmicas...")
    filepath, file_size = await generate_audio_for_episode(ep1_draft)
    
    episodes = [ep1_draft]
    save_episodes(episodes)
    generate_rss_xml(episodes)
    
    print("\n" + "=" * 60)
    print("🎉 NOVO EPISÓDIO 01 COMPLETO GERADO COM SUCESSO!")
    print(f"📁 Áudio MP3: {filepath} ({file_size} bytes)")
    print(f"⏱️ Duração Exata: {ep1_draft['duration']}")
    print(f"📡 Feed RSS: {os.path.join(BASE_DIR, 'rss.xml')}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
