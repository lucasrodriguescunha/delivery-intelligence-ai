from collections.abc import Generator

import openai

MODELO = "gpt-4o"

SYSTEM_PROMPT = """Você é um analista sênior de operações de delivery.
Recebe métricas operacionais e avaliações de clientes recuperadas por busca semântica.
Gera recomendações práticas, objetivas e priorizadas por impacto no negócio.

Estruture a resposta em três seções:

## Diagnóstico
Principais problemas identificados com base nos dados.

## Recomendações
Ações concretas priorizadas por impacto. Para cada uma, indique o problema que resolve
e o resultado esperado.

## Alertas
Pontos críticos que exigem atenção imediata.

Seja direto. Use os números das métricas e os comentários dos clientes para justificar
cada ponto. Evite generalizações sem respaldo nos dados fornecidos."""


def _formatar_metricas(metricas: dict) -> str:
    linhas = []
    for chave, valor in metricas.items():
        if isinstance(valor, float):
            linhas.append(f"- {chave}: {valor:.2f}")
        else:
            linhas.append(f"- {chave}: {valor}")
    return "\n".join(linhas)


def _formatar_reviews(reviews: list[dict]) -> str:
    return "\n".join(
        f"- [{item['nota']:.0f}/5] {item['restaurante']}: \"{item['comentario']}\""
        for item in reviews
    )


def gerar_insights_stream(
    metricas: dict,
    reviews: list[dict],
) -> Generator[str, None, None]:
    client = openai.OpenAI()

    mensagem_usuario = f"""## Métricas operacionais

{_formatar_metricas(metricas)}

## Avaliações de clientes (busca semântica — mais relevantes para o contexto)

{_formatar_reviews(reviews)}

Gere o diagnóstico, recomendações e alertas operacionais com base nesses dados."""

    stream = client.chat.completions.create(
        model=MODELO,
        max_tokens=4096,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": mensagem_usuario},
        ],
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
