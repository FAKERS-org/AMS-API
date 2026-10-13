from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta


class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)


class DepartmentCreate(DepartmentBase):
    slug: str | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    slug: str | None = None


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    slug: str | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.slug and self.name:
            self.slug = self.name.lower().replace(" ", "-")


class DepartmentDetailRead(DepartmentRead):
    total_courses: int = 0
    total_faculty: int = 0
    total_students: int = 0


class DepartmentPagination(BaseModel):
    data: list[DepartmentRead]
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
