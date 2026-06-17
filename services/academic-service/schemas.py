from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str


class CourseResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True