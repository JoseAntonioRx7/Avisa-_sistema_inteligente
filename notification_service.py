import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Carrega as credenciais
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

def enviar_sms(destino: str, mensagem: str):
    """
    Conecta na Twilio e dispara o SMS.
    """
    try:
        # Só tenta enviar se as chaves existirem no .env
        if not TWILIO_SID or not TWILIO_TOKEN:
            print(f"[MOCK SMS] Para {destino}: {mensagem}")
            return
            
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        message = client.messages.create(
            body=mensagem,
            from_=TWILIO_PHONE,
            to=destino
        )
        print(f"[SMS ENVIADO] ID: {message.sid} para {destino}")
        
    except Exception as e:
        print(f"[ERRO SMS] Falha ao enviar para {destino}: {e}")