# 🎙️ PodCastTI - Gerador Automático de Podcast sobre TI & Dados

> O podcast diário que traduz o **"tecniquês"** em conversas leves sobre **Python, SQL, Lógica de Programação e Ciência de Dados** para estudantes e iniciantes!

---

## 🎭 Os Apresentadores

- **Léo (Voz Neural `pt-BR-AntonioNeural`):** O estudante curioso. Faz perguntas simples de leigo e representa as dúvidas reais de quem está começando na faculdade.
- **Sara (Voz Neural `pt-BR-FranciscaNeural`):** A tutora especialista. Explica como os conceitos se aplicam na prática com analogias simples e encorajadoras.

---

## 🏗️ Arquitetura do Projeto

O **PodCastTI** segue uma arquitetura modular em Python para garantir manutenção limpa, alta legibilidade e automação total:

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
│   ├── ep01_podcastti.mp3
│   ├── ep02_podcastti.mp3
│   └── ep03_podcastti.mp3
├── main.py                    # Ponto de entrada CLI (python main.py)
├── rss.xml                    # Feed RSS final publicado
├── requirements.txt           # Dependências do projeto
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

### 3. Executar o Pipeline Automático
```bash
python main.py
```

---

## 📡 Integração com o Spotify

O podcast publica automaticamente no **Spotify** através do arquivo `rss.xml` hospedado no **GitHub Pages**:

- **URL do Feed RSS:** `https://rapha-dias.github.io/PodCastTI/rss.xml`

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE).
