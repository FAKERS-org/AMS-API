import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.partner import Partner
from app.repositories.base import BaseRepository


class PartnerRepository(BaseRepository[Partner]):
    def __init__(self, db: AsyncSession):
        super().__init__(Partner, db)

    async def get_active(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        partner_type: str | None = None,
    ):
        base = select(Partner).where(Partner.is_active.is_(True))

        if partner_type:
            base = base.where(Partner.partner_type == partner_type)

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    Partner.name.ilike(search_pattern),
                    Partner.description.ilike(search_pattern),
                )
            )

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(Partner.name.asc())
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

    async def get_active_by_id(self, partner_id: int) -> Partner | None:
        stmt = select(Partner).where(
            Partner.id == partner_id,
            Partner.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

