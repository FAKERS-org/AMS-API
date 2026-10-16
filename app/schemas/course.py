import time
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta


class DepartmentBrief(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CourseCreate(BaseModel):
    code: str | None = None
    code_name: str | None = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    credit_hours: int = 3
    credit: int | None = None
    department_id: int | None = None
    category_id: int | None = None
    semester: str | None = None
    year: int | None = None
    is_published: bool = True

    def model_post_init(self, __context):
        if not self.code and self.code_name:
            self.code = self.code_name
        elif not self.code:
            self.code = f"CRS{int(time.time() * 1000) % 100000:05d}"
        if self.credit is not None:
            self.credit_hours = self.credit
        if self.department_id is None and self.category_id is not None:
            self.department_id = self.category_id


class CourseUpdate(BaseModel):
    code: str | None = None
    code_name: str | None = None
    title: str | None = None
    description: str | None = None
    credit_hours: int | None = None
    credit: int | None = None
    department_id: int | None = None
    category_id: int | None = None
    semester: str | None = None
    year: int | None = None
    is_published: bool | None = None

    def model_post_init(self, __context):
        if not self.code and self.code_name:
            self.code = self.code_name
        if self.credit is not None and self.credit_hours is None:
            self.credit_hours = self.credit
        if self.department_id is None and self.category_id is not None:
            self.department_id = self.category_id


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
    category: str | None = None
    credit: int | None = None
    semester: str | None = "1"
    year: int | None = 1

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.category and self.department:
            self.category = self.department.name
        if self.credit is None:
            self.credit = self.credit_hours


class CoursePagination(BaseModel):
    data: list[CourseRead]
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
