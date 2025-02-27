from fastapi import APIRouter, Response, status
from app.services.health_check_service import HealthCheck

infra_route = APIRouter()

@infra_route.get("/health", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    """
    ## Realiza uma checagem da saúde da aplicação
    Utilize esse endpoint para verificar se a API está rodando corretamente.
    """
    check_result = HealthCheck().check()
    return check_result
