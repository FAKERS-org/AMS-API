from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class PublicStudentRead(BaseModel):
    id: int
    student_id_number: str
    full_name: str
    email: EmailStr
    department_name: str | None
    year_level: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentCreate(BaseModel):
    user_id: int
    student_id_number: str
    department_id: int | None = None
    year_level: int = 1
    date_of_birth: date | None = None


class StudentUpdate(BaseModel):
    department_id: int | None = None
    year_level: int | None = None
    date_of_birth: date | None = None


class PublicStudentPagination(BaseModel):
    data: list[PublicStudentRead]
    total: int
    page: int
    page_size: int
    total_pages: int

