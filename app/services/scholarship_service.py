from app.core.exceptions import AppException
from app.repositories.scholarship import ScholarshipRepository
from app.schemas.scholarship import ScholarshipCreate, ScholarshipUpdate


class ScholarshipService:
    def __init__(self, repo: ScholarshipRepository):
        self.repo = repo

    async def list_published(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        return await self.repo.get_published(
            page=page,
            page_size=page_size,
            search=search,
        )

    async def get_published_by_id(self, scholarship_id: int):
        scholarship = await self.repo.get_published_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        return scholarship

    async def create(self, data: ScholarshipCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, scholarship_id: int, data: ScholarshipUpdate):
        scholarship = await self.repo.get_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        return await self.repo.update(scholarship, data.model_dump(exclude_unset=True))

    async def delete(self, scholarship_id: int):
        scholarship = await self.repo.get_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        await self.repo.delete(scholarship)

