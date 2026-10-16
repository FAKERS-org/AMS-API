from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    currentPage: int
    perPage: int
    totalPages: int
    totalItems: int


class Response(BaseModel, Generic[T]):
    success: bool
    data: list[T]
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