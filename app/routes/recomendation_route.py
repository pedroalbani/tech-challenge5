from fastapi import APIRouter, HTTPException
from app.services.recomendation_service import RecommendationService

recommendation_route = APIRouter()

@recommendation_route.get("/recommendations/{userid}")
def get_recommendations(userid: str):
    """
    ## Obtém recomendações para um usuário específico.
    - O `userid` é obrigatório.
    """
    if not userid:
        raise HTTPException(status_code=400, detail="O campo 'userid' é obrigatório.")

    print(f"UserID recebido: {userid}")

    filtro = {}
    recommendations = RecommendationService().get_all_categories(filtro)

    if not recommendations:
        raise HTTPException(status_code=404, detail="Nenhuma recomendação encontrada para esse usuário.")

    print(f"Recommendations retornadas: {recommendations}")
    return recommendations