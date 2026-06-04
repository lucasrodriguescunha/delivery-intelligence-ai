# Importa a biblioteca pandas e define o apelido "pd".
# O pandas é usado para manipulação e análise de dados, principalmente com DataFrames.
import pandas as pd

# Importa o módulo pyplot da biblioteca matplotlib e define o apelido "plt".
# O pyplot é usado para criar gráficos e visualizações de dados.
import matplotlib.pyplot as plt

# Importa o módulo os da biblioteca padrão do Python.
# O os permite interagir com o sistema operacional, como acessar pastas, arquivos e caminhos.
import os


# Carrega os arquivos CSV em DataFrames
df_pedidos = pd.read_csv("../../data/pedidos.csv")
df_restaurantes = pd.read_csv("../../data/restaurantes.csv")
df_avaliacoes = pd.read_csv("../../data/avaliacoes.csv")


# Exibe a quantidade de linhas carregadas em cada DataFrame
print("Pedidos carregados:", len(df_pedidos), "linhas")
print("Restaurantes carregados:", len(df_restaurantes), "linhas")
print("Avaliações carregadas:", len(df_avaliacoes), "linhas")


print("\nMétricas gerais:\n")


# Calcula o valor médio dos pedidos
valor_medio_pedido = df_pedidos["valor_pedido"].mean()
print(f"Ticket médio por pedido: R$ {valor_medio_pedido:.2f}")


# Calcula a quantidade e o percentual de pedidos atrasados
quantidade_total_pedidos = len(df_pedidos)
quantidade_pedidos_atrasados = df_pedidos["atrasado"].sum()

percentual_pedidos_atrasados = (
    quantidade_pedidos_atrasados / quantidade_total_pedidos
) * 100

print(
    f"Pedidos atrasados: {quantidade_pedidos_atrasados} "
    f"de {quantidade_total_pedidos} "
    f"({percentual_pedidos_atrasados:.1f}%)"
)


# Calcula o tempo médio de entrega
tempo_medio_entrega = df_pedidos["tempo_total_minutos"].mean()
print(f"Tempo médio de entrega: {tempo_medio_entrega:.1f} min")


# Calcula a nota média geral das avaliações
nota_media_geral = df_avaliacoes["nota"].mean()
print(f"Nota média geral: {nota_media_geral:.2f} de 5.0")


print("\nMétricas por dia da semana:\n")


# Define a ordem correta dos dias da semana
ordem_dias_semana = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo",
]


# Agrupa os pedidos por dia da semana, conta a quantidade de pedidos
# e reorganiza o resultado seguindo a ordem correta dos dias
quantidade_pedidos_por_dia = (
    df_pedidos
    .groupby("dia_semana")
    .size()
    .reindex(ordem_dias_semana)
)


# Exibe a quantidade de pedidos por dia da semana
print(quantidade_pedidos_por_dia.to_string())


print("\nMétricas por clima:\n")


# Calcula o percentual de pedidos atrasados para cada tipo de clima
percentual_atraso_por_clima = (
    df_pedidos
    .groupby("clima")["atrasado"]
    .mean()
    * 100
)


# Ordena os climas do maior para o menor percentual de atraso
percentual_atraso_por_clima = percentual_atraso_por_clima.sort_values(
    ascending=False
)


# Exibe o percentual de pedidos atrasados por clima
for clima, percentual_atraso in percentual_atraso_por_clima.items():
    print(f"  {clima:<15} {percentual_atraso:.1f}% atrasados")


print("\nTop 5 restaurantes por nota média:\n")


# Junta as avaliações com o nome dos restaurantes
df_avaliacoes_com_restaurante = df_avaliacoes.merge(
    df_restaurantes[["id_restaurante", "nome_restaurante"]],
    on="id_restaurante"
)


# Calcula a nota média de cada restaurante e seleciona os 5 melhores
top_5_restaurantes_por_nota = (
    df_avaliacoes_com_restaurante
    .groupby("nome_restaurante")["nota"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)


# Exibe os 5 restaurantes com melhor nota média
for nome_restaurante, nota_media_restaurante in top_5_restaurantes_por_nota.items():
    print(f"  {nome_restaurante:<35} {nota_media_restaurante:.2f}")


print()

# # ── 6. GRÁFICOS ──────────────────────────────────────────────────────────────

# os.makedirs("graficos", exist_ok=True)

# # --- Gráfico 1: Pedidos por dia da semana
# fig, ax = plt.subplots(figsize=(8, 4))
# por_dia.plot(kind="bar", ax=ax, color="steelblue", edgecolor="white")
# ax.set_title("Pedidos por Dia da Semana")
# ax.set_xlabel("Dia")
# ax.set_ylabel("Quantidade de Pedidos")
# ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
# plt.tight_layout()
# plt.savefig("graficos/pedidos_por_dia.png")
# plt.close()
# print("Gráfico salvo: graficos/pedidos_por_dia.png")

# # --- Gráfico 2: % de atraso por clima
# fig, ax = plt.subplots(figsize=(6, 4))
# cores = ["#e74c3c" if v > 50 else "#3498db" for v in atraso_por_clima.values]
# atraso_por_clima.plot(kind="bar", ax=ax, color=cores, edgecolor="white")
# ax.set_title("% de Pedidos Atrasados por Clima")
# ax.set_xlabel("Clima")
# ax.set_ylabel("% Atrasados")
# ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
# plt.tight_layout()
# plt.savefig("graficos/atraso_por_clima.png")
# plt.close()
# print("Gráfico salvo: graficos/atraso_por_clima.png")

# # --- Gráfico 3: Distribuição das notas
# fig, ax = plt.subplots(figsize=(6, 4))
# avaliacoes["nota"].value_counts().sort_index().plot(kind="bar", ax=ax, color="gold", edgecolor="white")
# ax.set_title("Distribuição das Notas")
# ax.set_xlabel("Nota")
# ax.set_ylabel("Quantidade de Avaliações")
# ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
# plt.tight_layout()
# plt.savefig("graficos/distribuicao_notas.png")
# plt.close()
# print("Gráfico salvo: graficos/distribuicao_notas.png")

# # --- Gráfico 4: Ticket médio por tipo de culinária
# pedidos_rest = pedidos.merge(restaurantes[["id_restaurante", "tipo_culinaria"]], on="id_restaurante")
# ticket_por_tipo = (
#     pedidos_rest.groupby("tipo_culinaria")["valor_pedido"]
#     .mean()
#     .sort_values(ascending=False)
# )

# fig, ax = plt.subplots(figsize=(9, 4))
# ticket_por_tipo.plot(kind="bar", ax=ax, color="mediumseagreen", edgecolor="white")
# ax.set_title("Ticket Médio por Tipo de Culinária")
# ax.set_xlabel("Tipo de Culinária")
# ax.set_ylabel("Valor Médio (R$)")
# ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")
# plt.tight_layout()
# plt.savefig("graficos/ticket_por_culinaria.png")
# plt.close()
# print("Gráfico salvo: graficos/ticket_por_culinaria.png")

# print()
# print("Análise concluída!")
