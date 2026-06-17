from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Importamos os arquivos que acabamos de criar
import models
from database import engine, get_db

# Este comando é o que efetivamente CRIA a tabela no banco de dados quando a API liga
models.Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(title="Auth Service", description="Microsserviço de Autenticação Acadêmica")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definindo o Modelo de Dados (Como esperamos receber a requisição)
class LoginRequest(BaseModel):
    email: str
    senha: str

# Banco de dados "Fake" na memória (Substituiremos pelo PostgreSQL depois)
USUARIOS_MOCK = {
    "professor@escola.br": "senha123",
    "aluno@escola.br": "senha123"
}

# Rota de Health Check (Para o Docker saber se o serviço está vivo)
@app.get("/")
def health_check():
    return {"status": "Auth Service está rodando perfeitamente!"}

class LoginRequest(BaseModel):
    email: str
    senha: str

# Novo modelo para o Cadastro
class UsuarioCreate(BaseModel):
    email: str
    senha: str
    perfil: str = "aluno"

# Nova rota para Criar Usuário no Banco de Dados
@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Prepara o usuário para ser salvo (usando o modelo do banco)
    novo_usuario = models.Usuario(
        email=usuario.email, 
        senha=usuario.senha, 
        perfil=usuario.perfil
    )
    
    try:
        # Adiciona e salva no banco de dados
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario) # Atualiza a variável para pegar o ID gerado pelo banco
        
        return {
            "mensagem": "Usuário criado com sucesso no banco de dados!", 
            "id_gerado": novo_usuario.id,
            "email": novo_usuario.email
        }
    except Exception as e:
        db.rollback() # Se der erro (ex: email repetido), desfaz a operação
        raise HTTPException(status_code=400, detail="Erro ao criar usuário. Email já existe?")

# A rota de login agora recebe a injeção do banco de dados (db: Session)
@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # 1. Fazemos uma "query" (consulta) real no banco de dados buscando o email
    usuario_db = db.query(models.Usuario).filter(models.Usuario.email == req.email).first()

    # 2. Verificamos se o usuário não foi encontrado OU se a senha não bate
    if not usuario_db or usuario_db.senha != req.senha:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # 3. Se passou pelas barreiras, o login é sucesso!
    return {
        "mensagem": f"Bem-vindo, {usuario_db.perfil}!",
        "token": "token-jwt-simulado-12345"
    }
    
    # Se errar a senha ou usuário não existir, devolve Erro 401 (Não Autorizado)
    raise HTTPException(status_code=401, detail="Email ou senha inválidos")
@app.post("/validate")
def validate_token(token_data: dict):
    token = token_data.get("token")

    if token == "token-jwt-simulado-12345":
        return {"valid": True}

    return {"valid": False}