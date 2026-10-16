import time
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.faculty import FacultyTitle
from app.models.relations.course_faculty import Semester, InstructorRole
from app.schemas.common import PaginationMeta


class CourseBrief(BaseModel):
    id: int
    code: str
    title: str
    credit_hours: int

    model_config = {"from_attributes": True}


class CourseFacultyRead(BaseModel):
    id: int
    course: CourseBrief
    academic_year: str
    semester: Semester
    section: str
    role: InstructorRole
    created_at: datetime | None = None
    assigned_at: datetime | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if self.assigned_at is None and self.created_at is not None:
            self.assigned_at = self.created_at
        elif self.created_at is None and self.assigned_at is not None:
            self.created_at = self.assigned_at


class FacultyRead(BaseModel):
    id: int
    employee_id: str
    title: FacultyTitle
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    hire_date: date
    is_active: bool

    user_id: int
    full_name: str
    email: EmailStr
    department_id: int
    department_name: Optional[str] = None

    current_assignments: list[CourseFacultyRead] = Field(default_factory=list)

    name: Optional[str] = None
    education: Optional[str] = None
    role: Optional[str] = None
    photo: Optional[str] = None
    courses: list[str] = Field(default_factory=list)
    ongoing_projects: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.full_name
        if not self.education:
            self.education = self.specialization or ""
        if not self.role:
            self.role = str(self.title)
        if not self.courses and self.current_assignments:
            self.courses = [a.course.title for a in self.current_assignments if a.course]


class FacultyCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    full_name: Optional[str] = None
    name: Optional[str] = None
    employee_id: Optional[str] = None
    department_id: Optional[int] = None
    title: FacultyTitle = FacultyTitle.ASSISTANT_PROFESSOR
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[date] = None

    def model_post_init(self, __context):
        if not self.full_name and self.name:
            self.full_name = self.name
        if not self.name and self.full_name:
            self.name = self.full_name


class FacultyUpdate(BaseModel):
    full_name: Optional[str] = None
    name: Optional[str] = None
    title: Optional[FacultyTitle] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    department_id: Optional[int] = None

    def model_post_init(self, __context):
        if not self.full_name and self.name:
            self.full_name = self.name


# ── Assignment schemas ──
class CourseFacultyCreate(BaseModel):
    course_id: int
    academic_year: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    semester: Semester
    section: str = "A"
    role: InstructorRole = InstructorRole.LEAD


class PublicFacultyRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    title: FacultyTitle
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    department_name: Optional[str] = None
    name: Optional[str] = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.full_name


class PublicFacultyDetailRead(PublicFacultyRead):
    current_assignments: list[CourseFacultyRead] = Field(default_factory=list)


class PublicFacultyPagination(BaseModel):
    data: list[PublicFacultyRead]
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


class FacultyPagination(BaseModel):
    data: list[FacultyRead]
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
