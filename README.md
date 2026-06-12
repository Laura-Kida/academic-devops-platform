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