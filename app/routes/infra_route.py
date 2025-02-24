
from fastapi import APIRouter, Response, status
from app.services.health_check_service import HealthCheck

infra_route = APIRouter()

@infra_route.get("/health", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    """
    ## Realiza uma checagem da saúde da aplicação
    Utilize esse endpoint para verificar se todos os serviços necessários 
    estão rodando corretamente.

    Qualquer `status code` diferente de `200` significa problema, portanto,
    verifique na `response` qual serviço em específico está apresentando problema.
    """
    check_result = HealthCheck().check()

    if (check_result["healthy"] is False):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return check_result