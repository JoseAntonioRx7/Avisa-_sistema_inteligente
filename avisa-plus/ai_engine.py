from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Nosso "conhecimento base". Quanto mais exemplos adicionarmos aqui no futuro, mais inteligente a IA fica.
TRAINING_DATA = [
    # (Descrição do problema, Nível de Risco)
    ("Falta de água na rua principal, as torneiras estão secas", "Alto"),
    ("Cano vazando um pouco na calçada, mas tem água em casa", "Baixo"),
    ("Sem energia elétrica desde as 14h, tudo escuro", "Alto"),
    ("A luz está piscando bastante, mas ainda não caiu", "Medio"),
    ("O ônibus não passou no horário de pico, ponto lotado", "Alto"),
    ("Atraso de 10 minutos no transporte", "Baixo"),
    ("Poste pegando fogo, soltando faíscas, perigo", "Alto"),
    ("Rua alagada, água entrando nas casas", "Alto"),
    ("Água com cor muito escura e cheiro estranho saindo da torneira", "Medio"),
    ("Fio solto no meio da rua", "Alto"),
]

class RiskClassifier:
    def __init__(self):
        # Pipeline: transforma o texto em números e aplica a classificação
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.is_trained = False

    def train(self):
        # Separa os textos e as etiquetas (labels)
        texts = [item[0] for item in TRAINING_DATA]
        labels = [item[1] for item in TRAINING_DATA]
        
        # Treina o modelo instantaneamente
        self.model.fit(texts, labels)
        self.is_trained = True
        print("Modelo de IA (NLP) treinado e pronto para uso!")

    def predict_risk(self, description: str) -> str:
        # Garante que o modelo treine na primeira vez que for chamado
        if not self.is_trained:
            self.train()
        
        # A IA faz a previsão com base no que aprendeu
        prediction = self.model.predict([description])
        return str(prediction[0])

# Criamos uma instância global para a API utilizar
classifier = RiskClassifier()