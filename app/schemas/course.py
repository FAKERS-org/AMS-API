from datetime import datetime
from pydantic import BaseModel


class DepartmentBrief(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CourseRead(BaseModel):
    id: int
    code: str
    title: str
    description: str | None
    credit_hours: int
    department_id: int | None
    department: DepartmentBrief | None = None
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CoursePagination(BaseModel):
    data: list[CourseRead]
    total: int
    page: int
    page_size: int
    total_pages: int

