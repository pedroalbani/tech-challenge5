from fastapi import FastAPI
from app.core.mongodb_connector import MongoConnector
from app.routes import auth

# Inicializa a aplicação FastAPI
app = FastAPI(title="Datathon Fase 5")

# Teste de conexão com MongoDB (opcional, remova se não precisar)
try:
    mongo_connector = MongoConnector()
    mongo_connector.db.command("ping")  # Teste simples para validar a conexão
    mongo_status = True
except Exception as e:
    mongo_status = False

# Inclui as rotas de autenticação
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Rota raiz para testar se a API está rodando
@app.get("/")
def root():
    return {"message": "API is running successfully!"}

# Rota de health check
@app.get("/health")
def health_check():
    return {"status": "ok", "mongo": mongo_status}
