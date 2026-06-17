from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Microsserviço de Autenticação Acadêmica"
)

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


class LoginRequest(BaseModel):
    email: str
    senha: str


class UsuarioCreate(BaseModel):
    email: str
    senha: str
    perfil: str = "aluno"


@app.get("/")
def health_check():
    return {"status": "Auth Service está rodando perfeitamente!"}


@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = models.Usuario(
        email=usuario.email,
        senha=usuario.senha,
        perfil=usuario.perfil
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return {
            "mensagem": "Usuário criado com sucesso no banco de dados!",
            "id_gerado": novo_usuario.id,
            "email": novo_usuario.email
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar usuário. Email já existe?"
        )


@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    usuario_db = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == req.email)
        .first()
    )

    if not usuario_db or usuario_db.senha != req.senha:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    return {
        "mensagem": f"Bem-vindo, {usuario_db.perfil}!",
        "token": "token-jwt-simulado-12345"
    }


@app.post("/validate")
def validate_token(token_data: dict):
    token = token_data.get("token")

    if token == "token-jwt-simulado-12345":
        return {"valid": True}

    return {"valid": False}