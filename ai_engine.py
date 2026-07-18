from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class RiskClassifier:
    def __init__(self):
        # 1. O Dataset (Conjunto de Dados de Treino)
        # É assim que ensinamos a IA. Quanto mais exemplos, mais inteligente ela fica.
        self.training_data = [
            # Risco Alto (Risco à vida ou acidentes graves)
            ("fio solto pegando fogo no poste dando choque", "Alto"),
            ("estourou um cano e a rua está alagando muito rápido", "Alto"),
            ("cheiro forte de gás e faíscas perto da estação", "Alto"),
            ("ônibus pegando fogo na avenida", "Alto"),
            ("poste caiu em cima da casa e tem fios no chão", "Alto"),
            
            # Risco Médio (Problemas graves, mas sem risco imediato à vida)
            ("estamos sem energia desde ontem a noite inteira", "Medio"),
            ("vazamento de água grande na calçada", "Medio"),
            ("ônibus quebrou no meio da rua e travou o trânsito", "Medio"),
            ("bueiro entupido retornando esgoto para a rua", "Medio"),
            
            # Risco Baixo (Inconvenientes e manutenções simples)
            ("lâmpada do poste está queimada", "Baixo"),
            ("ônibus atrasou 20 minutos hoje", "Baixo"),
            ("água está saindo fraca da torneira", "Baixo"),
            ("buraco pequeno na rua atrapalhando", "Baixo")
        ]
        
        # 2. Separando os Dados
        # X = As frases (os dados de entrada)
        # y = O nível de risco (as respostas corretas)
        X_train = [item[0] for item in self.training_data]
        y_train = [item[1] for item in self.training_data]
        
        # 3. Construindo o Cérebro (Pipeline)
        # O Pipeline conecta a transformação de texto em números com o algoritmo de aprendizado
        self.model = Pipeline([
            ('vectorizer', TfidfVectorizer()),  # Transforma o texto em uma matriz de números
            ('classifier', MultinomialNB())     # Algoritmo de probabilidade que aprende os padrões
        ])
        
        # 4. O Treinamento (Fit)
        # Aqui é onde a CPU trabalha. A IA estuda as frases e cria seu modelo matemático.
        self.model.fit(X_train, y_train)

    def predict_risk(self, description: str) -> str:
        """
        Recebe a descrição do usuário e tenta prever o nível de risco.
        """
        # A IA faz a inferência com base no que aprendeu no treinamento
        prediction = self.model.predict([description])
        return str(prediction[0])

# Instanciamos a classe para o main.py poder usá-la
classifier = RiskClassifier()