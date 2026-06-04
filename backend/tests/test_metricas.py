import pandas as pd
import pytest

from services.metricas import calcular_metricas


@pytest.fixture
def pedidos():
    return pd.DataFrame({
        "valor_pedido":        [50.0, 30.0, 20.0, 100.0],
        "atrasado":            [1,    0,    1,    0],
        "tempo_total_minutos": [40,   20,   60,   30],
        "dia_semana":          ["Segunda", "Sexta", "Segunda", "Sábado"],
        "clima":               ["Chuvoso", "Ensolarado", "Chuvoso", "Nublado"],
        "id_restaurante":      [1, 2, 1, 3],
    })


@pytest.fixture
def avaliacoes():
    return pd.DataFrame({
        "nota":           [5, 4, 3, 4, 2, 5],
        "id_restaurante": [1, 1, 2, 2, 3, 3],
    })


@pytest.fixture
def restaurantes():
    return pd.DataFrame({
        "id_restaurante":  [1, 2, 3],
        "nome_restaurante": ["Restaurante A", "Restaurante B", "Restaurante C"],
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
    assert nota_media == pytest.approx(23 / 6)


def test_ticket_medio_pedido_unico():
    df = pd.DataFrame({"valor_pedido": [75.0]})
    assert df["valor_pedido"].mean() == pytest.approx(75.0)


def test_percentual_atraso_zero():
    df = pd.DataFrame({"atrasado": [0, 0, 0]})
    assert (df["atrasado"].sum() / len(df)) * 100 == pytest.approx(0.0)


def test_percentual_atraso_total():
    df = pd.DataFrame({"atrasado": [1, 1, 1]})
    assert (df["atrasado"].sum() / len(df)) * 100 == pytest.approx(100.0)


def test_pedidos_por_dia(pedidos):
    ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    resultado = pedidos.groupby("dia_semana").size().reindex(ordem)
    assert resultado["Segunda"] == 2
    assert resultado["Sexta"] == 1
    assert resultado["Sábado"] == 1
    assert resultado.fillna(0)["Terça"] == 0


def test_atraso_por_clima(pedidos):
    resultado = (
        pedidos
        .groupby("clima")["atrasado"]
        .mean()
        .mul(100)
    )
    assert resultado["Chuvoso"] == pytest.approx(100.0)
    assert resultado["Ensolarado"] == pytest.approx(0.0)
    assert resultado["Nublado"] == pytest.approx(0.0)


def test_atraso_por_clima_ordenado_decrescente(pedidos, avaliacoes):
    resultado = calcular_metricas(pedidos, avaliacoes)
    valores = list(resultado["atraso_por_clima"].values())
    assert valores == sorted(valores, reverse=True)


def test_top5_restaurantes(avaliacoes, restaurantes):
    df = avaliacoes.merge(restaurantes, on="id_restaurante")
    top5 = (
        df.groupby("nome_restaurante")["nota"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )
    assert top5.index[0] == "Restaurante A"
    assert top5["Restaurante A"] == pytest.approx(4.5)
    assert top5["Restaurante B"] == pytest.approx(3.5)
    assert top5["Restaurante C"] == pytest.approx(3.5)
