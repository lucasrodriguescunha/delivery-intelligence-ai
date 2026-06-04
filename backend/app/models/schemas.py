from pydantic import BaseModel


class PreverAtrasoRequest(BaseModel):
    valor_pedido: float
    quantidade_itens: int
    tempo_preparo_minutos: float
    tempo_estimado_minutos: float
    distancia_km: float
    hora: int
    clima: str
    dia_semana: str


class PreverAtrasoResponse(BaseModel):
    atrasado: bool
    probabilidade: float


class BuscarAvaliacoesRequest(BaseModel):
    query: str
    n_resultados: int = 5
    filtro_nota_minima: float | None = None


class InsightsRequest(BaseModel):
    query: str = "atraso entrega qualidade"
    n_reviews: int = 10
