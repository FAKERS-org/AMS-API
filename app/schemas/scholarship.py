from datetime import datetime
from pydantic import BaseModel


class ScholarshipContact(BaseModel):
    office: str | None = None
    email: str | None = None
    phone: str | None = None


class ScholarshipRead(BaseModel):
    id: int
    title: str
    description: str | None
    amount: str | None
    duration: str | None
    eligibility: str | None
    application_process: str | None
    contact_office: str | None
    contact_email: str | None
    contact_phone: str | None
    deadline: datetime | None
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ScholarshipCreate(BaseModel):
    title: str
    description: str | None = None
    amount: str | None = None
    duration: str | None = None
    eligibility: str | None = None
    application_process: str | None = None
    contact_office: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    deadline: datetime | None = None
    is_published: bool = True


class ScholarshipUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    amount: str | None = None
    duration: str | None = None
    eligibility: str | None = None
    application_process: str | None = None
    contact_office: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    deadline: datetime | None = None
    is_published: bool | None = None


class ScholarshipPagination(BaseModel):
    data: list[ScholarshipRead]
    total: int
    page: int
    page_size: int
    total_pages: int

