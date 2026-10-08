from app.core.exceptions import AppException
from app.repositories.collaboration import CollaborationRepository
from app.schemas.collaboration import CollaborationCreate, CollaborationUpdate


class CollaborationService:
    def __init__(self, repo: CollaborationRepository):
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

    async def get_published_by_id(self, collaboration_id: int):
        collab = await self.repo.get_published_by_id(collaboration_id)
        if not collab:
            raise AppException(404, "Collaboration not found")
        return collab

    async def create(self, data: CollaborationCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, collaboration_id: int, data: CollaborationUpdate):
        collab = await self.repo.get_by_id(collaboration_id)
        if not collab:
            raise AppException(404, "Collaboration not found")
        return await self.repo.update(collab, data.model_dump(exclude_unset=True))

    async def delete(self, collaboration_id: int):
        collab = await self.repo.get_by_id(collaboration_id)
        if not collab:
            raise AppException(404, "Collaboration not found")
        await self.repo.delete(collab)

