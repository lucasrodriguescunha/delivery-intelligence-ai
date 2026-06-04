from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import chromadb
from embeddings import criar_colecao, criar_funcao_embedding, buscar, popular_colecao, carregar_avaliacoes
from insights import gerar_insights_stream

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "../../data"
MODELO_PATH = BASE_DIR / "models/modelo_atraso.joblib"
CHROMA_PATH = str(BASE_DIR / "chroma_db")

FEATURES_NUMERICAS = [
    "valor_pedido",
    "quantidade_itens",
    "tempo_preparo_minutos",
    "tempo_estimado_minutos",
    "distancia_km",
    "hora",
]
FEATURES_CATEGORICAS = ["clima", "dia_semana"]

estado = {}


def calcular_metricas(df: pd.DataFrame, df_avaliacoes: pd.DataFrame) -> dict:
    total = len(df)
    atrasados = int(df["atrasado"].sum())

    return {
        "ticket_medio_R$": round(float(df["valor_pedido"].mean()), 2),
        "total_pedidos": total,
        "pedidos_atrasados": atrasados,
        "percentual_atraso_%": round((atrasados / total) * 100, 1),
        "tempo_medio_entrega_min": round(float(df["tempo_total_minutos"].mean()), 1),
        "nota_media_geral": round(float(df_avaliacoes["nota"].mean()), 2),
        "clima_maior_atraso": (
            df.groupby("clima")["atrasado"]
            .mean()
            .idxmax()
        ),
        "dia_maior_volume": (
            df.groupby("dia_semana")
            .size()
            .idxmax()
        ),
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    estado["pipeline"] = joblib.load(MODELO_PATH)

    funcao_embedding = criar_funcao_embedding()
    client_chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    colecao = criar_colecao(client_chroma, funcao_embedding)

    df_aval = carregar_avaliacoes(
        str(DATA_DIR / "avaliacoes.csv"),
        str(DATA_DIR / "restaurantes.csv"),
    )
    popular_colecao(colecao, df_aval)

    estado["colecao"] = colecao
    estado["df_pedidos"] = pd.read_csv(DATA_DIR / "pedidos.csv")
    estado["df_avaliacoes"] = pd.read_csv(DATA_DIR / "avaliacoes.csv")

    yield

    estado.clear()


app = FastAPI(title="Delivery Intelligence AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Schemas ---

class PreverAtrasoRequest(BaseModel):
    valor_pedido: float
    quantidade_itens: int
    tempo_preparo_minutos: float
    tempo_estimado_minutos: float
    distancia_km: float
    hora: int
    clima: str
    dia_semana: str


class PreverAtrasoResponse(BaseModel):
    atrasado: bool
    probabilidade: float


class BuscarAvaliacoesRequest(BaseModel):
    query: str
    n_resultados: int = 5
    filtro_nota_minima: float | None = None


class InsightsRequest(BaseModel):
    query: str = "atraso entrega qualidade"
    n_reviews: int = 10


# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok", "modelo_carregado": "pipeline" in estado}


@app.get("/metricas")
def metricas():
    df_pedidos = estado.get("df_pedidos")
    df_avaliacoes = estado.get("df_avaliacoes")
    if df_pedidos is None or df_avaliacoes is None:
        raise HTTPException(status_code=503, detail="Dados não inicializados")
    return calcular_metricas(df_pedidos, df_avaliacoes)


@app.post("/prever-atraso", response_model=PreverAtrasoResponse)
def prever_atraso(request: PreverAtrasoRequest):
    pipeline = estado.get("pipeline")
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    dados = pd.DataFrame([request.model_dump()])
    features = dados[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]

    probabilidade = float(pipeline.predict_proba(features)[0][1])
    atrasado = pipeline.predict(features)[0] == 1

    return PreverAtrasoResponse(atrasado=atrasado, probabilidade=round(probabilidade, 4))


@app.post("/buscar-avaliacoes")
def buscar_avaliacoes(request: BuscarAvaliacoesRequest):
    colecao = estado.get("colecao")
    if colecao is None:
        raise HTTPException(status_code=503, detail="ChromaDB não inicializado")

    resultados = buscar(
        colecao,
        query=request.query,
        n_resultados=request.n_resultados,
        filtro_nota_minima=request.filtro_nota_minima,
    )
    return {"resultados": resultados}


@app.post("/insights")
def gerar_insights(request: InsightsRequest):
    colecao = estado.get("colecao")
    df_pedidos = estado.get("df_pedidos")
    df_avaliacoes = estado.get("df_avaliacoes")

    if any(v is None for v in [colecao, df_pedidos, df_avaliacoes]):
        raise HTTPException(status_code=503, detail="Serviços não inicializados")

    metricas = calcular_metricas(df_pedidos, df_avaliacoes)
    reviews = buscar(colecao, query=request.query, n_resultados=request.n_reviews)

    return StreamingResponse(
        gerar_insights_stream(metricas, reviews),
        media_type="text/plain; charset=utf-8",
    )
