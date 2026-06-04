# Delivery Intelligence AI Platform

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.0+-150458?style=flat&logo=pandas&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5+-FF6B35?style=flat&logo=databricks&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.0+-0A9EDC?style=flat&logo=pytest&logoColor=white)

Plataforma de inteligência operacional para restaurantes em ambiente de delivery. Combina machine learning para previsão de atrasos, busca semântica sobre avaliações de clientes e geração de insights via LLM.

## Arquitetura

```
delivery-intelligence-ai/
├── data/
│   ├── pedidos.csv          # Histórico de pedidos com features e target
│   ├── avaliacoes.csv       # Avaliações dos clientes
│   └── restaurantes.csv     # Cadastro de restaurantes
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py          # API FastAPI (ponto de entrada)
│       ├── modelo_atraso.py # Treinamento do classificador ML
│       ├── embeddings.py    # ChromaDB + busca semântica
│       ├── insights.py      # Geração de insights via GPT-4o
│       ├── analise.py       # Análise exploratória e gráficos
│       └── models/
│           └── modelo_atraso.joblib
└── docs/
    ├── Modelo_de_Atraso.md
    ├── Embeddings.md
    ├── LLM_Insights.md
    ├── ROTAS.md
    └── Analise_Exploratoria.md
```

## Pré-requisitos

- Python 3.12+
- Chave de API da OpenAI

## Instalação

```bash
pip install -r backend/requirements.txt
```

## Variáveis de ambiente

```bash
export OPENAI_API_KEY="sk-..."
```

## Execução passo a passo

### 1. Análise exploratória (opcional)

Explora os dados e gera gráficos em `backend/app/graficos/`.

```bash
cd backend/app
python analise.py
```

### 2. Treinar o modelo de atraso

Treina o classificador e salva em `backend/app/models/modelo_atraso.joblib`.

```bash
cd backend/app
python modelo_atraso.py
```

### 3. Inicializar o banco de embeddings (opcional)

Popula o ChromaDB com as avaliações. A API faz isso automaticamente no startup, mas pode ser testado isoladamente.

```bash
cd backend/app
python embeddings.py
```

### 4. Subir a API

```bash
cd backend/app
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`.
Documentação Swagger: `http://localhost:8000/docs`

### 5. Subir via Docker

```bash
# A partir da raiz do projeto
docker build -f backend/app/Dockerfile -t delivery-intelligence-ai .
docker run -p 8000:8000 -e OPENAI_API_KEY="sk-..." delivery-intelligence-ai
```

## Testes

```bash
cd backend/app
pytest
```

## Documentação detalhada

| Módulo | Documento |
|---|---|
| Modelo de previsão de atraso | [docs/Modelo_de_Atraso.md](docs/Modelo_de_Atraso.md) |
| Busca semântica / embeddings | [docs/Embeddings.md](docs/Embeddings.md) |
| Geração de insights com LLM | [docs/LLM_Insights.md](docs/LLM_Insights.md) |
| Rotas da API | [docs/ROTAS.md](docs/ROTAS.md) |
| Análise exploratória | [docs/Analise_Exploratoria.md](docs/Analise_Exploratoria.md) |
