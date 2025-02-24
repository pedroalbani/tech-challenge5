from app.services import configuracao_service, transformar_dados_service
from app.config.base_settings import AppConfiguration
from app.backend.mongodb_connector import MongoConnector
import pandas as pd
from urllib import error

class BaixarDadosService:
    def __init__(self):
        self.settings = configuracao_service.ConfiguracaoService()
        self.app_setting = AppConfiguration()
        self.db = MongoConnector()

    def importar(self, tipo_operacao, sub_categoria = None, atualizar_base = True):
        sucesso = False

        try:
            tipo_objeto, dados = self.download_data(tipo_operacao, sub_categoria)
            mensagem = "Dados importados com sucesso!"

            if atualizar_base:
                self.atualizar_base(dados, tipo_objeto, tipo_operacao, sub_categoria)
                mensagem = " Obs: a base de dados foi atualizada."

            sucesso = True

        except Exception as ex:
            mensagem = "Não foi possível concluir a requisição. Mensagem técnica: " + str(ex)
            dados = []

        finally:
            return self.criar_response(dados, sucesso, mensagem)

    def download_data(self, tipo_operacao, sub_categoria):
        configuracao = self.settings.obter_configuracao_extracao(tipo_operacao, sub_categoria)

        if 'sub_tipos' not in configuracao.keys():
            sub_categorias_lst = [{"label_arquivo":"","categoria":""}]
        elif sub_categoria != None:
            sub_categorias_lst = [{"label_arquivo":x["label_arquivo"],"categoria":x["sub_tipo_operacao"]} for x in configuracao["sub_tipos"] if x["sub_tipo_operacao"] == sub_categoria]
        else:
            sub_categorias_lst = [{"label_arquivo":x["label_arquivo"],"categoria":x["sub_tipo_operacao"]}  for x in configuracao["sub_tipos"]]

        modelos = []

        for subcat_atual in sub_categorias_lst:

            nome_arquivo = configuracao["label_arquivo"] + subcat_atual["label_arquivo"] + ".csv"
            try:
                dados = pd.read_csv(self.app_setting.url_arquivo + nome_arquivo, **configuracao["pandas"])
            except error.HTTPError:
                dados = pd.read_csv(self.app_setting.url_fallback + nome_arquivo, **configuracao["pandas"])

            if len(configuracao["renomear_colunas"].keys()) > 0:
                dados = dados.rename(columns=configuracao["renomear_colunas"])

            if str(configuracao["tipo_objeto"]).lower() == "comercio":
                transformador = transformar_dados_service.TransformarDado(
                    transformar_dados_service.ComercioStrategy())
            else:
                transformador = transformar_dados_service.TransformarDado(
                    transformar_dados_service.ManufaturaStrategy())

            modelos += transformador.transformar(dados, tipo_operacao, subcat_atual["categoria"])

        return configuracao["tipo_objeto"], modelos

    def atualizar_base(self,dados,tipo_objeto,tipo_operacao,sub_categoria):
        filtro_apagar = {}
        filtro_apagar["operacao"] = tipo_operacao
        if sub_categoria != None:
            filtro_apagar["sub_categoria_operacao"] = sub_categoria
        self.db.apagar(tipo_objeto,filtro_apagar)

        self.db.salvar(tipo_objeto,dados)

    def criar_response(self, dados, sucesso, mensagem):
        csvResponseDetails = {
            "tamanho": len(dados),
            "sucesso": sucesso,
            "mensagem": mensagem,
            "dados":dados
        }

        return csvResponseDetails