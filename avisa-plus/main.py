from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import ai_engine
import database

app = FastAPI(
    title="Avisa+ API",
    description="Sistema inteligente de alertas para serviços essenciais.",
    version="2.0.0"
)

# Dependência para abrir e fechar a conexão com o banco a cada requisição
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema Pydantic: O formato exato que a API espera receber do usuário
class EventCreate(BaseModel):
    description: str
    service_type: str
    location: str

# Schema Pydantic: O formato que a API devolve
class EventResponse(EventCreate):
    id: int
    risk_level: str

    # Configuração para o Pydantic ler os dados do SQLAlchemy
    model_config = {"from_attributes": True}

@app.get("/")
def read_root():
    return {"status": "Avisa+ API rodando perfeitamente!"}

@app.post("/events/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # ATENÇÃO: Aqui é onde nossa IA vai entrar depois para classificar o risco!
    # Por enquanto, vamos deixar como "Pendente"
    calculated_risk = calculated_risk = ai_engine.classifier.predict_risk(event.description)
    
    # Salva no banco de dados
    db_event = database.Event(
        description=event.description,
        service_type=event.service_type,
        location=event.location,
        risk_level=calculated_risk
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event