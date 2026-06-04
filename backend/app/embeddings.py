import os

import chromadb
import pandas as pd
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


MODELO_EMBEDDING = "paraphrase-multilingual-MiniLM-L12-v2"
NOME_COLECAO = "avaliacoes"
CAMINHO_CHROMA = "chroma_db"


def criar_funcao_embedding() -> SentenceTransformerEmbeddingFunction:
    return SentenceTransformerEmbeddingFunction(model_name=MODELO_EMBEDDING)


def criar_colecao(
    client: chromadb.ClientAPI,
    funcao_embedding: SentenceTransformerEmbeddingFunction,
) -> chromadb.Collection:
    return client.get_or_create_collection(
        name=NOME_COLECAO,
        embedding_function=funcao_embedding,
        metadata={"hnsw:space": "cosine"},
    )


def carregar_avaliacoes(
    caminho_avaliacoes: str,
    caminho_restaurantes: str,
) -> pd.DataFrame:
    df_avaliacoes = pd.read_csv(caminho_avaliacoes)
    df_restaurantes = pd.read_csv(caminho_restaurantes)

    df = df_avaliacoes.merge(
        df_restaurantes[["id_restaurante", "nome_restaurante"]],
        on="id_restaurante",
        how="left",
    )

    # Remove avaliações sem comentário
    df = df.dropna(subset=["comentario"])
    df = df[df["comentario"].str.strip() != ""]

    return df


def popular_colecao(
    colecao: chromadb.Collection,
    df: pd.DataFrame,
) -> None:
    ids = df["id_avaliacao"].astype(str).tolist()

    # Evita reinserir documentos já existentes
    existentes = set(colecao.get(ids=ids)["ids"])
    df_novos = df[~df["id_avaliacao"].astype(str).isin(existentes)]

    if df_novos.empty:
        print("Coleção já populada. Nenhum documento novo.")
        return

    documentos = df_novos["comentario"].tolist()
    ids_novos = df_novos["id_avaliacao"].astype(str).tolist()

    metadados = [
        {
            "nota": float(row["nota"]),
            "id_restaurante": int(row["id_restaurante"]),
            "nome_restaurante": str(row["nome_restaurante"]),
            "id_pedido": int(row["id_pedido"]),
        }
        for _, row in df_novos.iterrows()
    ]

    colecao.add(documents=documentos, ids=ids_novos, metadatas=metadados)
    print(f"{len(ids_novos)} avaliações indexadas.")


def buscar(
    colecao: chromadb.Collection,
    query: str,
    n_resultados: int = 5,
    filtro_nota_minima: float | None = None,
) -> list[dict]:
    where = {"nota": {"$gte": filtro_nota_minima}} if filtro_nota_minima else None

    resultado = colecao.query(
        query_texts=[query],
        n_results=n_resultados,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    itens = []
    for doc, meta, dist in zip(
        resultado["documents"][0],
        resultado["metadatas"][0],
        resultado["distances"][0],
    ):
        itens.append(
            {
                "comentario": doc,
                "nota": meta["nota"],
                "restaurante": meta["nome_restaurante"],
                "similaridade": round(1 - dist, 4),
            }
        )

    return itens


def exibir_resultados(resultados: list[dict]) -> None:
    for i, item in enumerate(resultados, 1):
        print(f"\n[{i}] Similaridade: {item['similaridade']:.4f} | Nota: {item['nota']:.0f}/5")
        print(f"    Restaurante: {item['restaurante']}")
        print(f"    Comentário: {item['comentario']}")


def inicializar(
    caminho_avaliacoes: str = "../../data/avaliacoes.csv",
    caminho_restaurantes: str = "../../data/restaurantes.csv",
    caminho_chroma: str = CAMINHO_CHROMA,
) -> tuple[chromadb.ClientAPI, chromadb.Collection]:
    funcao_embedding = criar_funcao_embedding()
    client = chromadb.PersistentClient(path=caminho_chroma)
    colecao = criar_colecao(client, funcao_embedding)

    df = carregar_avaliacoes(caminho_avaliacoes, caminho_restaurantes)
    popular_colecao(colecao, df)

    return client, colecao


if __name__ == "__main__":
    _, colecao = inicializar()

    queries_demo = [
        "entrega muito demorada e fria",
        "ótimo atendimento e comida deliciosa",
        "pedido errado e embalagem aberta",
    ]

    for query in queries_demo:
        print(f"\n{'='*60}")
        print(f"Busca: \"{query}\"")
        print('='*60)
        resultados = buscar(colecao, query, n_resultados=3)
        exibir_resultados(resultados)
