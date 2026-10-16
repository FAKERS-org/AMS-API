import math
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.student import Student
from app.models.user import User
from app.repositories.base import BaseRepository


class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: AsyncSession):
        super().__init__(Student, db)

    async def get_by_student_id_number(self, student_id_number: str) -> Student | None:
        stmt = select(Student).where(
            func.lower(Student.student_id_number) == func.lower(student_id_number)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Student | None:
        stmt = select(Student).where(Student.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_relations(self, student_id: int) -> Student | None:
        stmt = (
            select(Student)
            .options(joinedload(Student.user), joinedload(Student.department))
            .where(Student.id == student_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        year_level: int | None = None,
    ):
        base = select(Student).join(Student.user).outerjoin(Student.department)

        if department_id is not None:
            base = base.where(Student.department_id == department_id)

        if year_level is not None:
            base = base.where(Student.year_level == year_level)

        if search:
            search_pattern = f"%{search}%"
            base = base.where(
                or_(
                    User.full_name.ilike(search_pattern),
                    Student.student_id_number.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                )
            )

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.options(joinedload(Student.user), joinedload(Student.department))
            .order_by(Student.student_id_number.asc())
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

    async def get_public_list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        year_level: int | None = None,
    ):
        return await self.list_all(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            year_level=year_level,
        )

    async def get_public_by_id(self, student_id: int) -> Student | None:
        return await self.get_with_relations(student_id)
