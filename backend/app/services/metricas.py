import pandas as pd


FEATURES_NUMERICAS = [
    "valor_pedido",
    "quantidade_itens",
    "tempo_preparo_minutos",
    "tempo_estimado_minutos",
    "distancia_km",
    "hora",
]
FEATURES_CATEGORICAS = ["clima", "dia_semana"]


_ORDEM_DIAS = [
    "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo",
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]


def _ordenar_dias(d: dict) -> dict:
    presentes = [k for k in _ORDEM_DIAS if k in d]
    resto = [k for k in d if k not in _ORDEM_DIAS]
    chaves = presentes + resto
    return {k: d[k] for k in chaves}


def calcular_metricas(df: pd.DataFrame, df_avaliacoes: pd.DataFrame) -> dict:
    total = len(df)
    atrasados = int(df["atrasado"].sum())

    pedidos_por_dia = _ordenar_dias(df.groupby("dia_semana").size().to_dict())
    atraso_por_clima = {
        k: round(float(v) * 100, 1)
        for k, v in df.groupby("clima")["atrasado"].mean().items()
    }
    tempo_por_dia = _ordenar_dias({
        k: round(float(v), 1)
        for k, v in df.groupby("dia_semana")["tempo_total_minutos"].mean().items()
    })

    return {
        "ticket_medio_R$": round(float(df["valor_pedido"].mean()), 2),
        "total_pedidos": total,
        "pedidos_atrasados": atrasados,
        "percentual_atraso_%": round((atrasados / total) * 100, 1),
        "tempo_medio_entrega_min": round(float(df["tempo_total_minutos"].mean()), 1),
        "nota_media_geral": round(float(df_avaliacoes["nota"].mean()), 2),
        "clima_maior_atraso": df.groupby("clima")["atrasado"].mean().idxmax(),
        "dia_maior_volume": df.groupby("dia_semana").size().idxmax(),
        "pedidos_por_dia": pedidos_por_dia,
        "atraso_por_clima": atraso_por_clima,
        "tempo_por_dia": tempo_por_dia,
    }
