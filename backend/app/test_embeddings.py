import pandas as pd
import pytest
import chromadb

from embeddings import (
    buscar,
    carregar_avaliacoes,
    criar_colecao,
    criar_funcao_embedding,
    popular_colecao,
)


@pytest.fixture(scope="module")
def funcao_embedding():
    return criar_funcao_embedding()


@pytest.fixture
def client():
    return chromadb.EphemeralClient()


@pytest.fixture
def colecao(client, funcao_embedding):
    return criar_colecao(client, funcao_embedding)


@pytest.fixture
def df_avaliacoes_fake():
    return pd.DataFrame({
        "id_avaliacao":   [1, 2, 3, 4, 5],
        "id_pedido":      [10, 11, 12, 13, 14],
        "id_restaurante": [1, 1, 2, 2, 3],
        "nota":           [5, 2, 4, 1, 5],
        "nome_restaurante": [
            "Restaurante A", "Restaurante A",
            "Restaurante B", "Restaurante B",
            "Restaurante C",
        ],
        "comentario": [
            "Comida excelente e entrega rápida",
            "Pedido chegou frio e atrasado",
            "Ótimo atendimento, recomendo muito",
            "Embalagem aberta e item errado no pedido",
            "Melhor restaurante da cidade, sempre perfeito",
        ],
    })


def test_criar_colecao_retorna_collection(colecao):
    assert isinstance(colecao, chromadb.Collection)


def test_colecao_usa_distancia_cosine(colecao):
    assert colecao.metadata["hnsw:space"] == "cosine"


def test_popular_colecao_insere_documentos(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    assert colecao.count() == 5


def test_popular_colecao_nao_duplica(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    popular_colecao(colecao, df_avaliacoes_fake)
    assert colecao.count() == 5


def test_buscar_retorna_n_resultados(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    resultados = buscar(colecao, "entrega atrasada", n_resultados=3)
    assert len(resultados) == 3


def test_buscar_retorna_campos_corretos(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    resultados = buscar(colecao, "comida boa", n_resultados=1)
    item = resultados[0]
    assert "comentario" in item
    assert "nota" in item
    assert "restaurante" in item
    assert "similaridade" in item


def test_buscar_similaridade_entre_zero_e_um(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    resultados = buscar(colecao, "pedido errado", n_resultados=5)
    for item in resultados:
        assert 0.0 <= item["similaridade"] <= 1.0


def test_buscar_resultado_mais_similar_relevante(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    resultados = buscar(colecao, "pedido chegou frio e atrasado", n_resultados=1)
    assert "frio" in resultados[0]["comentario"].lower() or "atrasado" in resultados[0]["comentario"].lower()


def test_buscar_filtro_nota_minima(colecao, df_avaliacoes_fake):
    popular_colecao(colecao, df_avaliacoes_fake)
    resultados = buscar(colecao, "restaurante", n_resultados=5, filtro_nota_minima=4.0)
    for item in resultados:
        assert item["nota"] >= 4.0


def test_carregar_avaliacoes_remove_comentarios_vazios(tmp_path):
    df_aval = pd.DataFrame({
        "id_avaliacao":   [1, 2, 3],
        "id_pedido":      [10, 11, 12],
        "id_restaurante": [1, 1, 2],
        "nota":           [5, 3, 4],
        "comentario":     ["Ótimo!", "", None],
    })
    df_rest = pd.DataFrame({
        "id_restaurante":  [1, 2],
        "nome_restaurante": ["Restaurante A", "Restaurante B"],
    })

    caminho_aval = tmp_path / "avaliacoes.csv"
    caminho_rest = tmp_path / "restaurantes.csv"
    df_aval.to_csv(caminho_aval, index=False)
    df_rest.to_csv(caminho_rest, index=False)

    df = carregar_avaliacoes(str(caminho_aval), str(caminho_rest))
    assert len(df) == 1
    assert df.iloc[0]["comentario"] == "Ótimo!"
