import pandas as pd
import pytest


@pytest.fixture
def pedidos():
    return pd.DataFrame({
        "valor_pedido": [50.0, 30.0, 20.0, 100.0],
        "atrasado":     [1,    0,    1,    0],
        "tempo_total_minutos": [40, 20, 60, 30],
    })


@pytest.fixture
def avaliacoes():
    return pd.DataFrame({
        "nota": [5, 4, 3, 4],
    })


def test_ticket_medio(pedidos):
    ticket_medio = pedidos["valor_pedido"].mean()
    assert ticket_medio == pytest.approx(50.0)


def test_percentual_atraso(pedidos):
    total = len(pedidos)
    atrasados = pedidos["atrasado"].sum()
    percentual = (atrasados / total) * 100
    assert percentual == pytest.approx(50.0)


def test_tempo_medio_entrega(pedidos):
    tempo_medio = pedidos["tempo_total_minutos"].mean()
    assert tempo_medio == pytest.approx(37.5)


def test_nota_media(avaliacoes):
    nota_media = avaliacoes["nota"].mean()
    assert nota_media == pytest.approx(4.0)


def test_ticket_medio_pedido_unico():
    df = pd.DataFrame({"valor_pedido": [75.0]})
    assert df["valor_pedido"].mean() == pytest.approx(75.0)


def test_percentual_atraso_zero():
    df = pd.DataFrame({"atrasado": [0, 0, 0]})
    assert (df["atrasado"].sum() / len(df)) * 100 == pytest.approx(0.0)


def test_percentual_atraso_total():
    df = pd.DataFrame({"atrasado": [1, 1, 1]})
    assert (df["atrasado"].sum() / len(df)) * 100 == pytest.approx(100.0)
