import math
from typing import Generic, TypeVar, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> ModelType | None:
        return await self.db.get(self.model, id)

    async def get_all(
        self, *, skip: int = 0, limit: int = 50
    ) -> Sequence[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_paginated(self, *, page: int = 1, page_size: int = 20):
        offset = (page - 1) * page_size
        count_stmt = select(func.count()).select_from(self.model)
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = select(self.model).offset(offset).limit(page_size)
        items = (await self.db.execute(stmt)).scalars().all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size),
        }

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.db.delete(db_obj)
        await self.db.flush()
