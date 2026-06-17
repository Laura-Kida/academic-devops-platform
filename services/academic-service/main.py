from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from schemas import CourseCreate
from database import engine, get_db
from models import Base, Course
from auth_client import validate_token


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academic Service")

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


def verify_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token ausente"
        )

    token = authorization.replace("Bearer ", "")

    result = validate_token(token)

    if not result.get("valid"):
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return True


@app.get("/")
def root():
    return {"service": "academic-service"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "academic-service"
    }


@app.get("/courses")
def get_courses(
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    return db.query(Course).all()


@app.post("/courses")
def create_course(
    course: CourseCreate,
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    new_course = Course(name=course.name)

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    user=Depends(verify_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )