# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Python/FastAPI)
```bash
cd backend && pytest                                         # all 52 tests
cd backend && pytest tests/test_api.py -v                   # single test file
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000  # dev server
python backend/app/ml/modelo_atraso.py                      # retrain ML model
```

### Frontend (Laravel/Livewire)
```bash
cd frontend && php artisan test                              # all ~123 tests
cd frontend && php artisan test tests/Feature/Livewire/DashboardTest.php  # single file
cd frontend && BACKEND_AVAILABLE=true php artisan test --group=integration  # integration only
cd frontend && php artisan serve --port=8001                # dev server
cd frontend && npm run dev                                   # Vite asset watcher
cd frontend && ./vendor/bin/pint --parallel                 # autofix lint
cd frontend && ./vendor/bin/pint --parallel --test          # lint check only
```

### Docker
```bash
docker build -f backend/app/Dockerfile -t delivery-intelligence-ai .
docker run -p 8000:8000 -e OPENAI_API_KEY="sk-..." delivery-intelligence-ai
```

## Architecture

Two-service system: Laravel frontend (port 8001) → FastAPI backend (port 8000) → CSV data + ML model + ChromaDB.

### Backend (`backend/app/`)

- **`main.py`** — FastAPI app entry point. `@asynccontextmanager` lifespan loads ML model, ChromaDB collection, and DataFrames into the `estado` dict at startup.
- **`state.py`** — Single global dict (`estado`) shared across all route handlers; holds model, chroma collection, and pandas DataFrames.
- **`api/routes.py`** — 5 endpoints: `GET /health`, `GET /metricas`, `POST /prever-atraso`, `POST /buscar-avaliacoes`, `POST /insights`. Pydantic schemas in `models/schemas.py`.
- **`ml/modelo_atraso.py`** — scikit-learn Pipeline (StandardScaler + OneHotEncoder + LogisticRegression). Serialized to `modelo_atraso.joblib`. Features: valor_pedido, quantidade_itens, tempo_preparo_minutos, tempo_estimado_minutos, distancia_km, hora, clima, dia_semana.
- **`rag/embeddings.py`** — ChromaDB persistent store with `paraphrase-multilingual-MiniLM-L12-v2` embeddings. Cosine similarity search over customer reviews with optional min-rating filter.
- **`services/metricas.py`** — KPI aggregation (avg ticket, delay rate, delivery time, ratings) from CSV data.
- **`services/insights.py`** — Sends metrics + top reviews to GPT-4o; returns structured JSON with Diagnosis, Recommendations, Alerts.

### Frontend (`frontend/app/`)

- **`Services/DeliveryApiService.php`** — Single HTTP client wrapping all FastAPI endpoints. Injected into Livewire components. API URL configured via `DELIVERY_API_URL` env var (default: `http://localhost:8000`). Timeout: 120s.
- **`Livewire/Dashboard.php`** — 7 metric cards + 3 Chart.js charts (fetches `/metricas`, transforms to chart-ready arrays).
- **`Livewire/PreverAtraso.php`** — Form → `POST /prever-atraso` → delay probability display.
- **`Livewire/BuscarAvaliacoes.php`** — Semantic search form → `POST /buscar-avaliacoes`.
- **`Livewire/Insights.php`** — Custom query → `POST /insights` → structured LLM output display.

### Data (`data/`)
CSV files: `pedidos.csv` (orders), `avaliacoes.csv` (reviews), `restaurantes.csv`. Loaded once at backend startup into DataFrames. `gerar_avaliacoes.py` regenerates synthetic data.

## Key Conventions

- **Day ordering**: `services/metricas.py` has a custom helper normalizing Portuguese/English day names for consistent chart ordering.
- **Integration tests**: Skipped by default; require `BACKEND_AVAILABLE=true` env var and a running backend.
- **CORS**: Backend allows only `http://localhost:8001`.
- **Insights response**: JSON with keys `diagnostico`, `recomendacoes`, `alertas` — not plain text.
- **503 pattern**: Routes return HTTP 503 when `estado` is not initialized (model/data not loaded).
