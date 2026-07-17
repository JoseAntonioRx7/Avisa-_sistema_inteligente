from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Cria um arquivo SQLite local chamado avisa_plus.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./avisa_plus.db"

# connect_args é necessário apenas para SQLite no FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo do nosso Evento/Alerta
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    service_type = Column(String, index=True) # ex: agua, energia, transporte
    risk_level = Column(String)               # ex: Baixo, Medio, Alto (A IA vai preencher isso!)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Cria a tabela no banco de dados automaticamente
Base.metadata.create_all(bind=engine)