Avisa+  ( Sistema inteligente de alertas focado em populações de áreas vulneráveis )

# Avisa+ API

Um sistema inteligente e automatizado para análise de risco em relatos de infraestrutura urbana e emissão de alertas preventivos. A aplicação utiliza inteligência artificial para auditar ocorrências em tempo real e cruza dados meteorológicos para notificar cidadãos sobre riscos iminentes em serviços essenciais (água, energia, transporte).

O core da aplicação é focado em **Python e Inteligência Artificial (LLMs)** para a tomada de decisão rápida na classificação de chamados. A evolução arquitetônica do projeto contempla a futura migração para **sistemas distribuídos e Web3**, visando garantir imutabilidade nos registros de auditoria e descentralização do processamento de alertas.

---

## 🏗️ Arquitetura e Estrutura do Projeto

A aplicação é construída de forma modular, separando as responsabilidades de processamento de IA, banco de dados, serviços externos e roteamento HTTP.

```text
.
├── ai_engine.py             # Motor de Inteligência Artificial (Integração Gemini)
├── database.py              # Configuração do banco SQLite e Modelos ORM (SQLAlchemy)
├── main.py                  # Ponto de entrada FastAPI e definição de Endpoints
├── notification_service.py  # Módulo de envio de SMS (Integração Twilio)
├── weather_service.py       # Serviço de predição meteorológica (OpenWeather API)
├── descobrir_modelos.py     # Script utilitário para listagem de modelos LLM
├── requirements.txt         # Dependências do projeto
└── templates/
    └── index.html           # Interface web estática


    Detalhamento dos Módulos:
    
ai_engine.py: Contém a classe RiskAuditor. Utiliza o modelo gemini-2.0-flash para analisar descrições em linguagem natural e classificar o risco (Alto, Medio, Baixo, Falso). Possui um sistema de fallback automático (contingência) que assume a classificação via palavras-chave caso a cota da API da IA seja excedida (Erro 429).

database.py: Gerencia a conexão com o banco de dados avisa_plus.db (SQLite). Define duas tabelas principais:

Event: Armazena os relatos, serviço afetado, localização e o nível de risco calculado pela IA.

Subscriber: Armazena os usuários do "Radar", contendo informações de contato e a região de interesse.

weather_service.py: Consulta a API do OpenWeather para monitorar tempestades, chuvas fortes ou ventanias nas regiões cadastradas, traduzindo o clima em um nível de risco de infraestrutura.

notification_service.py: Dispara alertas SMS utilizando a Twilio. Inclui um modo de simulação (mock) caso as credenciais não estejam presentes.

main.py: Orquestra todos os módulos utilizando o FastAPI. Gerencia a injeção de dependência do banco de dados e executa tarefas em segundo plano (BackgroundTasks) para não bloquear as respostas da API durante o envio de SMS.
<img width="160" height="125" alt="image" src="https://github.com/user-attachments/assets/5cb45b7c-3601-43fd-acf3-d11b8d2c19a8" />

<img width="480" height="154" alt="image" src="https://github.com/user-attachments/assets/5edc1c44-2d4d-4827-9a53-07fbfc2c7d97" />



