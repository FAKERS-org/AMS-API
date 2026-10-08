from app.core.exceptions import AppException
from app.repositories.faculty import FacultyRepository


class FacultyService:
    def __init__(self, repo: FacultyRepository):
        self.repo = repo

    async def list_public(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
    ):
        return await self.repo.get_public_list(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
        )

    async def get_public_by_id(self, faculty_id: int):
        faculty = await self.repo.get_public_by_id(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")
        return faculty

