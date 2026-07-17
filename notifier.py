import pyttsx3
import threading

class Notifier:
    def __init__(self):
        # A inicialização do motor de voz
        pass

    def _speak_offline(self, risk_level: str, description: str):
        """Função interna que aciona os alto-falantes do computador"""
        engine = pyttsx3.init()
        
        # Diminui um pouco a velocidade da voz para ficar mais claro
        engine.setProperty('rate', 160) 
        
        mensagem = f"Atenção. Alerta de risco {risk_level} registrado na sua região. Motivo: {description}"
        print(f"🔊 [SISTEMA OFFLINE] Falando: {mensagem}")
        
        engine.say(mensagem)
        engine.runAndWait()

    def send_voice_alert(self, risk_level: str, description: str):
        """
        Dispara o áudio em uma Thread separada.
        Isso garante que a API responda instantaneamente ao usuário,
        enquanto a voz toca no alto-falante em paralelo.
        """
        if risk_level in ["Alto", "Medio"]:  # Só avisa em voz alta se for relevante
            thread = threading.Thread(target=self._speak_offline, args=(risk_level, description))
            thread.start()

# Instância global
alert_system = Notifier()