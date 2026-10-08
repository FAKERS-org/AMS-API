from datetime import datetime
from pydantic import BaseModel


class AwardRead(BaseModel):
    id: int
    title: str
    description: str | None
    achievement: str | None
    imagepath: str | None
    recipient_name: str | None
    student_id: int | None
    award_date: datetime | None
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AwardCreate(BaseModel):
    title: str
    description: str | None = None
    achievement: str | None = None
    imagepath: str | None = None
    recipient_name: str | None = None
    student_id: int | None = None
    award_date: datetime | None = None
    is_published: bool = True


class AwardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    achievement: str | None = None
    imagepath: str | None = None
    recipient_name: str | None = None
    student_id: int | None = None
    award_date: datetime | None = None
    is_published: bool | None = None


class AwardPagination(BaseModel):
    data: list[AwardRead]
    total: int
    page: int
    page_size: int
    total_pages: int

