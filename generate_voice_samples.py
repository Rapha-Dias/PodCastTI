import os
import asyncio
import edge_tts

VOICES = [
    {
        "id": "pt-BR-FranciscaNeural",
        "name": "Francisca (pt-BR - Feminina)",
        "text": "Olá, gente! Eu sou a Sara. Aqui a gente traduz o tecniquês em conversas simples pra você mandar super bem na faculdade de tecnologia!"
    },
    {
        "id": "pt-BR-ThalitaMultilingualNeural",
        "name": "Thalita (pt-BR - Multilíngue Feminina)",
        "text": "Olá, pessoal! Eu sou a Sara. Aqui no PodCastTI, nós desmistificamos Python, SQL e termos em inglês para acelerar o seu aprendizado."
    },
    {
        "id": "pt-BR-AntonioNeural",
        "name": "Antonio (pt-BR - Masculino)",
        "text": "Fala, pessoal! Eu sou o Léo. Tô animado pra tirar todas as minhas dúvidas de programação e salvar meu progresso no GitHub!"
    },
    {
        "id": "pt-PT-RaquelNeural",
        "name": "Raquel (pt-PT - Feminina)",
        "text": "Olá a todos! Eu sou a Sara. No PodCastTI, explicamos os conceitos fundamentais de programação e ciência de dados de forma simples."
    },
    {
        "id": "pt-PT-DuarteNeural",
        "name": "Duarte (pt-PT - Masculino)",
        "text": "Boas, pessoal! Eu sou o Léo e estou aqui para compreender como funcionam os algoritmos, a lógica e as bases de dados."
    }
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "voice_samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_sample(v):
    filename = f"amostra_{v['id']}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Gerando amostra para {v['name']}...")
    
    communicate = edge_tts.Communicate(v["text"], v["id"])
    await communicate.save(filepath)
    print(f"  [OK] Salvo em: {filepath}")

async def main():
    for v in VOICES:
        await generate_sample(v)
    print("\n[OK] Todas as amostras de voz foram geradas com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
