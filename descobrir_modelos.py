import os
from google import genai
from dotenv import load_dotenv

# Carrega a sua chave do .env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Buscando modelos disponíveis para a sua chave...\n")

# Pede ao Google a lista de todos os modelos que você tem permissão para usar
for model in client.models.list():
    # Obtém a lista de métodos de geração de forma segura (atributo ou dict)
    methods = None
    if hasattr(model, "supported_generation_methods"):
        methods = getattr(model, "supported_generation_methods")
    elif isinstance(model, dict):
        methods = model.get("supported_generation_methods")
    else:
        methods = getattr(model, "supported_generation_methods", None)

    # Filtra para mostrar apenas os modelos de geração de texto
    if methods and "generateContent" in methods:
        # Usa getattr para evitar erro caso name não exista como atributo
        name = getattr(model, "name", None) or (model.get("name") if isinstance(model, dict) else None)
        print(f"- {name}")