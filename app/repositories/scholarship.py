import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scholarship import Scholarship
from app.repositories.base import BaseRepository


class ScholarshipRepository(BaseRepository[Scholarship]):
    def __init__(self, db: AsyncSession):
        super().__init__(Scholarship, db)

    async def get_published(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        base = select(Scholarship).where(Scholarship.is_published.is_(True))

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    Scholarship.title.ilike(search_pattern),
                    Scholarship.description.ilike(search_pattern),
                )
            )

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(Scholarship.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        data = (await self.db.execute(stmt)).scalars().all()

        return {
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size) if total else 0,
        }

    async def get_published_by_id(self, scholarship_id: int) -> Scholarship | None:
        stmt = select(Scholarship).where(
            Scholarship.id == scholarship_id,
            Scholarship.is_published.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

