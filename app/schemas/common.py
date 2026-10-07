from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    success: bool
    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int