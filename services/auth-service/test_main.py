from fastapi.testclient import TestClient
from main import app

# Cria um "cliente" falso que simula requisições para a nossa API
client = TestClient(app)

# Teste 1: Garante que a API está viva
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Auth Service está rodando perfeitamente!"}

# Teste 2: Garante que o login bloqueia senhas erradas (com dados falsos por enquanto)
def test_login_falho():
    response = client.post("/login", json={"email": "hacker@escola.br", "senha": "123"})
    assert response.status_code == 401