import os

import pandas as pd
import matplotlib.pyplot as plt


# Carrega os dados
df_pedidos = pd.read_csv("../../data/pedidos.csv")
df_restaurantes = pd.read_csv("../../data/restaurantes.csv")
df_avaliacoes = pd.read_csv("../../data/avaliacoes.csv")


print("Pedidos carregados:", len(df_pedidos), "linhas")
print("Restaurantes carregados:", len(df_restaurantes), "linhas")
print("Avaliações carregadas:", len(df_avaliacoes), "linhas")


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
    print(f"  {clima:<15} {percentual_atraso:.1f}% atrasados")


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
    print(f"  {nome_restaurante:<35} {nota_media_restaurante:.2f}")


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

ax.set_title("Pedidos por Dia da Semana")
ax.set_xlabel("Dia")
ax.set_ylabel("Quantidade de Pedidos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

plt.tight_layout()
plt.savefig("graficos/pedidos_por_dia.png")
plt.close()

print("Gráfico salvo: graficos/pedidos_por_dia.png")


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

ax.set_title("% de Pedidos Atrasados por Clima")
ax.set_xlabel("Clima")
ax.set_ylabel("% Atrasados")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("graficos/atraso_por_clima.png")
plt.close()

print("Gráfico salvo: graficos/atraso_por_clima.png")


# Gráfico 3: quantidade de avaliações por nota
fig, ax = plt.subplots(figsize=(6, 4))

quantidade_avaliacoes_por_nota = (
    df_avaliacoes["nota"]
    .value_counts()
    .sort_index()
)

quantidade_avaliacoes_por_nota.plot(
    kind="bar",
    ax=ax,
    color="gold",
    edgecolor="white"
)

ax.set_title("Distribuição das Notas")
ax.set_xlabel("Nota")
ax.set_ylabel("Quantidade de Avaliações")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("graficos/distribuicao_notas.png")
plt.close()

print("Gráfico salvo: graficos/distribuicao_notas.png")


# Gráfico 4: valor médio dos pedidos por tipo de culinária
df_pedidos_com_culinaria = df_pedidos.merge(
    df_restaurantes[["id_restaurante", "tipo_culinaria"]],
    on="id_restaurante"
)

valor_medio_pedido_por_culinaria = (
    df_pedidos_com_culinaria
    .groupby("tipo_culinaria")["valor_pedido"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(9, 4))

valor_medio_pedido_por_culinaria.plot(
    kind="bar",
    ax=ax,
    color="mediumseagreen",
    edgecolor="white"
)

ax.set_title("Ticket Médio por Tipo de Culinária")
ax.set_xlabel("Tipo de Culinária")
ax.set_ylabel("Valor Médio (R$)")
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")

plt.tight_layout()
plt.savefig("graficos/ticket_por_culinaria.png")
plt.close()

print("Gráfico salvo: graficos/ticket_por_culinaria.png")


print()
print("Análise concluída!")