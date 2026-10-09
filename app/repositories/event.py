import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, EventCategory
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, db: AsyncSession):
        super().__init__(Event, db)

    async def get_published(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        category: EventCategory | None = None,
    ):
        base = select(Event).where(Event.is_published.is_(True))

        if category is not None:
            base = base.where(Event.category == category)

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    Event.title.ilike(search_pattern),
                    Event.location.ilike(search_pattern),
                    Event.tag.ilike(search_pattern),
                )
            )

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(
                Event.published_date.desc().nullslast(),
                Event.created_at.desc(),
            )
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

    async def get_published_by_id(self, event_id: int) -> Event | None:
        stmt = select(Event).where(
            Event.id == event_id,
            Event.is_published.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

