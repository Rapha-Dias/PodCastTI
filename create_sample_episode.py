import os
from rss_generator import add_new_episode

def build_episode_1():
    title = "Python vs SQL: O Guia de Sobrevivência para Iniciantes em TI"
    
    summary = (
        "No episódio de estreia do PodCastTI, Léo e Sara traduzem o 'tecniquês' "
        "para quem está começando em Análise de Dados e TI. Explicamos o que são variáveis em Python, "
        "como o SQL se comunica com bancos de dados e como praticar direto no navegador com o Kaggle Learn!"
    )
    
    script_text = """
[00:00] INTRODUÇÃO
Léo: Olá, pessoal! Bem-vindos a mais um episódio do nosso PodCastTI. Eu sou o Léo, e hoje eu tô daquele jeito: cheio de dúvidas.
Sara: E aí, gente! Eu sou a Sara. Léo, não precisa ter medo, eu tô aqui pra traduzir o "tecniquês" pra você. Qual é o drama de hoje?
Léo: Sara, o negócio é o seguinte. Imagina a cena: a pessoa acabou de entrar na faculdade de Análise de Dados. Começam a chover palavras como "Python", "SQL", "Lógica de Programação"... Eu confesso que me sinto olhando pra aquela tela preta cheia de letras verdes caindo, tipo no filme Matrix. Por onde a gente começa a respirar?

[02:00] BLOCO 1: PYTHON PARA INICIANTES
Sara: (Risos) É super normal esse susto inicial! Mas olha a primeira notícia que separamos hoje, lá do freeCodeCamp. Eles mostram que o Python foi criado justamente para ser legível. É quase como escrever instruções em um inglês bem simples. Na lógica de programação, antes de escrever o código, a gente só precisa pensar no passo a passo. Sabe quando você faz um bolo e segue a receita?
Léo: Sei, bater os ovos, colocar farinha...
Sara: Exato! O Python é só o idioma que você usa pra passar essa receita pro computador. O artigo mostra que você começa criando "variáveis", que são como potinhos de plástico na cozinha, onde você guarda os ingredientes. É muito mais simples do que parece.

[08:00] BLOCO 2: O QUE É SQL E BANCO DE DADOS
Léo: Tá, o Python eu entendi, é a receita do bolo. Mas e esse tal de SQL? A notícia da Alura diz que é a linguagem dos bancos de dados. Se eu já tenho o Python, por que eu preciso de outra linguagem?
Sara: Excelente pergunta! Pensa que o Python é a ferramenta que processa e analisa as coisas. Mas onde estão guardados os dados que você vai analisar na sua futura profissão? Eles ficam em grandes "arquivos digitais", que são os Bancos de Dados. O SQL é a linguagem que você usa pra ir até o arquivo e dizer: "Ei, me traz aí todos os clientes que compraram no mês passado".
Léo: Ahhh! Então no SQL eu uso aquele comando SELECT pra "selecionar" a gaveta certa do arquivo?
Sara: Exatamente! O SELECT diz o que você quer ver, e o comando WHERE funciona como um filtro, dizendo "onde" ou "qual a condição". É literalmente uma conversa com o banco de dados.

[14:00] BLOCO 3: MÃO NA MASSA COM KAGGLE LEARN
Léo: Genial. Mas só ler não adianta, né? Eu aprendo muito mais colocando a mão na massa.
Sara: E é por isso que trouxemos a dica do Kaggle Learn! O legal de lá é que não tem teoria chata. Você lê um conceito curtinho e já tem uma tela do lado pra digitar o seu código Python. Errou? O sistema avisa na hora. É o melhor amigo de quem tá pegando o ritmo frenético de provas e trabalhos práticos, porque você estuda fazendo.
Léo: Perfeito! Sem precisar baixar e instalar um milhão de programas pesados no meu notebook. Já vou favoritar todos esses links.

[18:00] ENCERRAMENTO E DICAS
Sara: Isso aí. E pra quem tá ouvindo: cliquem nos links, brinquem com os códigos e não tenham medo de errar. O erro é só o computador te pedindo pra explicar a receita de um jeito melhor!
"""

    chapters = [
        ("00:00", "Intro & O Drama do Léo"),
        ("02:00", "Bloco 1: Python e Variáveis (freeCodeCamp)"),
        ("08:00", "Bloco 2: Entendendo SQL e Bancos de Dados (Alura)"),
        ("14:00", "Bloco 3: Prática no Navegador com Kaggle Learn"),
        ("18:00", "Recapitulação & Dicas Finais")
    ]

    sources = [
        ("freeCodeCamp - Guia de Python para Iniciantes", "https://www.freecodecamp.org/portuguese/news/o-guia-de-python-para-iniciantes/"),
        ("Alura - O que é SQL?", "https://www.alura.com.br/artigos/o-que-e-sql"),
        ("Kaggle Learn - Python na Prática", "https://www.kaggle.com/learn/python")
    ]

    audio_url = "https://podcastti.vercel.app/episodes/ep01_python_vs_sql.mp3"
    
    ep = add_new_episode(
        title=title,
        summary=summary,
        script_text=script_text,
        audio_url=audio_url,
        chapters=chapters,
        sources=sources
    )
    print(f"[OK] Episodio criado com sucesso: {ep['title']}")

if __name__ == "__main__":
    build_episode_1()
