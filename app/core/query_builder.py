from typing import List
import re
class QueryBuilder:
    def __init__(self):
        self.padrao_operador_er = "\[(\w{2,3})\]"
        self.padrao_param_er = "(?<=])(\d*)"
        self.operacoes_aceitas = ["$gt","$lt","$eq","$gte","$lte"]

    def escrever_filtro_numerico(self,parametros:List[str]):
        try:
            query = {'$' + re.search(self.padrao_operador_er, x).group(1).lower(): float(re.search(self.padrao_param_er, x).group(1)) for x in parametros}
        except:
            raise Exception("Um filtro inesperado/incorreto foi adicionado a sua requisição.")

        operacoes_inexperadas = ["[" + x.replace("$","") + "]" for x in query.keys() if x not in self.operacoes_aceitas]
        if len(operacoes_inexperadas) > 0:
            raise Exception("As seguintes operações não são aceitas pelo sistema: " + ",".join(operacoes_inexperadas))
        else:
            return query
    def escrever_filtro_string(self,parametros:List[str]):
        query = {}
        query["$in"] = parametros

        return query