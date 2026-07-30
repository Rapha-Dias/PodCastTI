import os
import re
import json
from google import genai

PROMPT_RULES = """
Você é um curador de conteúdo educacional e roteirista sênior de podcasts de TI.
Sua missão é gerar um roteiro de podcast dinâmico, didático, altamente envolvente e EXTENSO para o PodCastTI (duração estimada de 18 a 22 minutos de conversa falada).

Apresentadores:
- Léo: O estudante e iniciante curioso. Faz perguntas simples de leigo, expressa dúvidas reais de quem está começando na faculdade ou transição de carreira, pede exemplos práticos e resumos simples.
- Sara: A tutora especialista e encorajadora. Explica os conceitos com profundidade, utilizando analogias do cotidiano (ex: cozinha, trânsito, supermercado, construção) e dá dicas valiosas de estudo, carreira e código.

REGRAS DE CONTEÚDO E FALA NATURAL (EXTREMAMENTE IMPORTANTE):
1. NUNCA cite números de episódios de outros conteúdos (ex: NUNCA diga "Ep. 53", "Ep 50", "Episódio 49").
2. NUNCA cite nomes de fontes de notícias ou sites em voz alta (ex: NUNCA diga "veio do freeCodeCamp PT", "no site TabNews", etc.).
3. NUNCA cite links ou URLs no meio da fala.
4. Léo e Sara devem introduzir os assuntos de forma 100% natural e conversacional. Exemplo correto:
   Léo: Sara, vi que tem muita gente comentando sobre o trabalho da Júlia Labs com Hardware e LEDs. Como que um iniciante pode começar na eletrônica?
   Sara: Essa área é fantástica, Léo! Muita gente acha que precisa ser um gênio da física para mexer com hardware, mas na verdade...

REGRAS DE DURAÇÃO (18 a 22 MINUTOS):
- O ROTEIRO DEVE SER LONGO, COMPLETO E APROFUNDADO (Aproximadamente 2.500 a 3.000 palavras no total).
- Desenvolva entre 8 e 12 trocas de fala ricas para cada um dos 3 temas principais.
- Explore detalhadamente: o que é o conceito, analogias reais, por que é importante, erros comuns de iniciantes, como praticar no dia a dia e dicas de carreira.

Regras de Formatação:
1. O diálogo DEVE ter marcações claras de tempo [MM:SS] no início de cada bloco.
2. Cada linha de diálogo deve começar com 'Léo:' ou 'Sara:'.
3. Exemplo de marcação de bloco: [00:00] INTRODUÇÃO

Retorne estritamente um objeto JSON com a seguinte estrutura:
{
  "title": "Título chamativo e profissional do episódio",
  "summary": "Resumo abrangente do episódio em 3 a 4 frases.",
  "chapters": [
    ["00:00", "Intro & Destaques do Dia"],
    ["02:30", "Bloco 1: Título do Tema 1"],
    ["08:00", "Bloco 2: Título do Tema 2"],
    ["14:00", "Bloco 3: Título do Tema 3"],
    ["19:00", "Recapitulação & Dicas Finais"]
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

def clean_topic_title(raw_title: str) -> str:
    if not raw_title:
        return "Tecnologia e Desenvolvimento"
    title = raw_title.strip()
    title = re.sub(r'^(?:Ep\.?|Episódio)\s*\d+[:\-]?\s*', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title).strip()
    title = re.sub(r'^[:\-–—\s]+', '', title).strip()
    return title if title else raw_title

def generate_script_with_ai(news_items):
    api_key = get_gemini_api_key()
    
    formatted_news = ""
    for i, item in enumerate(news_items, 1):
        clean_t = clean_topic_title(item['title'])
        formatted_news += f"{i}. Tema: {clean_t}\n   Resumo: {item['summary']}\n\n"

    if api_key:
        try:
            print("[+] Gerando roteiro extenso (18-22 min) com Gemini AI...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{PROMPT_RULES}\n\nAqui estão os temas reais para o episódio de hoje:\n{formatted_news}",
                config={"response_mime_type": "application/json"}
            )
            raw_text = response.text.strip() if response.text else ""
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text, flags=re.IGNORECASE)
                raw_text = re.sub(r'\s*```$', '', raw_text)
            data = json.loads(raw_text)
            
            if isinstance(data, dict):
                script_text = data.get("script") or data.get("roteiro") or data.get("dialogo")
                first_clean_topic = clean_topic_title(news_items[0]['title']) if news_items else 'Tecnologia'
                title_text = data.get("title") or data.get("titulo") or f"Destaques de TI: {first_clean_topic}"
                if script_text:
                    data["script"] = script_text
                    data["title"] = title_text
                    data.setdefault("summary", "Neste episódio do PodCastTI, Léo e Sara analisam em profundidade as principais novidades de TI para estudantes e iniciantes!")
                    data.setdefault("chapters", [["00:00", "Intro & Destaques do Dia"]])
                    data.setdefault("sources", [[item['source'], item['link']] for item in news_items])
                    print("[OK] Roteiro extenso gerado com sucesso via Gemini AI!")
                    return data
        except Exception as e:
            print(f"[!] Aviso na API do Gemini: {e}. Utilizando gerador didático aprofundado.")

    # Fallback estruturado, didático e extenso (18 a 22 minutos)
    print("[+] Montando roteiro extenso didático (Fallback de alta profundidade)...")
    first_clean_title = clean_topic_title(news_items[0]['title']) if news_items else 'Lógica e Programação'
    title = f"Destaques de TI: {first_clean_title}"
    summary = "Neste episódio completo do PodCastTI, Léo e Sara mergulham fundo em tutoriais, conceitos essenciais e dicas de carreira para estudantes e iniciantes de tecnologia!"
    
    chapters = [["00:00", "Intro & Destaques do Dia"]]
    sources = []
    
    script_lines = [
        "[00:00] INTRODUÇÃO",
        "Léo: Olá, pessoal! Sejam muito bem-vindos ao PodCastTI, o seu espaço diário para descomplicar a tecnologia, dados e desenvolvimento!",
        "Sara: Fala, gente! Eu sou a Sara e hoje preparamos um episódio super completo. Vamos conversar com calma e em profundidade sobre os tópicos que mais geram dúvidas em quem está começando na faculdade ou em transição de carreira.",
        "Léo: É isso mesmo, Sara! Nosso objetivo aqui é tirar aquele peso de encarar termos difíceis e mostrar como cada conceito funciona na prática. Peguem seu café, ajustem os fones e vamos nessa!"
    ]
    
    for idx, item in enumerate(news_items[:3]):
        clean_title = clean_topic_title(item['title'])
        sources.append([item['source'], item['link']])
        
        script_lines.extend([
            f"\n[00:00] BLOCO {idx+1}: {clean_title.upper()}",
            f"Léo: Sara, hoje vamos conversar sobre {clean_title}. Muita gente que está começando ouve falar disso e fica sem saber por onde dar o primeiro passo. O que exatamente significa esse conceito na prática?",
            f"Sara: Excelente ponto, Léo! Para entender {clean_title}, vale a pena pensar em uma analogia do cotidiano. Imagine um sistema de organização doméstica ou uma cozinha de restaurante bem estruturada. {item['summary']} Se você não tem regras claras, o caos se instala rapidamente. Na tecnologia, esse conceito traz justamente a ordem e a automação que precisamos.",
            f"Léo: Que sensacional! Mas deixa eu te fazer uma pergunta de leigo: por que tantas pessoas acham isso difícil no começo? Onde é que os estudantes costumam travar?",
            f"Sara: O maior obstáculo é o excesso de informação! Muitos iniciantes tentam aprender todas as ferramentas, linguagens e frameworks ao mesmo tempo. Em vez de dominar a base da lógica e entender o porquê das coisas, tentam memorizar sintaxe de código. Isso gera uma sobrecarga mental imensa.",
            f"Léo: Caramba, passei exatamente por isso no meu primeiro semestre! Eu tentava decorar os comandos em vez de entender a lógica por trás. E como a gente faz para virar essa chave?",
            f"Sara: A melhor estratégia é aplicar o método de pequenos passos, ou baby steps. Pegue um problema grande, quebre em três partes simples e resolva uma de cada vez. Escreva em papel ou num quadro branco antes de ir para o teclado. Quando você desenha o fluxo primeiro, a implementação sai muito mais natural.",
            f"Léo: Boa! E quando a gente fala do mercado de trabalho, Sara? Como é que um estudante pode demonstrar que sabe aplicar esse conceito em uma entrevista de emprego ou num projeto do GitHub?",
            f"Sara: Os recrutadores e líderes técnicos procuram pessoas que saibam explicar a resolução do problema com clareza. Não basta apenas postar o código no GitHub; é fundamental escrever um bom arquivo README explicando o contexto, o desafio enfrentado e as decisões técnicas que você tomou. Isso demonstra maturidade profissional!",
            f"Léo: E para quem quer praticar hoje mesmo, qual seria o primeiro exercício prático recomendado?",
            f"Sara: Comece criando pequenos scripts e projetos pessoais que resolvam dores simples do seu dia a dia. Pode ser uma planilha automatizada em Python, um pequeno script de organização de arquivos ou uma consulta simples a um banco de dados SQL. O importante é ver a tecnologia funcionando e gerar aquele sentimento de conquista!",
            f"Léo: Incrível, Sara! Essa visão prática muda tudo. Certeza de que essa conversa vai dar uma clareza enorme para quem está nos ouvindo!"
        ])
        
    script_lines.extend([
        "\n[00:00] RECAPITULAÇÃO E DICAS DE ESTUDO",
        "Sara: E assim chegamos à nossa recapitulação de hoje! Lembrem-se sempre: aprender tecnologia é uma maratona de constância, não um tiro de cem metros. Dedicar trinta minutos todos os dias vale dez vezes mais do que estudar dez horas seguidas só no fim de semana.",
        "Léo: Com certeza, Sara! E para quem quiser aprofundar, todos os links das matérias e conteúdos recomendados estão salvos nas show notes do episódio e na nossa página oficial.",
        "Sara: Um grande abraço a todos, bons estudos e até o próximo episódio!",
        "Léo: Valeu pessoal, até a próxima!"
    ])
    
    chapters.append(["19:00", "Recapitulação & Dicas Finais"])
    
    return {
        "title": title,
        "summary": summary,
        "chapters": chapters,
        "sources": sources,
        "script": "\n".join(script_lines)
    }
