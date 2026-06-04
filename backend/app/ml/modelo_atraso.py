from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


_BASE = Path(__file__).parent
_DATA = _BASE.parent.parent.parent / "data"
_GRAFICOS = _BASE.parent / "graficos"

FEATURES_NUMERICAS = [
    "valor_pedido",
    "quantidade_itens",
    "tempo_preparo_minutos",
    "tempo_estimado_minutos",
    "distancia_km",
    "hora",
]

FEATURES_CATEGORICAS = [
    "clima",
    "dia_semana",
]

TARGET = "atrasado"

CAMINHO_MODELO = str(_BASE / "modelo_atraso.joblib")


def carregar_dados(caminho_csv: str | None = None) -> pd.DataFrame:
    caminho_csv = caminho_csv or str(_DATA / "pedidos.csv")
    df = pd.read_csv(caminho_csv)
    colunas_necessarias = FEATURES_NUMERICAS + FEATURES_CATEGORICAS + [TARGET]
    return df[colunas_necessarias]


def construir_pipeline() -> Pipeline:
    preprocessador = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURES_NUMERICAS),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                FEATURES_CATEGORICAS,
            ),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessador", preprocessador),
            ("modelo", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )


def avaliar_modelo(pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    print("\nRelatório de classificação:\n")
    print(classification_report(y_test, y_pred, target_names=["No prazo", "Atrasado"]))

    auc = roc_auc_score(y_test, y_proba)
    print(f"AUC-ROC: {auc:.4f}")

    _GRAFICOS.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_estimator(
        pipeline,
        X_test,
        y_test,
        display_labels=["No prazo", "Atrasado"],
        ax=ax,
        colorbar=False,
    )
    ax.set_title("Matriz de confusão — Modelo de atraso")
    plt.tight_layout()
    plt.savefig(_GRAFICOS / "matriz_confusao.png")
    plt.close()

    print(f"\nMatriz de confusão salva em: {_GRAFICOS / 'matriz_confusao.png'}")


def salvar_modelo(pipeline: Pipeline) -> None:
    joblib.dump(pipeline, CAMINHO_MODELO)
    print(f"\nModelo salvo em: {CAMINHO_MODELO}")


def treinar(caminho_csv: str | None = None) -> Pipeline:
    df = carregar_dados(caminho_csv)

    X = df[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Treino: {len(X_train)} amostras | Teste: {len(X_test)} amostras")
    print(f"Taxa de atraso no treino: {y_train.mean():.1%}")

    pipeline = construir_pipeline()
    pipeline.fit(X_train, y_train)

    avaliar_modelo(pipeline, X_test, y_test)
    salvar_modelo(pipeline)

    return pipeline


if __name__ == "__main__":
    treinar()
    print()
