# 🎙️ Tico & Tech - Podcast sobre Python, SQL & Lógica Descomplicada

> O podcast diário que traduz o **"tecniquês"** em conversas leves e diretas sobre **Python, SQL, Lógica de Programação e Ciência de Dados** para estudantes e iniciantes!

---

## 🎭 Os Apresentadores & Mascote

- **Tico (Voz Neural `pt-BR-AntonioNeural`):** O estudante curioso e entusiasta de tecnologia. Faz perguntas simples de leigo e representa as dúvidas reais de quem está começando a aprender Python e SQL.
- **Tech (Voz Neural `pt-BR-FranciscaNeural`):** A tutora especialista em TI e Dados. Explica como os conceitos se aplicam na prática com analogias simples do dia a dia e dicas valiosas de código.
- **Robô de IA:** O mascote e assistente robô que busca as notícias de tecnologia em tempo real e auxilia na curadoria.

---

## 🎨 Design & Vídeo de Fundo Interativo

- **Capa Oficial:** Arte vibrantemente ilustrada com Tico, Tech, o Robô de IA e elementos gráficos de Python, SQL, soundwaves e puzzle pieces.
- **Fundo em Vídeo Interativo (60 FPS):** Renderizador Canvas em tempo real na página web (`index.html`) com:
  - Visualizador de ondas de áudio estéreo reativo ao player de áudio via Web Audio API.
  - Partículas flutuantes com elementos de código (`print("Olá!");`, `SELECT *`, `if-else`, `for-loops`, `lambda`, `{ }`, `</>`, `🐍 Python`, `📊 SQL`).
  - Parallax interativo com o movimento do mouse.
  - Botão de controle de Vídeo de Fundo (ON / OFF).

---

## 🏗️ Arquitetura do Projeto

O **Tico & Tech** segue uma arquitetura modular em Python para garantir manutenção limpa, alta legibilidade e automação total:

```text
PodCastTI/
├── .github/
│   └── workflows/
│       └── daily_podcast.yml  # Automação diária no GitHub Actions
├── podcastti/                 # Pacote principal da aplicação
│   ├── __init__.py
│   ├── news_fetcher.py        # Coleta matérias reais de feeds RSS de TI
│   ├── script_generator.py    # Gera o roteiro estruturado em JSON via Gemini AI
│   ├── audio_generator.py     # Sintetiza diálogos em MP3 com vozes neurais (edge-tts)
│   ├── rss_generator.py       # Gerador de Feed RSS 2.0 compatível com Spotify & Apple
│   └── pipeline.py            # Orquestrador mestre do fluxo
├── data/
│   └── episodes.json          # Banco de dados (JSON) dos episódios
├── episodes/                  # MP3s dos episódios gerados
├── main.py                    # Ponto de entrada CLI (python main.py)
├── cover.jpg                  # Capa oficial do Tico & Tech
├── index.html                 # Player web interativo com vídeo de fundo
├── rss.xml                    # Feed RSS final publicado
├── requirements.txt           # Dependências do projeto
├── test_all.py                # Suíte completa de testes
└── PROMPT.md                  # Diretrizes e regras do gerador
```

---

## ⚡ Como Rodar o Projeto Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/Rapha-Dias/PodCastTI.git
cd PodCastTI
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a Suíte de Testes
```bash
python test_all.py
```

### 4. Executar o Pipeline Automático
```bash
python main.py
```

---

## 📡 Integração com o Spotify & agregadores

O podcast publica automaticamente no **Spotify** e outros agregadores através do arquivo `rss.xml` hospedado no **GitHub Pages**:

- **URL do Feed RSS:** `https://rapha-dias.github.io/PodCastTI/rss.xml`

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE).
