from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


_BASE = Path(__file__).parent
_DATA = _BASE.parent.parent.parent / "data"
_GRAFICOS = _BASE.parent / "graficos"


df_pedidos = pd.read_csv(_DATA / "pedidos.csv")
df_restaurantes = pd.read_csv(_DATA / "restaurantes.csv")
df_avaliacoes = pd.read_csv(_DATA / "avaliacoes.csv")


print(f"Pedidos carregados:      {len(df_pedidos):>5} linhas")
print(f"Restaurantes carregados: {len(df_restaurantes):>5} linhas")
print(f"Avaliações carregadas:   {len(df_avaliacoes):>5} linhas")


print("\nMétricas gerais:\n")


valor_medio_pedido = df_pedidos["valor_pedido"].mean()

quantidade_total_pedidos = len(df_pedidos)
quantidade_pedidos_atrasados = df_pedidos["atrasado"].sum()

percentual_pedidos_atrasados = (
    quantidade_pedidos_atrasados / quantidade_total_pedidos
) * 100

tempo_medio_entrega = df_pedidos["tempo_total_minutos"].mean()
nota_media_geral = df_avaliacoes["nota"].mean()


print(f"Ticket médio por pedido: R$ {valor_medio_pedido:.2f}")

print(
    f"Pedidos atrasados: {quantidade_pedidos_atrasados} "
    f"de {quantidade_total_pedidos} "
    f"({percentual_pedidos_atrasados:.1f}%)"
)

print(f"Tempo médio de entrega: {tempo_medio_entrega:.1f} min")
print(f"Nota média geral: {nota_media_geral:.2f} de 5.0")


print("\nMétricas por dia da semana:\n")


ordem_dias_semana = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo",
]

quantidade_pedidos_por_dia = (
    df_pedidos
    .groupby("dia_semana")
    .size()
    .reindex(ordem_dias_semana)
    .rename_axis(None)
)

print(quantidade_pedidos_por_dia.to_string())


print("\nMétricas por clima:\n")


percentual_atraso_por_clima = (
    df_pedidos
    .groupby("clima")["atrasado"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

for clima, percentual_atraso in percentual_atraso_por_clima.items():
    print(f"{clima:<15} {percentual_atraso:.1f}% atrasados")


print("\nTop 5 restaurantes por nota média:\n")


df_avaliacoes_com_restaurante = df_avaliacoes.merge(
    df_restaurantes[["id_restaurante", "nome_restaurante"]],
    on="id_restaurante"
)

top_5_restaurantes_por_nota = (
    df_avaliacoes_com_restaurante
    .groupby("nome_restaurante")["nota"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

for nome_restaurante, nota_media_restaurante in top_5_restaurantes_por_nota.items():
    print(f"{nome_restaurante:<35} {nota_media_restaurante:.2f}")


_GRAFICOS.mkdir(parents=True, exist_ok=True)


fig, ax = plt.subplots(figsize=(8, 4))

quantidade_pedidos_por_dia.plot(
    kind="bar",
    ax=ax,
    color="steelblue",
    edgecolor="white"
)

ax.set_title("Pedidos por dia da semana")
ax.set_xlabel("Dia")
ax.set_ylabel("Quantidade de pedidos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

plt.tight_layout()
plt.savefig(_GRAFICOS / "pedidos_por_dia.png")
plt.close()
print()

print(f"Gráfico de pedidos por dia da semana gerado e salvo em: {_GRAFICOS / 'pedidos_por_dia.png'}")


fig, ax = plt.subplots(figsize=(6, 4))

cores_barras_clima = [
    "#e74c3c" if percentual > 50 else "#3498db"
    for percentual in percentual_atraso_por_clima.values
]

percentual_atraso_por_clima.plot(
    kind="bar",
    ax=ax,
    color=cores_barras_clima,
    edgecolor="white"
)

ax.set_title("% de pedidos atrasados por clima")
ax.set_xlabel("Clima")
ax.set_ylabel("% Atrasados")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig(_GRAFICOS / "atraso_por_clima.png")
plt.close()

print(f"Gráfico de atraso por clima gerado e salvo em: {_GRAFICOS / 'atraso_por_clima.png'}")


fig, ax = plt.subplots(figsize=(8, 4))

top_5_restaurantes_por_nota.sort_values().plot(
    kind="barh",
    ax=ax,
    color="coral",
    edgecolor="white"
)

ax.set_title("Top 5 restaurantes por nota média")
ax.set_xlabel("Nota média")
ax.set_ylabel("Restaurante")

plt.tight_layout()
plt.savefig(_GRAFICOS / "top5_restaurantes.png")
plt.close()

print(f"Gráfico de top 5 restaurantes gerado e salvo em: {_GRAFICOS / 'top5_restaurantes.png'}")
print()


tempo_medio_por_dia = (
    df_pedidos
    .groupby("dia_semana")["tempo_total_minutos"]
    .mean()
    .reindex(ordem_dias_semana)
    .rename_axis(None)
    .round(1)
)

fig, ax = plt.subplots(figsize=(8, 4))

tempo_medio_por_dia.plot(
    kind="line",
    ax=ax,
    color="darkorange",
    marker="o",
)

ax.fill_between(range(len(tempo_medio_por_dia)), tempo_medio_por_dia.values, alpha=0.1, color="darkorange")
ax.set_title("Tempo médio de entrega por dia (min)")
ax.set_xlabel("Dia")
ax.set_ylabel("Minutos")
ax.set_xticks(range(len(ordem_dias_semana)))
ax.set_xticklabels(ordem_dias_semana, rotation=30, ha="right")

plt.tight_layout()
plt.savefig(_GRAFICOS / "tempo_medio_por_dia.png")
plt.close()

print(f"Gráfico de tempo médio por dia gerado e salvo em: {_GRAFICOS / 'tempo_medio_por_dia.png'}")
