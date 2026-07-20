import os
import json
from google import genai
from dotenv import load_dotenv
import re


load_dotenv()

class RiskAuditor:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        self.system_prompt = """
        Você é um auditor de infraestrutura urbana sênior. 
        Sua tarefa é analisar relatos de cidadãos sobre problemas em serviços essenciais (água, energia, transporte).
        
        Classifique o risco do relato em uma destas categorias exatas:
        - Alto: Risco imediato à vida, acidentes graves ou interrupção total (ex: fogo, fio exposto, enchente).
        - Medio: Problemas sérios sem risco imediato à vida (ex: vazamento, falta de energia).
        - Baixo: Inconvenientes ou manutenções simples (ex: lâmpada queimada, atraso).
        - Falso: Relatos absurdos, brincadeiras ou impossíveis (ex: dragão, alienígena).
        
        Você DEVE responder APENAS com um objeto JSON válido, sem markdown:
        {
            "risk_level": "Alto|Medio|Baixo|Falso",
            "extracted_entities": ["lista", "de", "palavras"],
            "justification": "Breve justificativa técnica"
        }
        """

    def predict_risk(self, description: str) -> str:
        try:
            prompt_completo = f"{self.system_prompt}\n\nRelato: '{description}'"
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt_completo
            )
            
            clean_text = re.sub(r'```(?:json)?\n?', '', response.text or '').strip()
            audited_data = json.loads(clean_text)
            
            print(f"\n[IA AUDITOR] Análise: {audited_data.get('justification', '')}")
            return audited_data.get("risk_level", "Baixo")

        except Exception as e:
            error_msg = str(e)
            # A REDE DE SEGURANÇA: Tratando o limite de cota
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print("\n[SISTEMA] Cota da IA excedida! Ativando protocolo de contingência (Fallback).")
                # Classificação de segurança manual baseada em palavras-chave urgentes
                palavras_criticas = ["fogo", "choque", "explosão", "enchente", "fio"]
                if any(palavra in description.lower() for palavra in palavras_criticas):
                    return "Alto"
                return "Medio"
            
            print(f"\n[ERRO IA] Falha desconhecida: {e}")
            return "Medio"

classifier = RiskAuditor()