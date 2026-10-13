from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.common import PaginationMeta


class StudentBrief(BaseModel):
    id: int
    student_id_number: str
    full_name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class CourseBrief(BaseModel):
    id: int
    code: str
    title: str
    credit_hours: int

    model_config = {"from_attributes": True}


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    student: StudentBrief | None = None
    course: CourseBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class EnrollmentPagination(BaseModel):
    data: list[EnrollmentRead]
    total: int
    page: int
    page_size: int
    total_pages: int
    meta: PaginationMeta | None = None

    def model_post_init(self, __context):
        if not self.meta:
            self.meta = PaginationMeta(
                currentPage=self.page,
                perPage=self.page_size,
                totalPages=self.total_pages,
                totalItems=self.total,
            )
