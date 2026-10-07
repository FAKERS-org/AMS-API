from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement
from app.repositories.base import BaseRepository


class AnnouncementRepository(BaseRepository[Announcement]):
    def __init__(self, db: AsyncSession):
        super().__init__(Announcement, db)

    async def get_published(self, *, page: int = 1, page_size: int = 20):
        import math
        from sqlalchemy import func

        base = select(Announcement).where(Announcement.is_published.is_(True))

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(
                Announcement.is_pinned.desc(),
                Announcement.created_at.desc(),
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