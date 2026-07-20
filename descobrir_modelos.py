import os
from google import genai
from dotenv import load_dotenv

# Carrega a sua chave do .env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- LISTA COMPLETA DE MODELOS ---")
for model in client.models.list():
    # Vai imprimir o nome exato de cada modelo disponível
    print(model.name)
print("---------------------------------")