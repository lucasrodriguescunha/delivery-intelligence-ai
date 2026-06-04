import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from modelo_atraso import (
    FEATURES_CATEGORICAS,
    FEATURES_NUMERICAS,
    TARGET,
    carregar_dados,
    construir_pipeline,
)


@pytest.fixture
def df_pedidos_fake():
    return pd.DataFrame({
        "valor_pedido":          [50.0, 30.0, 80.0, 20.0, 60.0],
        "quantidade_itens":      [2,    1,    3,    1,    2],
        "tempo_preparo_minutos": [15,   10,   20,   8,    12],
        "tempo_estimado_minutos":[40,   30,   50,   25,   35],
        "distancia_km":          [3.5,  1.2,  5.0,  0.8,  2.1],
        "hora":                  [12,   19,   21,   13,   20],
        "clima":                 ["Chuvoso", "Ensolarado", "Chuvoso", "Nublado", "Ensolarado"],
        "dia_semana":            ["Segunda", "Sexta", "Sábado", "Terça", "Domingo"],
        "atrasado":              [1, 0, 1, 0, 0],
    })


def test_construir_pipeline_retorna_pipeline():
    pipeline = construir_pipeline()
    assert isinstance(pipeline, Pipeline)


def test_pipeline_tem_preprocessador_e_modelo():
    pipeline = construir_pipeline()
    nomes = [nome for nome, _ in pipeline.steps]
    assert "preprocessador" in nomes
    assert "modelo" in nomes


def test_pipeline_treina_e_prediz(df_pedidos_fake):
    X = df_pedidos_fake[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]
    y = df_pedidos_fake[TARGET]

    pipeline = construir_pipeline()
    pipeline.fit(X, y)

    predicoes = pipeline.predict(X)
    assert len(predicoes) == len(y)
    assert set(predicoes).issubset({0, 1})


def test_pipeline_predict_proba(df_pedidos_fake):
    X = df_pedidos_fake[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]
    y = df_pedidos_fake[TARGET]

    pipeline = construir_pipeline()
    pipeline.fit(X, y)

    probabilidades = pipeline.predict_proba(X)
    assert probabilidades.shape == (len(y), 2)
    assert (probabilidades >= 0).all() and (probabilidades <= 1).all()


def test_carregar_dados_seleciona_colunas_corretas(tmp_path, df_pedidos_fake):
    df_com_extras = df_pedidos_fake.copy()
    df_com_extras["coluna_extra"] = 999
    df_com_extras["tempo_entrega_minutos"] = 25

    caminho = tmp_path / "pedidos.csv"
    df_com_extras.to_csv(caminho, index=False)

    df = carregar_dados(str(caminho))
    colunas_esperadas = set(FEATURES_NUMERICAS + FEATURES_CATEGORICAS + [TARGET])
    assert set(df.columns) == colunas_esperadas
    assert "coluna_extra" not in df.columns
    assert "tempo_entrega_minutos" not in df.columns


def test_carregar_dados_sem_linhas_nulas(tmp_path, df_pedidos_fake):
    caminho = tmp_path / "pedidos.csv"
    df_pedidos_fake.to_csv(caminho, index=False)

    df = carregar_dados(str(caminho))
    assert df.isnull().sum().sum() == 0


def test_pipeline_clima_desconhecido_nao_quebra(df_pedidos_fake):
    X_train = df_pedidos_fake[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]
    y_train = df_pedidos_fake[TARGET]

    pipeline = construir_pipeline()
    pipeline.fit(X_train, y_train)

    X_novo = X_train.copy()
    X_novo["clima"] = "Tempestade"
    predicoes = pipeline.predict(X_novo)
    assert len(predicoes) == len(X_novo)
