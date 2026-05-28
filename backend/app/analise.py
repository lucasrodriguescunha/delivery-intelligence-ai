import pandas as pd
import matplotlib.pyplot as plt
import os

# ── 1. CARREGAR OS CSVs ──────────────────────────────────────────────────────

pedidos      = pd.read_csv("../../data/pedidos.csv")
restaurantes = pd.read_csv("../../data/restaurantes.csv")
avaliacoes   = pd.read_csv("../../data/avaliacoes.csv")

print("Pedidos carregados:",      len(pedidos),      "linhas")
print("Restaurantes carregados:", len(restaurantes), "linhas")
print("Avaliações carregadas:",   len(avaliacoes),   "linhas")
print()

# ── 2. MÉTRICAS GERAIS ───────────────────────────────────────────────────────

print("=" * 45)
print("MÉTRICAS GERAIS")
print("=" * 45)

# Ticket médio
ticket_medio = pedidos["valor_pedido"].mean()
print(f"Ticket médio por pedido:   R$ {ticket_medio:.2f}")

# Percentual de pedidos atrasados
total_pedidos   = len(pedidos)
pedidos_atrasados = pedidos["atrasado"].sum()
pct_atraso = (pedidos_atrasados / total_pedidos) * 100
print(f"Pedidos atrasados:         {pedidos_atrasados} de {total_pedidos} ({pct_atraso:.1f}%)")

# Tempo médio de entrega
tempo_medio = pedidos["tempo_total_minutos"].mean()
print(f"Tempo médio de entrega:    {tempo_medio:.1f} min")

# Nota média geral
nota_media = avaliacoes["nota"].mean()
print(f"Nota média geral:          {nota_media:.2f} / 5.0")

print()

# ── 3. MÉTRICAS POR DIA DA SEMANA ────────────────────────────────────────────

print("=" * 45)
print("PEDIDOS POR DIA DA SEMANA")
print("=" * 45)

ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
por_dia = pedidos.groupby("dia_semana").size().reindex(ordem_dias)
print(por_dia.to_string())
print()

# ── 4. MÉTRICAS POR CLIMA ────────────────────────────────────────────────────

print("=" * 45)
print("ATRASO POR CLIMA")
print("=" * 45)

atraso_por_clima = pedidos.groupby("clima")["atrasado"].mean() * 100
atraso_por_clima = atraso_por_clima.sort_values(ascending=False)
for clima, pct in atraso_por_clima.items():
    print(f"  {clima:<15} {pct:.1f}% atrasados")
print()

# ── 5. TOP 5 RESTAURANTES (por nota) ─────────────────────────────────────────

print("=" * 45)
print("TOP 5 RESTAURANTES POR NOTA MÉDIA")
print("=" * 45)

# Junta avaliações com nome do restaurante
av_com_nome = avaliacoes.merge(restaurantes[["id_restaurante", "nome_restaurante"]], on="id_restaurante")
top_restaurantes = (
    av_com_nome.groupby("nome_restaurante")["nota"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)
for nome, nota in top_restaurantes.items():
    print(f"  {nome:<35} {nota:.2f}")
print()

# ── 6. GRÁFICOS ──────────────────────────────────────────────────────────────

os.makedirs("graficos", exist_ok=True)

# --- Gráfico 1: Pedidos por dia da semana
fig, ax = plt.subplots(figsize=(8, 4))
por_dia.plot(kind="bar", ax=ax, color="steelblue", edgecolor="white")
ax.set_title("Pedidos por Dia da Semana")
ax.set_xlabel("Dia")
ax.set_ylabel("Quantidade de Pedidos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("graficos/pedidos_por_dia.png")
plt.close()
print("Gráfico salvo: graficos/pedidos_por_dia.png")

# --- Gráfico 2: % de atraso por clima
fig, ax = plt.subplots(figsize=(6, 4))
cores = ["#e74c3c" if v > 50 else "#3498db" for v in atraso_por_clima.values]
atraso_por_clima.plot(kind="bar", ax=ax, color=cores, edgecolor="white")
ax.set_title("% de Pedidos Atrasados por Clima")
ax.set_xlabel("Clima")
ax.set_ylabel("% Atrasados")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("graficos/atraso_por_clima.png")
plt.close()
print("Gráfico salvo: graficos/atraso_por_clima.png")

# --- Gráfico 3: Distribuição das notas
fig, ax = plt.subplots(figsize=(6, 4))
avaliacoes["nota"].value_counts().sort_index().plot(kind="bar", ax=ax, color="gold", edgecolor="white")
ax.set_title("Distribuição das Notas")
ax.set_xlabel("Nota")
ax.set_ylabel("Quantidade de Avaliações")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("graficos/distribuicao_notas.png")
plt.close()
print("Gráfico salvo: graficos/distribuicao_notas.png")

# --- Gráfico 4: Ticket médio por tipo de culinária
pedidos_rest = pedidos.merge(restaurantes[["id_restaurante", "tipo_culinaria"]], on="id_restaurante")
ticket_por_tipo = (
    pedidos_rest.groupby("tipo_culinaria")["valor_pedido"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(9, 4))
ticket_por_tipo.plot(kind="bar", ax=ax, color="mediumseagreen", edgecolor="white")
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
