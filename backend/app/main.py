# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import database
from . import models

from .modules.api_router import api_router

app = FastAPI(
    title="DecisumSystem API",
    description="API para o sistema de gestão integrada DecisumSystem.",
    version="0.1.0"
)

# --- CONFIGURAÇÃO DO CORS ---
# Esta é a configuração que resolve o problema de comunicação com o frontend.

origins = [
    "http://localhost:5173", # O endereço do seu servidor de desenvolvimento Vite/React
    "http://localhost:3000", # Adicione outras portas comuns, se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FIM DA CONFIGURAÇÃO DO CORS ---

# @app.on_event("startup")
# def on_startup():
    # models.Base.metadata.create_all(bind=database.engine)

app.include_router(api_router)

@app.get("/", tags=["Status"])
def read_root():
    return {"status": "API está no ar!"}

