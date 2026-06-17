from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    # Define o nome da tabela lá no PostgreSQL
    __tablename__ = "usuarios"

    # Define as colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    perfil = Column(String, default="aluno") # Pode ser "aluno" ou "professor"