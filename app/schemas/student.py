import time
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class PaginationMeta(BaseModel):
    currentPage: int
    perPage: int
    totalPages: int
    totalItems: int


class PublicStudentRead(BaseModel):
    id: int
    student_id_number: str
    full_name: str
    email: EmailStr
    department_name: str | None
    year_level: int
    created_at: datetime
    name: str | None = None
    major: str | None = None
    year: int | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.full_name
        if not self.major:
            self.major = self.department_name
        if not self.year:
            self.year = self.year_level


class StudentRead(BaseModel):
    id: int
    user_id: int
    student_id_number: str
    full_name: str
    email: EmailStr
    department_id: int | None
    department_name: str | None
    year_level: int
    date_of_birth: date | None
    created_at: datetime
    updated_at: datetime
    name: str | None = None
    major: str | None = None
    year: int | None = None
    photo: str | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.full_name
        if not self.major:
            self.major = self.department_name
        if not self.year:
            self.year = self.year_level


class StudentCreate(BaseModel):
    name: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    user_id: int | None = None
    student_id_number: str | None = None
    department_id: int | None = None
    major: str | None = None
    year: int | None = None
    year_level: int = 1
    date_of_birth: date | None = None
    photo: str | None = None

    def model_post_init(self, __context):
        if not self.full_name and self.name:
            self.full_name = self.name
        if not self.name and self.full_name:
            self.name = self.full_name
        if self.year and not self.year_level:
            self.year_level = self.year


class StudentUpdate(BaseModel):
    name: str | None = None
    full_name: str | None = None
    department_id: int | None = None
    major: str | None = None
    year: int | None = None
    year_level: int | None = None
    date_of_birth: date | None = None
    photo: str | None = None


class PublicStudentPagination(BaseModel):
    data: list[PublicStudentRead]
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


class StudentPagination(BaseModel):
    data: list[StudentRead]
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
