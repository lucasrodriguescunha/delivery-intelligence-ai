# LLM Insights

Módulo de geração de insights operacionais via OpenAI GPT-4o com streaming de resposta.

## Arquivo

`backend/app/services/insights.py`

## Como funciona

Combina métricas operacionais calculadas sobre os dados de pedidos com avaliações de clientes recuperadas por busca semântica (RAG). O resultado é enviado ao GPT-4o que retorna uma análise estruturada em streaming.

### Fluxo

```
métricas dos pedidos (calcular_metricas em main.py)
    +
avaliações relevantes (busca semântica no ChromaDB)
    └── GPT-4o (gpt-4o)
        └── StreamingResponse → cliente
```

### Estrutura do prompt

O system prompt instrui o modelo a agir como analista sênior de operações de delivery e estruturar a resposta em três seções:

- **Diagnóstico** — problemas identificados nos dados
- **Recomendações** — ações priorizadas por impacto com resultado esperado
- **Alertas** — pontos críticos que exigem atenção imediata

### Métricas enviadas ao modelo

Calculadas em `services/metricas.py::calcular_metricas()`:

| Métrica | Descrição |
|---|---|
| `ticket_medio_R$` | Valor médio dos pedidos |
| `total_pedidos` | Total de pedidos no dataset |
| `pedidos_atrasados` | Contagem de atrasos |
| `percentual_atraso_%` | % de pedidos atrasados |
| `tempo_medio_entrega_min` | Tempo médio total de entrega |
| `nota_media_geral` | Média das notas dos clientes |
| `clima_maior_atraso` | Clima com maior taxa de atraso |
| `dia_maior_volume` | Dia da semana com mais pedidos |
| `pedidos_por_dia` | Volume de pedidos por dia da semana |
| `atraso_por_clima` | % de atraso por condição climática |
| `tempo_por_dia` | Tempo médio de entrega por dia da semana |

## Configuração

Requer `OPENAI_API_KEY`. Formas de configurar:

```bash
# Opção 1 — arquivo .env (recomendado)
cp backend/.env.example backend/.env
# editar backend/.env e preencher OPENAI_API_KEY=sk-...

# Opção 2 — variável de ambiente
export OPENAI_API_KEY="sk-..."
```

Se a chave não estiver configurada, o endpoint `/insights` retorna **503** com mensagem `OPENAI_API_KEY não configurada`.

Modelo configurável em `services/insights.py`:

```python
MODELO = "gpt-4o"  # Troque por gpt-4-turbo, gpt-4.1, etc.
```

## Como testar isoladamente

```python
from services.insights import gerar_insights_stream

metricas = {
    "ticket_medio_R$": 45.50,
    "total_pedidos": 1000,
    "pedidos_atrasados": 230,
    "percentual_atraso_%": 23.0,
    "tempo_medio_entrega_min": 42.5,
    "nota_media_geral": 3.8,
    "clima_maior_atraso": "Chuva",
    "dia_maior_volume": "Sábado",
}

reviews = [
    {"nota": 2.0, "restaurante": "Restaurante X", "comentario": "Chegou frio e atrasado"},
]

for chunk in gerar_insights_stream(metricas, reviews):
    print(chunk, end="", flush=True)
```

## Dependências

```
openai>=1.0.0
python-dotenv>=1.0.0
```
