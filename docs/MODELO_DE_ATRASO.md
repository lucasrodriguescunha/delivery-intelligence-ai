# Modelo de Atraso

Módulo de machine learning que treina e serve um classificador binário para prever se um pedido será entregue com atraso.

## Arquivo

`backend/app/ml/modelo_atraso.py`

## Como funciona

O modelo usa **Regressão Logística** dentro de um pipeline scikit-learn com pré-processamento automático de features numéricas e categóricas.

### Features de entrada

| Feature | Tipo | Descrição |
|---|---|---|
| `valor_pedido` | float | Valor total do pedido em R$ |
| `quantidade_itens` | int | Número de itens no pedido |
| `tempo_preparo_minutos` | float | Tempo estimado de preparo |
| `tempo_estimado_minutos` | float | Tempo estimado total de entrega |
| `distancia_km` | float | Distância entre restaurante e destino |
| `hora` | int | Hora do pedido (0–23) |
| `clima` | string | Condição climática (ex: "Chuva", "Sol") |
| `dia_semana` | string | Dia da semana (ex: "Segunda", "Sábado") |

### Target

`atrasado` — binário: `1` (atrasado) ou `0` (no prazo)

### Pipeline

```
pedidos.csv
    └── StandardScaler (features numéricas)
    └── OneHotEncoder (features categóricas)
        └── LogisticRegression(max_iter=1000, random_state=42)
            └── ml/modelo_atraso.joblib
```

## Como treinar

```bash
cd backend/app
python ml/modelo_atraso.py
```

Saída esperada:
- Relatório de classificação no terminal
- AUC-ROC score
- Imagem `graficos/matriz_confusao.png`
- Arquivo `ml/modelo_atraso.joblib`

## Como avaliar

A função `avaliar_modelo()` gera automaticamente:

- `classification_report` com precision, recall e F1 para cada classe
- AUC-ROC para medir separabilidade entre classes
- Matriz de confusão salva em `graficos/matriz_confusao.png`

## Dependências

```
scikit-learn>=1.5.0
pandas>=3.0.2
matplotlib>=3.10.9
joblib>=1.4.0
```

## Dados necessários

`data/pedidos.csv` com as colunas listadas acima mais `atrasado` e `tempo_total_minutos`.
