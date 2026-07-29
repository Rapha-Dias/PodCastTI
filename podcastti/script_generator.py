import os
import re
import json
from google import genai

PROMPT_RULES = """
Você é um curador de conteúdo educacional e roteirista sênior de podcasts de TI.
Sua missão é gerar um roteiro de podcast dinâmico, didático e envolvente para o PodCastTI (duração estimada entre 15 e 20 minutos de conversa).

Apresentadores:
- Léo: O estudante e iniciante curioso. Faz perguntas simples de leigo, expressa dúvidas reais de quem está começando na faculdade ou transição de carreira, pede exemplos práticos.
- Sara: A tutora especialista e encorajadora. Explica os conceitos com profundidade, utilizando analogias do cotidiano (ex: cozinha, trânsito, supermercado) e dá dicas valiosas de estudo e código.

Tom da conversa: Descontraído, empático, altamente didático e fluido.

Regras de Formatação:
1. O diálogo DEVE ter marcações claras de tempo [MM:SS] no início de cada bloco.
2. Cada linha de diálogo deve começar com 'Léo:' ou 'Sara:'.
3. Exemplo de marcação de bloco: [00:00] INTRODUÇÃO
4. Exemplo de diálogo:
   Léo: Fala Sara! Hoje tenho uma dúvida sobre SQL.
   Sara: Olá Léo! Que ótimo assunto, vamos desmistificar isso agora!

Retorne estritamente um objeto JSON com a seguinte estrutura:
{
  "title": "Título chamativo e profissional do episódio",
  "summary": "Resumo abrangente do episódio em 3 a 4 frases.",
  "chapters": [
    ["00:00", "Intro & Destaques do Dia"],
    ["02:30", "Bloco 1: Título do Tema 1"],
    ["08:00", "Bloco 2: Título do Tema 2"],
    ["14:00", "Bloco 3: Título do Tema 3"],
    ["18:00", "Recapitulação & Dicas Finais"]
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
            print("[+] Gerando roteiro estruturado com Gemini AI...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{PROMPT_RULES}\n\nAqui estão as notícias reais do dia:\n{formatted_news}",
                config={"response_mime_type": "application/json"}
            )
            raw_text = response.text.strip() if response.text else ""
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text, flags=re.IGNORECASE)
                raw_text = re.sub(r'\s*```$', '', raw_text)
            data = json.loads(raw_text)
            
            if isinstance(data, dict):
                script_text = data.get("script") or data.get("roteiro") or data.get("dialogo")
                title_text = data.get("title") or data.get("titulo") or f"Destaques de TI: {news_items[0]['title'] if news_items else 'Tecnologia'}"
                if script_text:
                    data["script"] = script_text
                    data["title"] = title_text
                    data.setdefault("summary", "Neste episódio do PodCastTI, Léo e Sara analisam as principais novidades de TI para estudantes e iniciantes!")
                    data.setdefault("chapters", [["00:00", "Intro & Destaques do Dia"]])
                    data.setdefault("sources", [[item['source'], item['link']] for item in news_items])
                    print("[OK] Roteiro gerado com sucesso via Gemini AI!")
                    return data
        except Exception as e:
            print(f"[!] Aviso na API do Gemini: {e}. Utilizando gerador didático de roteiros.")

    # Fallback estruturado e rico
    print("[+] Montando roteiro didático estruturado (Fallback)...")
    title = f"Destaques de TI: {news_items[0]['title'] if news_items else 'Lógica e Programação'}"
    summary = "Neste episódio do PodCastTI, Léo e Sara analisam as últimas novidades e tutoriais práticos de TI para ajudar estudantes e iniciantes!"
    
    chapters = [["00:00", "Intro & Destaques do Dia"]]
    sources = []
    
    script_lines = [
        "[00:00] INTRODUÇÃO",
        "Léo: Olá, pessoal! Sejam muito bem-vindos ao PodCastTI, o seu podcast diário de tecnologia e dados!",
        "Sara: Fala, gente! Eu sou a Sara e hoje trazemos tópicos incríveis sobre lógica de programação, Python e desenvolvimento para ajudar nos seus estudos.",
        "Léo: Isso mesmo! Vamos descomplicar o tecniquês e ver como aplicar tudo isso na prática."
    ]
    
    time_marks = ["02:30", "08:00", "14:00"]
    for idx, item in enumerate(news_items[:3]):
        t_mark = time_marks[idx] if idx < len(time_marks) else f"{15+idx}:00"
        chapters.append([t_mark, f"Bloco {idx+1}: {item['title'][:35]}"])
        sources.append([item['source'], item['link']])
        
        script_lines.extend([
            f"\n[{t_mark}] BLOCO {idx+1}: {item['title'].upper()}",
            f"Léo: Sara, a matéria principal desse bloco veio de {item['source']}: '{item['title']}'. O que o estudante iniciante precisa saber sobre isso?",
            f"Sara: Essa matéria é fundamental, Léo! Ela nos mostra que {item['summary']} Pense nisso como uma receita de bolo: você define os passos claros e o computador executa sem erros.",
            "Léo: Sensacional! Isso tira aquele medo inicial de encarar uma tela preta cheia de códigos.",
            "Sara: Exatamente! E a dica de ouro é praticar pequenas partes todos os dias em vez de tentar aprender tudo de uma vez."
        ])
        
    script_lines.extend([
        "\n[18:00] ENCERRAMENTO E DICAS",
        "Sara: E com isso encerramos o episódio de hoje! Não se esqueçam de conferir os links recomendados no feed ou na nossa página web.",
        "Léo: Até o próximo episódio, pessoal! Mantenham a curiosidade acesa e bons estudos!"
    ])
    
    chapters.append(["18:00", "Recapitulação & Dicas Finais"])
    
    return {
        "title": title,
        "summary": summary,
        "chapters": chapters,
        "sources": sources,
        "script": "\n".join(script_lines)
    }
