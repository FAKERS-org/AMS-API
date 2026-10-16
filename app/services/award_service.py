from app.core.exceptions import AppException
from app.repositories.award import AwardRepository
from app.schemas.award import AwardCreate, AwardUpdate


class AwardService:
    def __init__(self, repo: AwardRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "title", "label": "Title", "type": "text"},
            {"value": "achievement", "label": "Achievement", "type": "text"},
            {"value": "student", "label": "Student", "type": "text"},
            {"value": "image", "label": "Image", "type": "image"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Award",
            "fields": [
                {"name": "title", "value": "title", "type": "text", "label": "Title", "is_required": True},
                {"name": "achievement", "value": "achievement", "type": "text", "label": "Achievement"},
                {"name": "recipient_name", "value": "recipient_name", "type": "text", "label": "Student"},
                {"name": "imagepath", "value": "imagepath", "type": "image", "label": "Image"},
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

    async def get_published_by_id(self, award_id: int):
        award = await self.repo.get_published_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        return award

    async def get_by_id(self, award_id: int):
        award = await self.repo.get_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        return award

    async def view(self, award_id: int):
        return await self.get_by_id(award_id)

    async def create(self, data: AwardCreate):
        dump = data.model_dump()
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "achievement", "imagepath", "recipient_name", "student_id", "award_date", "is_published"}
        }
        return await self.repo.create(filtered)

    async def update(self, award_id: int, data: AwardUpdate):
        award = await self.repo.get_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        dump = data.model_dump(exclude_unset=True)
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "achievement", "imagepath", "recipient_name", "student_id", "award_date", "is_published"}
        }
        return await self.repo.update(award, filtered)

    async def delete(self, award_id: int):
        award = await self.repo.get_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        await self.repo.delete(award)
