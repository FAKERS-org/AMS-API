from app.core.exceptions import AppException
from app.repositories.announcement import AnnouncementRepository
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate


class AnnouncementService:
    def __init__(self, repo: AnnouncementRepository):
        self.repo = repo

    async def list_published(self, page: int = 1, page_size: int = 20):
        return await self.repo.get_published(page=page, page_size=page_size)

    async def create(self, data: AnnouncementCreate, author_id: int):
        return await self.repo.create(
            {**data.model_dump(), "author_id": author_id, "is_published": True}
        )

    async def update(self, announcement_id: int, data: AnnouncementUpdate):
        ann = await self.repo.get_by_id(announcement_id)
        if not ann:
            raise AppException(404, "Announcement not found")
        return await self.repo.update(ann, data.model_dump(exclude_unset=True))

    async def delete(self, announcement_id: int):
        ann = await self.repo.get_by_id(announcement_id)
        if not ann:
            raise AppException(404, "Announcement not found")
        await self.repo.delete(ann)
