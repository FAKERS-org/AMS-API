from app.core.exceptions import AppException
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo

    async def list_public(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        year_level: int | None = None,
    ):
        return await self.repo.get_public_list(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            year_level=year_level,
        )

    async def get_public_by_id(self, student_id: int):
        student = await self.repo.get_public_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")
        return student

    async def create(self, data: StudentCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, student_id: int, data: StudentUpdate):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")
        return await self.repo.update(student, data.model_dump(exclude_unset=True))

    async def delete(self, student_id: int):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")
        await self.repo.delete(student)

