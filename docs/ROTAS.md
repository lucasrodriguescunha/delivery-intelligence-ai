# Rotas da API

API REST construída com FastAPI. Base URL: `http://localhost:8000`

Documentação interativa disponível em `http://localhost:8000/docs` (Swagger UI).

---

## GET `/health`

Verifica se a API está no ar e o modelo carregado.

**Resposta**

```json
{
  "status": "ok",
  "modelo_carregado": true
}
```

---

## POST `/prever-atraso`

Prevê se um pedido será entregue com atraso usando o modelo de Regressão Logística.

**Request body**

```json
{
  "valor_pedido": 52.90,
  "quantidade_itens": 3,
  "tempo_preparo_minutos": 20.0,
  "tempo_estimado_minutos": 45.0,
  "distancia_km": 4.2,
  "hora": 19,
  "clima": "Chuva",
  "dia_semana": "Sexta"
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `valor_pedido` | float | Valor total em R$ |
| `quantidade_itens` | int | Número de itens |
| `tempo_preparo_minutos` | float | Tempo de preparo estimado |
| `tempo_estimado_minutos` | float | Tempo total estimado |
| `distancia_km` | float | Distância em km |
| `hora` | int | Hora do pedido (0–23) |
| `clima` | string | Condição climática |
| `dia_semana` | string | Dia da semana em português |

**Resposta**

```json
{
  "atrasado": true,
  "probabilidade": 0.7821
}
```

**Erros**

| Status | Motivo |
|---|---|
| `503` | Modelo não carregado (falta `models/modelo_atraso.joblib`) |

---

## POST `/buscar-avaliacoes`

Busca avaliações de clientes por similaridade semântica usando ChromaDB.

**Request body**

```json
{
  "query": "entrega demorada e comida fria",
  "n_resultados": 5,
  "filtro_nota_minima": 1.0
}
```

| Campo | Tipo | Padrão | Descrição |
|---|---|---|---|
| `query` | string | — | Texto de busca em linguagem natural |
| `n_resultados` | int | `5` | Quantidade de resultados |
| `filtro_nota_minima` | float \| null | `null` | Filtra avaliações com nota >= valor |

**Resposta**

```json
{
  "resultados": [
    {
      "comentario": "Chegou frio e uma hora atrasado.",
      "nota": 1.0,
      "restaurante": "Pizzaria Central",
      "similaridade": 0.9134
    }
  ]
}
```

**Erros**

| Status | Motivo |
|---|---|
| `503` | ChromaDB não inicializado |

---

## POST `/insights`

Gera análise operacional em streaming combinando métricas e avaliações via GPT-4o.

**Request body**

```json
{
  "query": "atraso entrega qualidade",
  "n_reviews": 10
}
```

| Campo | Tipo | Padrão | Descrição |
|---|---|---|---|
| `query` | string | `"atraso entrega qualidade"` | Query para busca semântica de avaliações |
| `n_reviews` | int | `10` | Número de avaliações enviadas ao modelo |

**Resposta**

`text/plain; charset=utf-8` em streaming com três seções:

```
## Diagnóstico
...

## Recomendações
...

## Alertas
...
```

**Erros**

| Status | Motivo |
|---|---|
| `503` | ChromaDB, dados de pedidos ou avaliações não inicializados |

---

## Exemplo com curl

```bash
# Health check
curl http://localhost:8000/health

# Prever atraso
curl -X POST http://localhost:8000/prever-atraso \
  -H "Content-Type: application/json" \
  -d '{"valor_pedido":52.90,"quantidade_itens":3,"tempo_preparo_minutos":20,"tempo_estimado_minutos":45,"distancia_km":4.2,"hora":19,"clima":"Chuva","dia_semana":"Sexta"}'

# Buscar avaliações
curl -X POST http://localhost:8000/buscar-avaliacoes \
  -H "Content-Type: application/json" \
  -d '{"query":"entrega atrasada","n_resultados":3}'

# Insights em streaming
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{"query":"atraso chuva","n_reviews":10}'
```
