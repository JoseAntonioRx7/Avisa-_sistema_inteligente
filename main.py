from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import ai_engine
import database
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
import weather_service
from fastapi import FastAPI, Depends, BackgroundTasks
import notification_service


app = FastAPI(
    title="Avisa+ API",
    description="Sistema inteligente de alertas para serviços essenciais.",
    version="2.0.0"
)

database.Base.metadata.create_all(bind=database.engine)  # Cria as tabelas no banco de dados, se não existirem

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

# Schemas para o Radar
class SubscriberCreate(BaseModel):
    contact_info: str
    location: str

class SubscriberResponse(SubscriberCreate):
    id: int
    is_active: bool
    model_config = {"from_attributes": True}


@app.get("/", response_class=HTMLResponse)
def read_root():
    # Lê o arquivo HTML que acabamos de criar e devolve para o navegador
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content

@app.post("/events/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # ATENÇÃO: Aqui é onde nossa IA vai entrar depois para classificar o risco!
    # Por enquanto, vamos deixar como "Pendente"
    calculated_risk = ai_engine.classifier.predict_risk(event.description)
    
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

# NOVA ROTA: Cadastro no Radar
@app.post("/subscribe/", response_model=SubscriberResponse)
def create_subscriber(sub: SubscriberCreate, db: Session = Depends(get_db)):
    # Verifica se o contato já existe para evitar duplicidade
    existing_sub = db.query(database.Subscriber).filter(
        database.Subscriber.contact_info == sub.contact_info
    ).first()
    
    if existing_sub:
        # Se já existe, apenas atualiza a localização
        existing_sub.location = sub.location  # type: ignore[assignment]
        db.commit()
        db.refresh(existing_sub)
        return existing_sub

    # Se é novo, cria o registro
    new_sub = database.Subscriber(
        contact_info=sub.contact_info,
        location=sub.location
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    
    return new_sub

# NOVA ROTA: O Vigia que verifica o clima para os inscritos
@app.get("/check-radar/")
def check_radar(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Pega todas as regiões únicas que temos cadastradas
    subscribers = db.query(database.Subscriber).filter(database.Subscriber.is_active == True).all()
    
    # Extrai apenas os nomes dos bairros/cidades, sem repetir
    unique_locations = set([sub.location for sub in subscribers])
    alerts_generated = []

    for location in unique_locations:
        weather_report = weather_service.check_weather_risk(str(location))
        
        if weather_report["risk"] in ["Alto", "Medio"]:
            # Acha quem são as pessoas dessa região
            affected_users = [str(sub.contact_info) for sub in subscribers if (str(sub.location) == location)]
            
            # Prepara a mensagem de emergência
            mensagem_alerta = f"AVISA+: Alerta de risco {weather_report['risk']} em {location}. {weather_report['message']}"
            
            # Dispara os SMS nos bastidores para não travar a tela do usuário
            for telefone in affected_users:
                background_tasks.add_task(notification_service.enviar_sms, telefone, mensagem_alerta)
            
            alerts_generated.append({
                "location": location,
                "risk": weather_report["risk"],
                "message": weather_report["message"],
                "users_notified": affected_users
            })

    if not alerts_generated:
        return {"status": "Tudo tranquilo", "message": "Nenhum risco iminente nas regiões monitoradas."}
    
    return {"status": "Alertas Disparados", "alerts": alerts_generated}