import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

import models
from database import engine, get_db


# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - auth-service - %(levelname)s - %(message)s"
)

logger = logging.getLogger("auth-service")


# Criação das tabelas no banco
models.Base.metadata.create_all(bind=engine)


# Inicialização da aplicação
app = FastAPI(
    title="Auth Service",
    description="Microsserviço de Autenticação Acadêmica"
)


# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exposição de métricas Prometheus em /metrics
Instrumentator().instrument(app).expose(app)


# Schemas
class LoginRequest(BaseModel):
    email: str
    senha: str


class UsuarioCreate(BaseModel):
    email: str
    senha: str
    perfil: str = "aluno"


@app.get("/")
def root():
    logger.info("Health check raiz acessado")
    return {"status": "Auth Service está rodando perfeitamente!"}


@app.get("/health")
def health_check():
    logger.info("Health check acessado")
    return {
        "status": "ok",
        "service": "auth-service"
    }


@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    logger.info(f"Tentativa de cadastro de usuário: {usuario.email}")

    novo_usuario = models.Usuario(
        email=usuario.email,
        senha=usuario.senha,
        perfil=usuario.perfil
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        logger.info(f"Usuário cadastrado com sucesso: {novo_usuario.email}")

        return {
            "mensagem": "Usuário criado com sucesso no banco de dados!",
            "id_gerado": novo_usuario.id,
            "email": novo_usuario.email
        }

    except Exception:
        db.rollback()

        logger.warning(f"Erro ao cadastrar usuário: {usuario.email}")

        raise HTTPException(
            status_code=400,
            detail="Erro ao criar usuário. Email já existe?"
        )


@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Tentativa de login para: {req.email}")

    usuario_db = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == req.email)
        .first()
    )

    if not usuario_db or usuario_db.senha != req.senha:
        logger.warning(f"Login inválido para: {req.email}")

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    logger.info(f"Login realizado com sucesso: {usuario_db.email}")

    return {
        "mensagem": f"Bem-vindo, {usuario_db.perfil}!",
        "token": "token-jwt-simulado-12345"
    }


@app.post("/validate")
def validate_token(token_data: dict):
    token = token_data.get("token")

    if token == "token-jwt-simulado-12345":
        logger.info("Token validado com sucesso")
        return {"valid": True}

    logger.warning("Tentativa de validação com token inválido")
    return {"valid": False}