import os
from rss_generator import add_new_episode

def build_episode_2():
    title = "Estruturas de Decisão e Git: Como Tomar Escolhas no Código e Nunca Mais Perder seus Projetos"
    
    summary = (
        "No segundo episódio do PodCastTI, Léo e Sara desmistificam como os programas tomam decisões com 'if/else' em Python, "
        "revelam a magia do Git/GitHub para salvar o progresso dos seus estudos de TI sem criar pastas como 'projeto_final_v2', "
        "e mostram ideias de projetos práticos para colocar a mão na massa!"
    )
    
    script_text = """
[00:00] INTRODUÇÃO
Léo: Fala, pessoal! Bem-vindos a mais um PodCastTI. Eu sou o Léo, seu colega de faculdade que fica desesperado a cada nova aula de programação.
Sara: (Risos) Calma, Léo! Eu sou a Sara, e a nossa missão aqui é transformar esse desespero em aprendizado prático e sem frescura. Preparado pro episódio de hoje?
Léo: Hoje eu tô muito curioso, Sara. Ontem eu tava tentando fazer um código em Python e me deparei com uma situação: "Se a nota do aluno for maior que 7, aprovado. Se não, reprovado". Como o computador sabe escolher o caminho certo? E pior: salvei o arquivo como 'trabalho_final_OFICIAL_v3.py' e perdi metade do código!

[02:00] BLOCO 1: ESTRUTURAS DE DECISÃO (IF, ELIF, ELSE)
Sara: (Risos) Quem nunca salvou um arquivo assim que atire a primeira pedra! Mas calma, vamos por partes. O primeiro assunto de hoje veio de um artigo incrível da Alura sobre estruturas condicionais em Python. Na vida real, você toma decisões o tempo todo: "Se estiver chovendo, levo guarda-chuva; senão, vou de óculos de sol".
Léo: Exatamente!
Sara: No Python é igualzinho. A gente usa a palavra 'if' para o 'se', e 'else' para o 'senão'. Se você tiver mais de duas opções, entra o 'elif' (que é a junção de 'else' + 'if'). É como um semáforo: se for verde, siga; se for amarelo, atente; se for vermelho, pare!
Léo: Ahhh, então o computador lê essa condição, avalia se é Verdadeiro ou Falso, e decide qual bloco de código vai executar!
Sara: Perfeito! Viu como a lógica de programação nada mais é do que o nosso pensamento do dia a dia traduzido em regras simples?

[08:00] BLOCO 2: GIT E GITHUB - O 'CONTROL+Z' DEFINITIVO
Léo: Caramba, fez total sentido! Agora me salva da segunda dor de cabeça: como eu paro de criar 'trabalho_v1.py', 'trabalho_v2_final.py'?
Sara: Aí entra a nossa segunda notícia do dia, direto do freeCodeCamp: o Guia de Git e GitHub para Iniciantes! O Git é como uma máquina do tempo pro seu código. Em vez de duplicar arquivos, você trabalha em um projeto só e faz 'commits', que são fotos do seu código naquele momento exato.
Léo: E se eu fizer uma besteira gigantesca e quebrar o código todo?
Sara: Você simplesmente volta no tempo pro 'commit' anterior! E o GitHub é a nuvem onde você guarda essa máquina do tempo, além de ser o seu portfólio para mostrar pra futuros recrutadores. É indispensável pra qualquer estudante de TI.

[14:00] BLOCO 3: PROJETOS PRÁTICOS PARA FIXAR
Léo: Sensacional! Já entendi que preciso instalar o Git hoje mesmo. Mas o que eu posso construir pra treinar 'if/else' e já subir pro meu GitHub?
Sara: O freeCodeCamp publicou uma lista com 25 projetos práticos em Python. Pra quem tá começando, a dica de ouro é criar uma 'Calculadora de IMC' ou um 'Jogo de Adivinhação de Números'. São projetos pequenos, que usam variáveis, 'if/else' e entrada do usuário. Você faz em 30 minutos e já ganha uma confiança gigante!
Léo: Nossa, adorei a ideia do jogo de adivinhação! O computador sorteia um número e o 'if' checa se o meu palpite foi maior ou menor!

[18:00] ENCERRAMENTO E DICAS
Sara: Exatamente! É assim que a lógica ganha vida. Para todos os estudantes ou entusiastas de tecnologia acompanhando: não fiquem só na teoria. Crie seu projeto simples, use o Git pra registrar sua evolução e comemore cada 'if' que funcionar!
Léo: Com certeza! Os links de todas as matérias de hoje estão nas nossas Show Notes. Valeu demais, Sara! Até o próximo episódio, pessoal!
Sara: Até a próxima, gente! Bons estudos e boas linhas de código!
"""

    chapters = [
        ("00:00", "Intro & O Drama das Versões de Arquivo"),
        ("02:00", "Bloco 1: Se, Senão e Estruturas Condicionais (Alura)"),
        ("08:00", "Bloco 2: Git e GitHub para Iniciantes (freeCodeCamp)"),
        ("14:00", "Bloco 3: 25 Projetos Práticos em Python (freeCodeCamp)"),
        ("18:00", "Recapitulação & Dicas Finais")
    ]

    sources = [
        ("Alura - Estruturas Condicionais em Python", "https://www.alura.com.br/artigos/estruturas-condicionais-python"),
        ("freeCodeCamp - Guia de Git e GitHub para Iniciantes", "https://www.freecodecamp.org/portuguese/news/o-guia-de-git-e-github-para-iniciantes/"),
        ("freeCodeCamp - 25 Projetos em Python para Iniciantes", "https://www.freecodecamp.org/portuguese/news/25-projetos-em-python-para-iniciantes-ideias-faceis-para-comecar-a-programar-em-python/")
    ]

    audio_url = "https://podcastti.vercel.app/episodes/ep02_estruturas_e_git.mp3"
    
    ep = add_new_episode(
        title=title,
        summary=summary,
        script_text=script_text,
        audio_url=audio_url,
        chapters=chapters,
        sources=sources
    )
    print(f"[OK] Episodio 2 criado com sucesso: {ep['title']}")

if __name__ == "__main__":
    build_episode_2()
