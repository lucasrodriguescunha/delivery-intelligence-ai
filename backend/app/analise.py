import os

import pandas as pd
import matplotlib.pyplot as plt


# Carrega os dados
df_pedidos = pd.read_csv("../../data/pedidos.csv")
df_restaurantes = pd.read_csv("../../data/restaurantes.csv")
df_avaliacoes = pd.read_csv("../../data/avaliacoes.csv")


print(f"Pedidos carregados:      {len(df_pedidos):>5} linhas")
print(f"Restaurantes carregados: {len(df_restaurantes):>5} linhas")
print(f"Avaliações carregadas:   {len(df_avaliacoes):>5} linhas")


print("\nMétricas gerais:\n")


# Calcula indicadores gerais dos pedidos e avaliações
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


# Conta os pedidos por dia da semana na ordem correta
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


# Calcula o percentual de atraso por clima
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


# Relaciona avaliações aos restaurantes e calcula os melhores por nota média
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


# Cria a pasta onde os gráficos serão salvos
os.makedirs("graficos", exist_ok=True)


# Gráfico 1: quantidade de pedidos por dia da semana
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
plt.savefig("graficos/pedidos_por_dia.png")
plt.close()
print()

print("Gráfico de pedidos por dia da semana gerado e salvo em: graficos/pedidos_por_dia_da_semana.png")


# Gráfico 2: percentual de pedidos atrasados por clima
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

ax.set_title("% de Pedidos atrasados por clima")
ax.set_xlabel("Clima")
ax.set_ylabel("% Atrasados")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("graficos/atraso_por_clima.png")
plt.close()

print("Gráfico de atraso por clima gerado e salvo em: graficos/atraso_por_clima.png")


# Gráfico 3: top 5 restaurantes por nota média
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
plt.savefig("graficos/top5_restaurantes.png")
plt.close()

print("Gráfico de top 5 restaurantes gerado e salvo em: graficos/top5_restaurantes.png")
print()