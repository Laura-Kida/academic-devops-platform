from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializa a aplicação FastAPI
app = FastAPI(title="Auth Service", description="Microsserviço de Autenticação Acadêmica")

# 1. Definindo o Modelo de Dados (Como esperamos receber a requisição)
class LoginRequest(BaseModel):
    email: str
    senha: str

# 2. Banco de dados "Fake" na memória (Substituiremos pelo PostgreSQL depois)
USUARIOS_MOCK = {
    "professor@escola.br": "senha123",
    "aluno@escola.br": "senha123"
}

# 3. Rota de Health Check (Para o Docker saber se o serviço está vivo)
@app.get("/")
def health_check():
    return {"status": "Auth Service está rodando perfeitamente!"}

# 4. Rota principal de Login
@app.post("/login")
def login(request: LoginRequest):
    # Verifica se o email existe e se a senha bate
    if request.email in USUARIOS_MOCK and USUARIOS_MOCK[request.email] == request.senha:
        return {
            "mensagem": "Login aprovado!",
            "token": "token-jwt-simulado-12345",
            "usuario": request.email
        }
    
    # Se errar a senha ou usuário não existir, devolve Erro 401 (Não Autorizado)
    raise HTTPException(status_code=401, detail="Email ou senha inválidos")