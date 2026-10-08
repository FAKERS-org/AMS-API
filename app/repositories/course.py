import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.course import Course
from app.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: AsyncSession):
        super().__init__(Course, db)

    async def get_published(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
    ):
        base = select(Course).where(Course.is_published.is_(True))

        if search:
            search_filter = f"%{search}%"
            base = base.where(
                or_(
                    Course.title.ilike(search_filter),
                    Course.code.ilike(search_filter),
                )
            )

        if department_id is not None:
            base = base.where(Course.department_id == department_id)

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.options(selectinload(Course.department))
            .order_by(Course.code.asc())
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

    async def get_published_by_id(self, course_id: int) -> Course | None:
        stmt = (
            select(Course)
            .options(selectinload(Course.department))
            .where(Course.id == course_id, Course.is_published.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

