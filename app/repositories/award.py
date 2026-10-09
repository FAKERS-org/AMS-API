import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.award import Award
from app.repositories.base import BaseRepository


class AwardRepository(BaseRepository[Award]):
    def __init__(self, db: AsyncSession):
        super().__init__(Award, db)

    async def get_published(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        base = select(Award).where(Award.is_published.is_(True))

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    Award.title.ilike(search_pattern),
                    Award.description.ilike(search_pattern),
                    Award.achievement.ilike(search_pattern),
                    Award.recipient_name.ilike(search_pattern),
                )
            )

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(Award.created_at.desc())
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

    async def get_published_by_id(self, award_id: int) -> Award | None:
        stmt = select(Award).where(
            Award.id == award_id,
            Award.is_published.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

