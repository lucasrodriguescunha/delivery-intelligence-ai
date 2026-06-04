# Embeddings e Busca Semântica

Módulo de busca semântica sobre avaliações de clientes usando ChromaDB e embeddings multilíngues.

## Arquivo

`backend/app/embeddings.py`

## Como funciona

Avaliações de clientes são convertidas em vetores numéricos (embeddings) e armazenadas no ChromaDB. Buscas por similaridade de cosseno permitem encontrar avaliações semanticamente próximas de uma query em linguagem natural.

### Modelo de embedding

**`paraphrase-multilingual-MiniLM-L12-v2`** (SentenceTransformers)

- Multilíngue — funciona bem com português
- Leve e rápido (dimensão 384)
- Download automático no primeiro uso via `sentence-transformers`

### Banco vetorial

**ChromaDB** persistente em `backend/app/chroma_db/`

- Coleção: `avaliacoes`
- Métrica de distância: cosseno
- Metadados armazenados por documento: `nota`, `id_restaurante`, `nome_restaurante`, `id_pedido`

## Dados necessários

| Arquivo | Colunas obrigatórias |
|---|---|
| `data/avaliacoes.csv` | `id_avaliacao`, `id_restaurante`, `id_pedido`, `nota`, `comentario` |
| `data/restaurantes.csv` | `id_restaurante`, `nome_restaurante` |

## Como inicializar e popular o banco

```bash
cd backend/app
python embeddings.py
```

Indexa todas as avaliações com comentário não nulo. Execuções subsequentes ignoram documentos já existentes (idempotente).

Saída esperada:
```
N avaliações indexadas.
```

Seguido de 3 buscas demo no terminal.

## Como buscar via código

```python
from embeddings import inicializar, buscar

_, colecao = inicializar()

resultados = buscar(
    colecao,
    query="entrega demorada e comida fria",
    n_resultados=5,
    filtro_nota_minima=None,  # ou float, ex: 4.0
)

for item in resultados:
    print(item["similaridade"], item["nota"], item["restaurante"])
    print(item["comentario"])
```

### Retorno de `buscar()`

Lista de dicts com:

| Campo | Tipo | Descrição |
|---|---|---|
| `comentario` | string | Texto da avaliação |
| `nota` | float | Nota de 1 a 5 |
| `restaurante` | string | Nome do restaurante |
| `similaridade` | float | Score 0–1 (1 = idêntico) |

## Dependências

```
chromadb>=0.5.0
sentence-transformers>=3.0.0
pandas>=3.0.2
```
