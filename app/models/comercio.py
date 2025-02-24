from pydantic import BaseModel
class Comercio(BaseModel):
    pais: str
    ano: int
    quantidade: int
    valor: float
    operacao: str
    sub_categoria_operacao: str
    def __init__(self,pais,ano,quantidade,valor,operacao, subcat_operacao):
        super().__init__(pais=pais,ano=ano,quantidade=quantidade,valor=valor,operacao=operacao, sub_categoria_operacao = subcat_operacao)