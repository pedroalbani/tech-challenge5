from app.core.mongodb_connector import MongoConnector

def test_api_mongo():
    print("🔹 Testando conexão do MongoDB dentro da API...")

    try:
        mongo = MongoConnector()
        if mongo.db is None:
            print("❌ Erro: `mongo.db` está `None`, a API não está acessando o banco!")
        else:
            print("✅ Conexão estabelecida na API com sucesso!")

            # Teste de inserção e leitura
            collection_name = "test_api_collection"
            test_doc = {"name": "API Test", "value": 42}
            mongo.salvar(collection_name, test_doc)

            print("🔹 Dados inseridos com sucesso!")

            result = mongo.listar(collection_name)
            print(f"✅ Dados encontrados na API: {result}")

    except Exception as e:
        print(f"❌ Erro ao testar MongoDB na API: {e}")

if __name__ == "__main__":
    test_api_mongo()
