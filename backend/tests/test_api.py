import sys
from contextlib import asynccontextmanager
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Stub módulos pesados antes de importar main.
# patch.dict remove "main" de sys.modules ao sair do contexto (não estava lá antes),
# então patch("main.buscar") reimportaria um módulo diferente sem os stubs.
# Registrar manualmente mantém a referência correta.
with patch.dict(
    "sys.modules",
    {
        "chromadb": MagicMock(),
        "joblib": MagicMock(),
        "embeddings": MagicMock(),
        "insights": MagicMock(),
    },
):
    import main as _main_mod

sys.modules["main"] = _main_mod
app = _main_mod.app
estado = _main_mod.estado


# Substitui lifespan real por noop — testes controlam estado manualmente
@asynccontextmanager
async def _lifespan_noop(app):
    yield


app.router.lifespan_context = _lifespan_noop


METRICAS_KEYS = {
    "ticket_medio_R$",
    "total_pedidos",
    "pedidos_atrasados",
    "percentual_atraso_%",
    "tempo_medio_entrega_min",
    "nota_media_geral",
    "clima_maior_atraso",
    "dia_maior_volume",
}


# --- Fixtures ---

PEDIDO_VALIDO = {
    "valor_pedido": 45.5,
    "quantidade_itens": 3,
    "tempo_preparo_minutos": 20.0,
    "tempo_estimado_minutos": 30.0,
    "distancia_km": 5.0,
    "hora": 12,
    "clima": "Ensolarado",
    "dia_semana": "Segunda",
}


@pytest.fixture()
def pipeline_mock():
    m = MagicMock()
    m.predict_proba.return_value = [[0.2, 0.8]]
    m.predict.return_value = [1]
    return m


@pytest.fixture()
def df_pedidos():
    return pd.DataFrame(
        {
            "valor_pedido": [30.0, 50.0],
            "quantidade_itens": [2, 4],
            "atrasado": [0, 1],
            "tempo_total_minutos": [25.0, 45.0],
            "clima": ["Ensolarado", "Tempestade"],
            "dia_semana": ["Segunda", "Sexta"],
        }
    )


@pytest.fixture()
def df_avaliacoes():
    return pd.DataFrame(
        {
            "nota": [4.0, 5.0],
            "id_restaurante": [1, 2],
            "comentario": ["bom", "ótimo"],
        }
    )


@pytest.fixture()
def client(pipeline_mock, df_pedidos, df_avaliacoes):
    estado["pipeline"] = pipeline_mock
    estado["colecao"] = MagicMock()
    estado["df_pedidos"] = df_pedidos
    estado["df_avaliacoes"] = df_avaliacoes
    with TestClient(app) as c:
        yield c
    estado.clear()


# --- /metricas ---

def test_metricas_retorna_200(client):
    assert client.get("/metricas").status_code == 200


def test_metricas_contem_todas_as_chaves(client):
    data = client.get("/metricas").json()
    assert METRICAS_KEYS == set(data.keys())


def test_metricas_total_pedidos(client):
    assert client.get("/metricas").json()["total_pedidos"] == 2


def test_metricas_pedidos_atrasados(client):
    assert client.get("/metricas").json()["pedidos_atrasados"] == 1


def test_metricas_percentual_atraso(client):
    assert client.get("/metricas").json()["percentual_atraso_%"] == pytest.approx(50.0)


def test_metricas_ticket_medio(client):
    assert client.get("/metricas").json()["ticket_medio_R$"] == pytest.approx(40.0)


def test_metricas_nota_media(client):
    assert client.get("/metricas").json()["nota_media_geral"] == pytest.approx(4.5)


def test_metricas_sem_dados_retorna_503():
    estado.clear()
    with TestClient(app) as c:
        assert c.get("/metricas").status_code == 503


# --- /health ---

def test_health_retorna_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_health_modelo_carregado(client):
    assert client.get("/health").json()["modelo_carregado"] is True


def test_health_sem_modelo_retorna_false():
    estado.clear()
    with TestClient(app) as c:
        assert c.get("/health").json()["modelo_carregado"] is False


# --- /prever-atraso ---

def test_prever_atraso_retorna_200(client):
    assert client.post("/prever-atraso", json=PEDIDO_VALIDO).status_code == 200


def test_prever_atraso_schema(client):
    data = client.post("/prever-atraso", json=PEDIDO_VALIDO).json()
    assert "atrasado" in data
    assert "probabilidade" in data


def test_prever_atraso_valores(client):
    data = client.post("/prever-atraso", json=PEDIDO_VALIDO).json()
    assert data["atrasado"] is True
    assert data["probabilidade"] == pytest.approx(0.8, abs=0.001)


def test_prever_atraso_sem_modelo_retorna_503():
    estado.clear()
    with TestClient(app) as c:
        assert c.post("/prever-atraso", json=PEDIDO_VALIDO).status_code == 503


def test_prever_atraso_campo_faltando_retorna_422(client):
    incompleto = {k: v for k, v in PEDIDO_VALIDO.items() if k != "clima"}
    assert client.post("/prever-atraso", json=incompleto).status_code == 422


# --- /buscar-avaliacoes ---

_RESULTADO_FAKE = [
    {"nota": 5, "comentario": "ótimo", "restaurante": "X", "similaridade": 0.9}
]


def test_buscar_avaliacoes_retorna_200(client):
    with patch("main.buscar", return_value=_RESULTADO_FAKE):
        assert client.post("/buscar-avaliacoes", json={"query": "entrega"}).status_code == 200


def test_buscar_avaliacoes_tem_chave_resultados(client):
    with patch("main.buscar", return_value=_RESULTADO_FAKE):
        resp = client.post("/buscar-avaliacoes", json={"query": "entrega"})
    assert "resultados" in resp.json()


def test_buscar_avaliacoes_sem_chroma_retorna_503():
    estado.clear()
    with TestClient(app) as c:
        assert c.post("/buscar-avaliacoes", json={"query": "teste"}).status_code == 503


def test_buscar_avaliacoes_repassa_filtro_nota(client):
    with patch("main.buscar", return_value=[]) as mock_buscar:
        resp = client.post(
            "/buscar-avaliacoes",
            json={"query": "bom", "filtro_nota_minima": 4.0},
        )
    assert resp.status_code == 200
    mock_buscar.assert_called_once()
    assert mock_buscar.call_args.kwargs.get("filtro_nota_minima") == 4.0


# --- /insights ---

def test_insights_retorna_200(client):
    with patch("main.buscar", return_value=[]), \
         patch("main._gerar_insights", return_value="insight gerado"), \
         patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        assert client.post("/insights", json={}).status_code == 200


def test_insights_sem_servicos_retorna_503():
    estado.clear()
    with TestClient(app) as c, patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        assert c.post("/insights", json={}).status_code == 503


def test_insights_sem_api_key_retorna_503(client):
    env_sem_key = {k: v for k, v in __import__("os").environ.items() if k != "OPENAI_API_KEY"}
    with patch.dict("os.environ", env_sem_key, clear=True):
        assert client.post("/insights", json={}).status_code == 503


def test_insights_retorna_texto(client):
    with patch("main.buscar", return_value=[]), \
         patch("main._gerar_insights", return_value="insight gerado"), \
         patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        resp = client.post("/insights", json={})
    assert resp.json()["texto"] == "insight gerado"
