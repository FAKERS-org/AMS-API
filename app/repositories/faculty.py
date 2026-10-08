import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.faculty import Faculty
from app.models.relations.course_faculty import CourseFaculty
from app.models.user import User
from app.repositories.base import BaseRepository


class FacultyRepository(BaseRepository[Faculty]):
    def __init__(self, db: AsyncSession):
        super().__init__(Faculty, db)

    async def get_public_list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
    ):
        base = (
            select(Faculty)
            .join(Faculty.user)
            .outerjoin(Faculty.department)
            .where(Faculty.is_active.is_(True))
        )

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    User.full_name.ilike(search_pattern),
                    Faculty.specialization.ilike(search_pattern),
                )
            )

        if department_id is not None:
            base = base.where(Faculty.department_id == department_id)

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.options(joinedload(Faculty.user), joinedload(Faculty.department))
            .order_by(User.full_name.asc())
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

    async def get_public_by_id(self, faculty_id: int) -> Faculty | None:
        stmt = (
            select(Faculty)
            .options(
                joinedload(Faculty.user),
                joinedload(Faculty.department),
                selectinload(Faculty.course_assignments).joinedload(
                    CourseFaculty.course
                ),
            )
            .where(Faculty.id == faculty_id, Faculty.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

