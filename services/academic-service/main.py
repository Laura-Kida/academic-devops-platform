import logging
import os

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from schemas import CourseCreate
from database import engine, get_db
from models import Base, Course
from auth_client import validate_token


# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - academic-service - %(levelname)s - %(message)s"
)

logger = logging.getLogger("academic-service")


# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)


# Inicialização da aplicação
app = FastAPI(title="Academic Service")


# Configuração de CORS
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exposição de métricas Prometheus em /metrics
Instrumentator().instrument(app).expose(app)


def verify_user(authorization: str = Header(None)):
    if not authorization:
        logger.warning("Acesso negado: token ausente")

        raise HTTPException(
            status_code=401,
            detail="Token ausente"
        )

    token = authorization.replace("Bearer ", "")

    result = validate_token(token)

    if not result.get("valid"):
        logger.warning("Acesso negado: token inválido")

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    logger.info("Token validado com sucesso pelo Academic Service")
    return True


@app.get("/")
def root():
    logger.info("Rota raiz acessada")

    return {"service": "academic-service"}


@app.get("/health")
def health():
    logger.info("Health check acessado")

    return {
        "status": "ok",
        "service": "academic-service"
    }


@app.get("/courses")
def get_courses(
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    logger.info("Listagem de cursos solicitada")

    courses = db.query(Course).all()

    logger.info(f"{len(courses)} cursos retornados")

    return courses


@app.post("/courses")
def create_course(
    course: CourseCreate,
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Tentativa de criação de curso: {course.name}")

    new_course = Course(name=course.name)

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    logger.info(
        f"Curso criado com sucesso: {new_course.name} | ID: {new_course.id}"
    )

    return new_course


@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Busca por curso ID: {course_id}")

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course:
        logger.info(f"Curso encontrado: {course.name}")
    else:
        logger.warning(f"Curso não encontrado. ID: {course_id}")

    return course