import os

import pandas as pd
from fastapi import APIRouter, HTTPException

from models.schemas import (
    BuscarAvaliacoesRequest,
    InsightsRequest,
    PreverAtrasoRequest,
    PreverAtrasoResponse,
)
from rag.embeddings import buscar
from services.insights import gerar_insights as _gerar_insights
from services.metricas import (
    FEATURES_CATEGORICAS,
    FEATURES_NUMERICAS,
    calcular_metricas,
)
from state import estado

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "modelo_carregado": "pipeline" in estado}


@router.get("/defaults")
def defaults():
    df = estado.get("df_pedidos")
    if df is None:
        raise HTTPException(status_code=503, detail="Dados não inicializados")

    def _moda(col: str, fallback):
        if col not in df.columns:
            return fallback
        s = df[col].dropna()
        return s.mode().iloc[0] if not s.empty else fallback

    def _mediana(col: str, fallback: float) -> float:
        if col not in df.columns:
            return fallback
        s = df[col].dropna()
        return float(round(s.median(), 2)) if not s.empty else fallback

    return {
        "valor_pedido": _mediana("valor_pedido", 45.0),
        "quantidade_itens": int(_mediana("quantidade_itens", 3)),
        "tempo_preparo_minutos": _mediana("tempo_preparo_minutos", 20.0),
        "tempo_estimado_minutos": _mediana("tempo_estimado_minutos", 35.0),
        "distancia_km": _mediana("distancia_km", 3.0),
        "hora": int(_mediana("hora", 19)),
        "clima": str(_moda("clima", "Sol")),
        "dia_semana": str(_moda("dia_semana", "Sexta")),
    }


@router.get("/metricas")
def metricas():
    df_pedidos = estado.get("df_pedidos")
    df_avaliacoes = estado.get("df_avaliacoes")
    if df_pedidos is None or df_avaliacoes is None:
        raise HTTPException(status_code=503, detail="Dados não inicializados")
    return calcular_metricas(df_pedidos, df_avaliacoes)


@router.post("/prever-atraso", response_model=PreverAtrasoResponse)
def prever_atraso(request: PreverAtrasoRequest):
    pipeline = estado.get("pipeline")
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    dados = pd.DataFrame([request.model_dump()])
    features = dados[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]

    probabilidade = float(pipeline.predict_proba(features)[0][1])
    atrasado = pipeline.predict(features)[0] == 1

    return PreverAtrasoResponse(atrasado=atrasado, probabilidade=round(probabilidade, 4))


@router.post("/buscar-avaliacoes")
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


@router.post("/insights")
def gerar_insights(request: InsightsRequest):
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY não configurada")

    colecao = estado.get("colecao")
    df_pedidos = estado.get("df_pedidos")
    df_avaliacoes = estado.get("df_avaliacoes")

    if any(v is None for v in [colecao, df_pedidos, df_avaliacoes]):
        raise HTTPException(status_code=503, detail="Serviços não inicializados")

    metricas = calcular_metricas(df_pedidos, df_avaliacoes)
    reviews = buscar(colecao, query=request.query, n_resultados=request.n_reviews)

    return {"texto": _gerar_insights(metricas, reviews)}
