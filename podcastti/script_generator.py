import os
import json
from google import genai

PROMPT_RULES = """
Você é um curador de conteúdo educacional e roteirista sênior de podcasts de TI.
Sua missão é gerar um roteiro de podcast LONGO, COMPLETO e EXTENSO para o PodCastTI, com duração estimada entre 18 e 22 minutos (aproximadamente 2.300 a 2.800 palavras de diálogo natural e conversacional).

Apresentadores:
- Léo: O estudante/iniciante curioso (faz perguntas de leigo, relata dificuldades reais de quem está começando na faculdade, pede exemplos práticos).
- Sara: A tutora especialista e encorajadora (explica conceitos em profundidade com analogias do cotidiano, mostra como aplicar na prática, dá dicas de código e de estudo).

Tom: Descontraído, empático, altamente didático e fluido.

Diretrizes Obrigatórias para a Duração de 18 a 22 Minutos:
1. O diálogo DEVE ser RICO, EXTENSO e PROFUNDO. Cada bloco deve durar vários minutos de conversa ativa.
2. Léo e Sara devem discutir cada notícia/tema em detalhes: o que é, por que foi criado, problemas reais que resolve, exemplos práticos de código falado, erros comuns de iniciantes e analogias do dia a dia.
3. Evite respostas curtas ou superficiais. Desenvolva debates completos onde Léo faz réplicas, tira dúvidas sobre os conceitos e Sara explica o passo a passo com paciência e clareza.
4. Inclua exemplos de cenários reais (ex: bancos de dados de e-commerce, scripts de automação em Python, rotinas de estudos em TI).

Sua resposta DEVE ser um JSON válido no seguinte formato exato:
{
  "title": "Título chamativo e profissional do episódio",
  "summary": "Resumo detalhado e abrangente do episódio em 3 a 4 frases.",
  "chapters": [
    ["00:00", "Intro & Visão Geral do Dia"],
    ["02:30", "Bloco 1: Título Notícia/Tema 1"],
    ["07:30", "Bloco 2: Título Notícia/Tema 2"],
    ["13:00", "Bloco 3: Título Notícia/Tema 3"],
    ["18:00", "Recapitulação, Exercício Prático e Dicas Finais"]
  ],
  "sources": [
    ["Nome da Fonte 1", "https://url1.com"],
    ["Nome da Fonte 2", "https://url2.com"]
  ],
  "script": "[00:00] INTRODUÇÃO\\nLéo: ...\\nSara: ...\\n\\n[02:30] BLOCO 1\\n..."
}
"""

def get_gemini_api_key():
    for key, val in os.environ.items():
        if "GEMINI" in key.upper() and ("KEY" in key.upper() or "TOKEN" in key.upper() or "API" in key.upper()):
            if val and len(val) > 5:
                return val
    return os.environ.get("GEMINI_API_KEY")

def generate_script_with_ai(news_items):
    api_key = get_gemini_api_key()
    
    formatted_news = ""
    for i, item in enumerate(news_items, 1):
        formatted_news += f"{i}. Título: {item['title']}\n   Fonte: {item['source']} ({item['link']})\n   Resumo: {item['summary']}\n\n"

    if api_key:
        try:
            print("[+] Gerando roteiro com a API do Gemini...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{PROMPT_RULES}\n\nAqui estão as notícias reais do dia:\n{formatted_news}",
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            print("[OK] Roteiro gerado com sucesso via Gemini AI!")
            return data
        except Exception as e:
            print(f"[!] Erro ao chamar a API do Gemini: {e}. Usando gerador fallback.")

    # Fallback
    print("[+] Montando roteiro com as notícias coletadas (Fallback)...")
    title = f"Destaques de TI: {news_items[0]['title'] if news_items else 'Lógica e Programação'}"
    summary = "Neste episódio do PodCastTI, Léo e Sara analisam as últimas novidades e tutoriais práticos de TI para ajudar estudantes e iniciantes!"
    
    chapters = [["00:00", "Intro & Destaques do Dia"]]
    sources = []
    
    script_lines = [
        "[00:00] INTRODUÇÃO",
        "Léo: Olá, pessoal! Bem-vindos ao PodCastTI! Eu sou o Léo e hoje trouxe notícias muito legais pra gente discutir.",
        "Sara: Fala, gente! Eu sou a Sara. Vamos dar uma olhada no que rolou de mais importante no mundo dos estudos em TI hoje!"
    ]
    
    time_marks = ["02:00", "08:00", "14:00"]
    for idx, item in enumerate(news_items[:3]):
        t_mark = time_marks[idx] if idx < len(time_marks) else f"{15+idx}:00"
        chapters.append([t_mark, f"Bloco {idx+1}: {item['title'][:35]}"])
        sources.append([item['source'], item['link']])
        
        script_lines.extend([
            f"\n[{t_mark}] BLOCO {idx+1}: {item['title'].upper()}",
            f"Léo: Sara, a primeira notícia de hoje veio do site {item['source']}: '{item['title']}'. O que isso significa pra quem tá começando?",
            f"Sara: Essa matéria é sensacional, Léo! Ela explica que {item['summary']} Isso é fundamental porque reduz a curva de aprendizado de quem tá dando os primeiros passos.",
            "Léo: Maravilha! Já faz total sentido pro meu dia a dia de estudos."
        ])
        
    script_lines.extend([
        "\n[18:00] ENCERRAMENTO E DICAS",
        "Sara: E essas foram as dicas de hoje! Acessem os links nas Show Notes e continuem praticando todos os dias.",
        "Léo: Até o próximo episódio, pessoal! Bons estudos!"
    ])
    
    chapters.append(["18:00", "Recapitulação & Dicas Finais"])
    
    return {
        "title": title,
        "summary": summary,
        "chapters": chapters,
        "sources": sources,
        "script": "\n".join(script_lines)
    }
