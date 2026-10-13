import math
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty
from app.models.student import Student
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: AsyncSession):
        super().__init__(Department, db)

    async def get_by_name(self, name: str) -> Department | None:
        stmt = select(Department).where(func.lower(Department.name) == func.lower(name))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_departments(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        base = select(Department)

        if search:
            base = base.where(Department.name.ilike(f"%{search}%"))

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.order_by(Department.name.asc())
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

    async def get_with_counts(self, department_id: int) -> dict | None:
        dept = await self.get_by_id(department_id)
        if not dept:
            return None

        course_count = (
            await self.db.execute(
                select(func.count()).where(Course.department_id == department_id)
            )
        ).scalar_one()

        faculty_count = (
            await self.db.execute(
                select(func.count()).where(Faculty.department_id == department_id)
            )
        ).scalar_one()

        student_count = (
            await self.db.execute(
                select(func.count()).where(Student.department_id == department_id)
            )
        ).scalar_one()

        return {
            "id": dept.id,
            "name": dept.name,
            "created_at": dept.created_at,
            "updated_at": dept.updated_at,
            "total_courses": course_count,
            "total_faculty": faculty_count,
            "total_students": student_count,
        }

