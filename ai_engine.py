import os
import json
import re
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class RiskAuditor:
    def __init__(self):
        # O novo SDK usa o Client para gerenciar a conexão
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # O System Prompt (regras do jogo) continua o mesmo
        self.system_prompt = """
        Você é um auditor de infraestrutura urbana sênior. 
        Sua tarefa é analisar relatos de cidadãos sobre problemas em serviços essenciais (água, energia, transporte).
        
        Classifique o risco do relato em uma destas categorias exatas:
        - Alto: Risco imediato à vida, acidentes graves ou interrupção total de serviço vital (ex: fogo, fio exposto, inundação grave).
        - Medio: Problemas sérios que precisam de atenção, mas sem risco imediato à vida (ex: vazamento, falta de energia).
        - Baixo: Inconvenientes ou manutenções simples (ex: lâmpada queimada, atraso).
        - Falso: Relatos absurdos, testes, brincadeiras ou impossíveis (ex: disco voador, dragão, invasão alienígena).
        
        Você DEVE responder APENAS com um objeto JSON válido, sem formatação markdown (como ```json), usando a seguinte estrutura:
        {
            "risk_level": "Alto|Medio|Baixo|Falso",
            "extracted_entities": ["lista", "de", "palavras-chave", "do", "problema"],
            "justification": "Breve justificativa técnica da sua decisão"
        }
        """

    def predict_risk(self, description: str) -> str:
        """
        Envia a descrição para o Gemini usando o novo SDK e audita a resposta.
        """
        try:
            # Junta as instruções do sistema com o relato do usuário
            prompt_completo = f"{self.system_prompt}\n\nRelato do cidadão: '{description}'"
            
            # Nova sintaxe para chamar o modelo (usando a versão flash mais recente)
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt_completo
            )
            
            # Limpa a resposta para o JSON ler corretamente
            clean_text = re.sub(r'```(?:json)?\n?', '', response.text or '').strip()
            
            # Transforma a string em um dicionário
            audited_data = json.loads(clean_text)
            
            # Exibe no terminal para acompanhamento
            print(f"\n[IA AUDITOR] Análise concluída: {audited_data.get('justification', '')}")
            print(f"[IA AUDITOR] Entidades detectadas: {audited_data.get('extracted_entities', [])}\n")
            
            return audited_data.get("risk_level", "Baixo")

        except Exception as e:
            print(f"Erro na análise da IA: {e}")
            return "Medio"

# Instanciamos o novo auditor
classifier = RiskAuditor()