from typing import Any
from fastapi import APIRouter, Depends, Query
from app.services.comercio_service import ComercioService
from bson import json_util
import json
from typing import List

comercio_route = APIRouter(tags=["listagem"])

def criar_instancia_de_servico():
    return ComercioService()


@comercio_route.get("/comercio",summary="Lista e Filtra os dados referentes a Importação/Exportação")
def listar_dados_comercio(service: ComercioService = Depends(criar_instancia_de_servico)
                          , operacao: List[str] = Query(None)
                          , sub_operacao: List[str] = Query(None)
                          , pais: List[str] = Query(None)
                          , valor: List[str] = Query(None)
                          , quantidade: List[str] = Query(None)
                          , ano: List[str] = Query(None)
                          ):
    """
        Utilize esse serviço para listar os dados importados em  <a href="/docs/#/importar/importar_importar_get" target="_self">importar</a>

        Os campos String (Operacao,Sub_Operacao e Pais), aceitam uma lista inclusiva, que será tratado como um filtro IN.

        Para os campos Numéricos, será necessário utilizar ao menos um dos seguintes filtros:

          [gt] - <i>Maior que</i>

          [lt] - <i>Menor que</i>

          [eq] - <i>Igual a</i>

          [gte] - <i>Maior ou igual a </i>

          [lte] - <i>Menor ou igual a</i>

        Ex: Ano=[gt]1000&Ano=[lt]1500
    """
    filtro = {}
    if operacao != None:
        filtro["operacao"] = service.query_builder.escrever_filtro_string(operacao)
    if sub_operacao != None:
        filtro["sub_categoria_operacao"] = service.query_builder.escrever_filtro_string(sub_operacao)
    if pais != None:
        filtro["pais"] = service.query_builder.escrever_filtro_string(pais)
    if valor != None:
        filtro["valor"] = service.query_builder.escrever_filtro_numerico(valor)
    if quantidade != None:
        filtro["quantidade"] = service.query_builder.escrever_filtro_numerico(quantidade)
    if ano != None:
        filtro["ano"] = service.query_builder.escrever_filtro_numerico(ano)

    response = service.listar_comercios(filtro)

    return json.loads(json_util.dumps(response))