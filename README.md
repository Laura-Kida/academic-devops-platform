# Plataforma DevOps Acadêmica

Projeto Final de Semestre de Engenharia da Computação focado em criar uma Plataforma DevOps com Microsserviços, Observabilidade e Pipeline CI/CD Completo.

## 1. Documento Arquitetural

O sistema foi desenhado para ser uma plataforma escalável de gerenciamento acadêmico. A arquitetura adota a separação de responsabilidades e independência de deploy através de conteinerização.

**Decisões Técnicas:**

* **Frontend:** Aplicação Web isolada (React/Vite).

* **Backend:** Microsserviços independentes desenvolvidos em Python (FastAPI), comunicando-se via API REST.

* **Banco de Dados:** PostgreSQL, adotado para garantir a integridade dos relacionamentos complexos do domínio acadêmico.

* **Infraestrutura:** Ambiente local gerenciado via `docker-compose`, com `Dockerfile` exclusivo para cada serviço.

## 2. Definição dos Microsserviços

A plataforma atende à exigência mínima de serviços com a seguinte divisão:

* **auth-service:** Microsserviço focado em segurança. Gerencia a entidade Usuário e é responsável pela autenticação simples do sistema.

* **academic-service:** Microsserviço focado na regra de negócio (Core). Gerencia as entidades de Alunos, Professores, Disciplinas, Turmas, Matrículas e Atividades.

## 3. Modelo Conceitual

Abaixo está a representação UML das entidades e relacionamentos do banco de dados relacional:

```mermaid
classDiagram
    Usuario <|-- Professor
    Usuario <|-- Aluno
    
    Professor "1" --> "*" Disciplina : ministra
    Disciplina "1" --> "*" Turma
    Turma "1" --> "*" Matricula
    Aluno "1" --> "*" Matricula
    Turma "1" --> "*" Atividade
    Atividade "1" --> "*" Entrega
    Aluno "1" --> "*" Entrega

    class Usuario {
        +id
        +nome
        +email
        +senha
        +tipo
    }
    class Professor {
        +siape
        +departamento
    }
    class Aluno {
        +matricula
        +curso
    }
    class Disciplina {
        +id
        +nome
        +codigo
        +cargaHoraria
    }
    class Turma {
        +id
        +semestre
        +horario
    }
    class Matricula {
        +data
        +status
    }
    class Atividade {
        +id
        +titulo
        +descricao
        +prazo
    }
    class Entrega {
        +dataEntrega
        +nota
    }

    ## 4. Deploy e Observabilidade — Sprint 3

Na Sprint 3, a aplicação foi publicada em ambiente externo utilizando a plataforma Render. A arquitetura foi mantida em serviços separados, seguindo a proposta de microsserviços da plataforma acadêmica.

### Serviços publicados

* **Frontend React/Vite:** https://academic-devops-platform.onrender.com
* **Auth Service:** https://auth-service-9bwb.onrender.com
* **Academic Service:** https://academic-service-71ed.onrender.com
* **Banco de Dados:** PostgreSQL gerenciado pelo Render

### Arquitetura em Produção

```text
Frontend React/Vite
        |
        | REST API
        v
Auth Service
        |
        v
PostgreSQL

Frontend React/Vite
        |
        | REST API com token
        v
Academic Service
        |
        | valida token
        v
Auth Service
        |
        v
PostgreSQL
```

### Fluxo de Autenticação

1. O usuário acessa o frontend publicado no Render.
2. O usuário realiza cadastro ou login.
3. O frontend envia as credenciais para o Auth Service.
4. O Auth Service valida o usuário e retorna um token.
5. O frontend envia esse token nas requisições para o Academic Service.
6. O Academic Service valida o token consultando o Auth Service.
7. Se o token for válido, o Academic Service libera o acesso aos cursos.

### Health Checks

Os microsserviços possuem endpoints de health check para verificar se estão ativos:

* Auth Service: https://auth-service-9bwb.onrender.com/health
* Academic Service: https://academic-service-71ed.onrender.com/health

Exemplo de resposta esperada:

```json
{
  "status": "ok",
  "service": "auth-service"
}
```

### Métricas

Também foram adicionadas métricas básicas no formato Prometheus:

* Auth Metrics: https://auth-service-9bwb.onrender.com/metrics
* Academic Metrics: https://academic-service-71ed.onrender.com/metrics

As métricas permitem observar informações como:

* quantidade de requisições por rota;
* status HTTP das respostas;
* tempo de resposta;
* uso básico de CPU e memória do processo.

Exemplo de métrica:

```text
http_requests_total{handler="/health",method="GET",status="2xx"} 1.0
```

### Logs

Os microsserviços também registram logs para eventos importantes da aplicação, como:

* acesso ao health check;
* cadastro de usuário;
* login realizado;
* tentativa de login inválida;
* validação de token;
* acesso negado por token ausente;
* listagem de cursos;
* criação de curso.

Esses logs podem ser acompanhados diretamente no painel do Render, na aba **Logs** de cada serviço.

### Variáveis de Ambiente

Para separar o ambiente local do ambiente de produção, foram utilizadas variáveis de ambiente.

#### Auth Service

```text
DATABASE_URL
FRONTEND_URL
PYTHON_VERSION
```

#### Academic Service

```text
DATABASE_URL
AUTH_SERVICE_URL
FRONTEND_URL
PYTHON_VERSION
```

#### Frontend

```text
VITE_AUTH_API_URL
VITE_ACADEMIC_API_URL
```

### Como testar o sistema online

1. Acessar o frontend: https://academic-devops-platform.onrender.com
2. Criar um cadastro.
3. Fazer login.
4. Atualizar a lista de cursos.
5. Criar um novo curso.
6. Verificar se o curso aparece na lista.

Também é possível testar diretamente os serviços:

```bash
curl https://auth-service-9bwb.onrender.com/health
curl https://academic-service-71ed.onrender.com/health
```

Teste de rota protegida sem token:

```bash
curl https://academic-service-71ed.onrender.com/courses
```

Resposta esperada:

```json
{
  "detail": "Token ausente"
}
```

Teste de rota protegida com token:

```bash
curl -X GET https://academic-service-71ed.onrender.com/courses \
-H "Authorization: Bearer token-jwt-simulado-12345"
```

### Resultado da Sprint 3

Com essa etapa, a aplicação passou a contar com deploy externo, banco de dados gerenciado, variáveis de ambiente, logs, health checks e métricas básicas, aproximando o projeto de uma arquitetura DevOps mais completa.
