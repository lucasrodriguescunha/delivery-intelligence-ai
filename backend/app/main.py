import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

import chromadb
from api.routes import router
from rag.embeddings import carregar_avaliacoes, criar_colecao, criar_funcao_embedding, popular_colecao
from state import estado

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "../../data"
MODELO_PATH = BASE_DIR / "ml/modelo_atraso.joblib"
CHROMA_PATH = str(BASE_DIR / "chroma_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    estado["pipeline"] = joblib.load(MODELO_PATH)

    funcao_embedding = criar_funcao_embedding()
    client_chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    colecao = criar_colecao(client_chroma, funcao_embedding)

    df_aval = carregar_avaliacoes(
        str(DATA_DIR / "avaliacoes.csv"),
        str(DATA_DIR / "restaurantes.csv"),
    )
    popular_colecao(colecao, df_aval)

    estado["colecao"] = colecao
    estado["df_pedidos"] = pd.read_csv(DATA_DIR / "pedidos.csv")
    estado["df_avaliacoes"] = pd.read_csv(DATA_DIR / "avaliacoes.csv")

    yield

    estado.clear()


app = FastAPI(title="Delivery Intelligence AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
