# Análise Exploratória

Script de análise e visualização dos dados operacionais de delivery.

## Arquivo

`backend/app/services/analise.py`

## O que faz

Carrega os três CSVs de dados, calcula métricas gerais e gera três gráficos salvos em `backend/app/graficos/`.

### Métricas calculadas

| Métrica | Descrição |
|---|---|
| Ticket médio | Valor médio por pedido em R$ |
| Pedidos atrasados | Contagem e percentual |
| Tempo médio de entrega | Em minutos |
| Nota média geral | Média das avaliações (escala 1–5) |
| Pedidos por dia da semana | Volume por dia |
| % atraso por clima | Taxa de atraso por condição climática |
| Top 5 restaurantes por nota | Melhores avaliados |

### Gráficos gerados

| Arquivo | Conteúdo |
|---|---|
| `graficos/pedidos_por_dia.png` | Barras com volume de pedidos por dia da semana |
| `graficos/atraso_por_clima.png` | Barras com % de atraso por clima (vermelho > 50%, azul ≤ 50%) |
| `graficos/top5_restaurantes.png` | Barras horizontais com top 5 restaurantes por nota média |

## Como executar

```bash
cd backend/app
python services/analise.py
```

## Dados necessários

| Arquivo | Colunas usadas |
|---|---|
| `data/pedidos.csv` | `valor_pedido`, `atrasado`, `tempo_total_minutos`, `dia_semana`, `clima` |
| `data/restaurantes.csv` | `id_restaurante`, `nome_restaurante` |
| `data/avaliacoes.csv` | `nota`, `id_restaurante` |

## Dependências

```
pandas>=3.0.2
matplotlib>=3.10.9
```
