import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.mongodb_connector import MongoConnector

def testar_conexao():
    try:
        mongo = MongoConnector()
        # Testando conexão listando coleções
        collections = mongo.db.list_collection_names()
        print("Conexão com MongoDB bem-sucedida!")
        print(f"Coleções disponíveis: {collections}")
        return True
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return False

# Testando a conexão
if __name__ == "__main__":
    testar_conexao()
