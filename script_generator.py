import os
import json
from google import genai

PROMPT_RULES = """
Você é um curador de conteúdo educacional e roteirista de podcasts de TI.
Você deve gerar o conteúdo para o podcast PodCastTI seguindo estritamente as diretrizes:

Apresentadores:
- Léo: O iniciante curioso (faz perguntas de leigo, expressa as dúvidas reais de um estudante).
- Sara: A tutora especialista e encorajadora (explica como os conceitos se aplicam na prática com analogias simples).

Tom: Descontraído, empático, motivador e altamente didático.

Sua resposta DEVE ser um JSON válido no seguinte formato exato:
{
  "title": "Título chamativo do episódio",
  "summary": "Resumo geral do episódio em 2 a 3 frases.",
  "chapters": [
    ["00:00", "Intro & Tema Principal"],
    ["02:00", "Bloco 1: Título Notícia 1"],
    ["08:00", "Bloco 2: Título Notícia 2"],
    ["14:00", "Bloco 3: Título Notícia 3"],
    ["18:00", "Recapitulação & Dicas Finais"]
  ],
  "sources": [
    ["Nome da Fonte 1", "https://url1.com"],
    ["Nome da Fonte 2", "https://url2.com"]
  ],
  "script": "[00:00] INTRODUÇÃO\\nLéo: ...\\nSara: ...\\n\\n[02:00] BLOCO 1\\n..."
}
"""

def generate_script_with_ai(news_items):
    api_key = os.environ.get("GEMINI_API_KEY")
    
    formatted_news = ""
    for i, item in enumerate(news_items, 1):
        formatted_news += f"{i}. Título: {item['title']}\n   Fonte: {item['source']} ({item['link']})\n   Resumo: {item['summary']}\n\n"

    if api_key:
        try:
            print("[+] Gerando roteiro com a API do Gemini...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{PROMPT_RULES}\n\nAqui estão as notícias reais do dia:\n{formatted_news}",
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            print("[OK] Roteiro gerado com sucesso via Gemini AI!")
            return data
        except Exception as e:
            print(f"[!] Erro ao chamar a API do Gemini: {e}. Usando gerador fallback.")

    # Fallback caso a API Key não esteja configurada localmente
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

if __name__ == "__main__":
    from news_fetcher import fetch_tech_news
    news = fetch_tech_news()
    res = generate_script_with_ai(news)
    print("Título gerado:", res["title"])
