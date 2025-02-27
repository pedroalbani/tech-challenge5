from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:pass123@localhost:27017/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "tech_db")

def debug_mongo_client():
    print("🔹 Testando conexão com o MongoDB...")

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # Testa a conexão imediatamente
        print(f"✅ Conectado ao MongoDB: {MONGO_URI}")
    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB: {e}")

if __name__ == "__main__":
    debug_mongo_client()
