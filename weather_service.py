import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def check_weather_risk(location_name: str) -> dict:
    """
    Verifica o clima de uma região e retorna se há risco de impacto
    na infraestrutura (ex: chuvas fortes que podem derrubar energia).
    """
    if not API_KEY:
        return {"risk": "Baixo", "message": "API Key não configurada."}

    # Monta a URL para buscar a cidade/bairro em português
    params = {
        "q": f"{location_name}, BR",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            weather_condition = data["weather"][0]["main"] # Ex: Rain, Thunderstorm, Clear
            description = data["weather"][0]["description"]
            
            # Lógica de Classificação Preditiva
            if weather_condition in ["Thunderstorm", "Tornado", "Squall"]:
                return {
                    "risk": "Alto", 
                    "message": f"Alerta Crítico: Previsão de {description}. Alto risco de queda de energia e árvores."
                }
            elif weather_condition in ["Rain", "Drizzle"]:
                return {
                    "risk": "Medio", 
                    "message": f"Atenção: Previsão de {description}. Risco moderado de alagamentos e atrasos no transporte."
                }
            else:
                return {
                    "risk": "Baixo", 
                    "message": f"Clima estável ({description}). Serviços operando normalmente."
                }
        else:
            return {"risk": "Baixo", "message": f"Não foi possível obter dados para {location_name}."}

    except Exception as e:
        return {"risk": "Baixo", "message": "Erro de conexão com o satélite."}