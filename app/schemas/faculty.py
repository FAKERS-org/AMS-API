from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.faculty import FacultyTitle
from app.models.relations.course_faculty import Semester, InstructorRole

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
    assigned_at: datetime

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


class FacultyCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    employee_id: str = Field(..., min_length=3, max_length=50)
    department_id: int
    title: FacultyTitle = FacultyTitle.ASSISTANT_PROFESSOR
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    hire_date: date


class FacultyUpdate(BaseModel):
    title: Optional[FacultyTitle] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


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

    model_config = {"from_attributes": True}


class PublicFacultyDetailRead(PublicFacultyRead):
    current_assignments: list[CourseFacultyRead] = Field(default_factory=list)


class PublicFacultyPagination(BaseModel):
    data: list[PublicFacultyRead]
    total: int
    page: int
    page_size: int
    total_pages: int

