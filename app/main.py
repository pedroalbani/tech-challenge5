from fastapi import FastAPI, Depends
from app.routes.comercio_route import comercio_route
from app.routes.infra_route import infra_route
from app.routes.auth import router as auth_route, get_current_active_user
from app.backend.mongodb_connector import MongoConnector

app = FastAPI(
    title="Datathon Fase 5"
)

app.include_router(comercio_route, dependencies=[Depends(get_current_active_user)])
app.include_router(infra_route)
app.include_router(auth_route, prefix="/auth")
