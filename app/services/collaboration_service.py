from app.core.exceptions import AppException
from app.repositories.collaboration import CollaborationRepository
from app.schemas.collaboration import CollaborationCreate, CollaborationUpdate


class CollaborationService:
    def __init__(self, repo: CollaborationRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "title", "label": "Title", "type": "text"},
            {"value": "duration", "label": "Duration", "type": "text"},
            {"value": "funding", "label": "Funding", "type": "text"},
            {"value": "tag", "label": "Tag", "type": "text"},
            {"value": "image", "label": "Image", "type": "image"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Collaboration",
            "fields": [
                {"name": "title", "value": "title", "type": "text", "label": "Title", "is_required": True},
                {"name": "duration", "value": "duration", "type": "text", "label": "Duration"},
                {"name": "funding", "value": "funding", "type": "text", "label": "Funding"},
                {"name": "tag", "value": "tag", "type": "text", "label": "Tag"},
                {"name": "image", "value": "image", "type": "image", "label": "Image"},
                {"name": "url", "value": "url", "type": "text", "label": "URL"},
                {"name": "objective", "value": "objective", "type": "textarea", "label": "Objective"},
                {"name": "description", "value": "description", "type": "textarea", "label": "Description"},
            ],
        }

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

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        is_published: bool | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            is_published=is_published,
        )

    async def get_published_by_id(self, collaboration_id: int):
        collab = await self.repo.get_published_by_id(collaboration_id)
        if not collab:
            raise AppException(404, "Collaboration not found")
        return collab

    async def get_by_id(self, collaboration_id: int):
        collab = await self.repo.get_by_id(collaboration_id)
        if not collab:
            raise AppException(404, "Collaboration not found")
        return collab

    async def view(self, collaboration_id: int):
        return await self.get_by_id(collaboration_id)

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
