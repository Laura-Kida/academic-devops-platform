from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# A URL de conexão segue este padrão: postgresql://usuario:senha@host:porta/nome_do_banco
# Estamos apontando para 'devops_db' porque é o nome do container do banco na rede do Docker
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@devops_db:5432/academic_db"

# Cria o "motor" de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a fábrica de sessões (cada requisição na API abrirá uma sessão rápida com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criarmos as nossas tabelas depois
Base = declarative_base()

# Função auxiliar para injetar o banco de dados nas rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()