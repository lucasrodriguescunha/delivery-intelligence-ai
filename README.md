# Delivery Intelligence AI

<!-- Python ecosystem -->
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0+-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10+-11557C?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![joblib](https://img.shields.io/badge/joblib-1.4+-3776AB?style=flat&logo=python&logoColor=white)
<!-- API -->
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32+-499848?style=flat&logo=gunicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-E92063?style=flat&logo=pydantic&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-0.27+-009688?style=flat&logo=python&logoColor=white)
<!-- AI / ML -->
![sentence-transformers](https://img.shields.io/badge/sentence--transformers-3.0+-FF6F00?style=flat&logo=huggingface&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5+-FF6B35?style=flat&logo=databricks&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)
<!-- Frontend -->
![PHP](https://img.shields.io/badge/PHP-8.3+-777BB4?style=flat&logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-13+-FF2D20?style=flat&logo=laravel&logoColor=white)
![Livewire](https://img.shields.io/badge/Livewire-4.1+-4E56A6?style=flat&logo=livewire&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0+-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.0+-646CFF?style=flat&logo=vite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
<!-- Testes / Infra -->
![pytest](https://img.shields.io/badge/pytest-9.0+-0A9EDC?style=flat&logo=pytest&logoColor=white)
![Pest](https://img.shields.io/badge/Pest-4.7+-F4645F?style=flat&logo=php&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

Plataforma de inteligência operacional para restaurantes em ambiente de delivery, construída em fases incrementais. Combina machine learning, busca semântica, geração de insights via LLM e uma interface web completa.

---

## Roadmap de construção

Este projeto foi construído fase a fase, do dado bruto até a interface web. Cada fase entrega valor isolado e serve de base para a próxima.

### ✅ Fase 1 — MVP de dados

> Criar CSVs fictícios, carregar com Pandas, gerar métricas e gráficos.

**O que foi construído:**

- Geração de datasets sintéticos realistas: `pedidos.csv`, `avaliacoes.csv`, `restaurantes.csv`
- Análise exploratória com Pandas: ticket médio, taxa de atraso, volume por dia/clima
- Visualizações com Matplotlib (histogramas, barras, heatmap de correlação)
- Testes unitários das funções de métricas com pytest

**Arquivos:** `backend/app/analise.py` · `data/`

```bash
cd backend/app
python analise.py   # gera gráficos em backend/app/graficos/
```

---

### ✅ Fase 2 — Modelo de atraso

> Treinar um modelo simples para prever pedidos atrasados.

**O que foi construído:**

- Pipeline scikit-learn com `StandardScaler` + `OneHotEncoder` + `LogisticRegression`
- Features: valor, quantidade de itens, distância, clima, dia da semana, hora
- Avaliação com classification report, AUC-ROC e matriz de confusão
- Serialização do modelo treinado com joblib

**Arquivos:** `backend/app/modelo_atraso.py` · `docs/Modelo_de_Atraso.md`

```bash
cd backend/app
python modelo_atraso.py   # treina e salva em models/modelo_atraso.joblib
```

---

### ✅ Fase 3 — Embeddings e busca semântica

> Criar embeddings das avaliações e implementar busca semântica com ChromaDB.

**O que foi construído:**

- Geração de embeddings com `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
- Armazenamento vetorial persistente com ChromaDB
- Busca por similaridade de cosseno com filtro opcional de nota mínima
- Retorno de comentário, restaurante, nota e score de similaridade

**Arquivos:** `backend/app/embeddings.py` · `docs/Embeddings.md`

---

### ✅ Fase 4 — LLM Insights

> Criar endpoint que gera recomendações a partir das métricas e reviews recuperados.

**O que foi construído:**

- Endpoint de streaming com `StreamingResponse` + GPT-4o
- Contexto rico: métricas operacionais + avaliações recuperadas via busca semântica
- Saída estruturada em três seções: **Diagnóstico**, **Recomendações**, **Alertas**
- Prompt de sistema com persona de analista operacional

**Arquivos:** `backend/app/insights.py` · `docs/LLM_Insights.md`

---

### ✅ Fase 5 — API + Frontend

> Expor tudo em FastAPI e criar uma interface web com Laravel + Livewire.

**O que foi construído:**

**Backend (FastAPI):**
- `GET  /health` — health check
- `GET  /metricas` — métricas operacionais agregadas
- `POST /prever-atraso` — predição com probabilidade
- `POST /buscar-avaliacoes` — busca semântica em avaliações
- `POST /insights` — análise GPT-4o em streaming
- CORS configurado para o frontend

**Frontend (Laravel 13 + Livewire 4 + Flux UI):**
- Dashboard com cards de métricas em tempo real
- Formulário de previsão de atraso com feedback visual
- Interface de busca semântica com filtro de nota
- Gerador de insights com query customizável

**Arquivos:** `backend/app/main.py` · `frontend/` · `docs/ROTAS.md`

```bash
# FastAPI
cd backend/app && uvicorn main:app --reload --port 8000

# Laravel
cd frontend && php artisan serve --port=8001
```

---

## Arquitetura

```
delivery-intelligence-ai/
├── data/
│   ├── pedidos.csv           # Histórico de pedidos (features + target)
│   ├── avaliacoes.csv        # Avaliações dos clientes
│   └── restaurantes.csv      # Cadastro de restaurantes
├── backend/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/
│   │   ├── main.py           # API FastAPI
│   │   ├── analise.py        # Análise exploratória e gráficos
│   │   ├── modelo_atraso.py  # Treinamento do classificador ML
│   │   ├── embeddings.py     # ChromaDB + busca semântica
│   │   ├── insights.py       # Geração de insights via GPT-4o
│   │   ├── Dockerfile
│   │   └── models/
│   │       └── modelo_atraso.joblib
│   └── tests/
│       ├── conftest.py
│       ├── test_api.py
│       ├── test_embeddings.py
│       ├── test_metricas.py
│       └── test_modelo_atraso.py
├── frontend/
│   ├── app/
│   │   ├── Livewire/         # Componentes reativos
│   │   └── Services/         # DeliveryApiService
│   ├── resources/views/
│   │   ├── dashboard.blade.php
│   │   └── pages/delivery/   # prever-atraso, buscar-avaliacoes, insights
│   └── tests/
│       ├── Unit/Services/    # DeliveryApiServiceTest (15 testes)
│       └── Feature/
│           ├── Livewire/     # Dashboard, BuscarAvaliacoes, PreverAtraso, Insights (48 testes)
│           └── Integration/  # Testes com backend real (requer BACKEND_AVAILABLE=true)
└── docs/
    ├── ANALISE_EXPLORATORIA.md
    ├── MODELO_DE_ATRASO.md
    ├── EMBEDDINGS.md
    ├── LLM_INSIGHTS.md
    ├── ROTAS.md
    └── FRONTEND.md
```

## Stack

| Camada | Tecnologia |
|---|---|
| Dados | Python · Pandas · Matplotlib |
| ML | scikit-learn · joblib |
| Embeddings | sentence-transformers · ChromaDB |
| LLM | OpenAI GPT-4o |
| API | FastAPI · Uvicorn · Pydantic |
| Frontend | Laravel 13 · Livewire 4 · Flux UI |
| Testes | pytest · Pest PHP |
| Infraestrutura | Docker |

## Setup

**Pré-requisitos:** Python 3.12+, PHP 8.3+, Composer, Node.js, chave OpenAI

```bash
# 1. Dependências Python
pip install -r backend/requirements.txt

# 2. Treinar o modelo
cd backend/app && python modelo_atraso.py

# 3. Dependências Laravel
cd frontend && composer install && npm install && cp .env.example .env
php artisan key:generate && php artisan migrate

# 4. Variáveis de ambiente
# backend/.env ou export:
export OPENAI_API_KEY="sk-..."
# frontend/.env:
# DELIVERY_API_URL=http://localhost:8000
```

**Subir os servidores:**

```bash
# Terminal 1 — FastAPI
cd backend/app && uvicorn main:app --reload --port 8000

# Terminal 2 — Laravel
cd frontend && php artisan serve --port=8001
```

**Via Docker (apenas backend):**

```bash
docker build -f backend/app/Dockerfile -t delivery-intelligence-ai .
docker run -p 8000:8000 -e OPENAI_API_KEY="sk-..." delivery-intelligence-ai
```

## Testes

```bash
# Backend (pytest) — 50 testes
cd backend && pytest

# Frontend (Pest PHP) — 100 testes
cd frontend && php artisan test

# Frontend: testes de integração com backend real
cd frontend && BACKEND_AVAILABLE=true php artisan test --group=integration
```

## Documentação

| Módulo | Documento |
|---|---|
| Análise exploratória | [docs/ANALISE_EXPLORATORIA.md](docs/ANALISE_EXPLORATORIA.md) |
| Modelo de previsão de atraso | [docs/MODELO_DE_ATRASO.md](docs/MODELO_DE_ATRASO.md) |
| Busca semântica / embeddings | [docs/EMBEDDINGS.md](docs/EMBEDDINGS.md) |
| Geração de insights com LLM | [docs/LLM_INSIGHTS.md](docs/LLM_INSIGHTS.md) |
| Rotas da API | [docs/ROTAS.md](docs/ROTAS.md) |
| Frontend Laravel | [docs/FRONTEND.md](docs/FRONTEND.md) |
