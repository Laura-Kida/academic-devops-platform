from fastapi import FastAPI

app = FastAPI(title="Academic Service")

@app.get("/")
def root():
    return {"service": "academic-service"}

@app.get("/courses")
def get_courses():
    return [
        {"id": 1, "name": "Engenharia da Computação"},
        {"id": 2, "name": "Ciência da Computação"},
        {"id": 3, "name": "Sistemas de Informação"}
    ]
