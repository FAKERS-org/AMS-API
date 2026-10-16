from app.core.exceptions import AppException
from app.repositories.scholarship import ScholarshipRepository
from app.schemas.scholarship import ScholarshipCreate, ScholarshipUpdate


class ScholarshipService:
    def __init__(self, repo: ScholarshipRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "id", "label": "ID", "type": "number"},
            {"value": "name", "label": "Scholarship Name", "type": "text"},
            {"value": "description", "label": "Description", "type": "text"},
            {"value": "eligibility", "label": "Eligibility", "type": "text"},
            {"value": "application_process", "label": "Application Process", "type": "text"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Scholarship",
            "fields": [
                {"name": "title", "value": "title", "type": "text", "label": "Scholarship Name", "is_required": True},
                {"name": "description", "value": "description", "type": "textarea", "label": "Description"},
                {"name": "eligibility", "value": "eligibility", "type": "textarea", "label": "Eligibility"},
                {"name": "application_process", "value": "application_process", "type": "textarea", "label": "Application Process"},
                {"name": "amount", "value": "amount", "type": "text", "label": "Amount"},
                {"name": "duration", "value": "duration", "type": "text", "label": "Duration"},
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

    async def get_published_by_id(self, scholarship_id: int):
        scholarship = await self.repo.get_published_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        return scholarship

    async def get_by_id(self, scholarship_id: int):
        scholarship = await self.repo.get_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        return scholarship

    async def view(self, scholarship_id: int):
        return await self.get_by_id(scholarship_id)

    async def create(self, data: ScholarshipCreate):
        dump = data.model_dump()
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "amount", "duration", "eligibility", "application_process", "contact_office", "contact_email", "contact_phone", "deadline", "is_published"}
        }
        return await self.repo.create(filtered)

    async def update(self, scholarship_id: int, data: ScholarshipUpdate):
        scholarship = await self.repo.get_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        dump = data.model_dump(exclude_unset=True)
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "amount", "duration", "eligibility", "application_process", "contact_office", "contact_email", "contact_phone", "deadline", "is_published"}
        }
        return await self.repo.update(scholarship, filtered)

    async def delete(self, scholarship_id: int):
        scholarship = await self.repo.get_by_id(scholarship_id)
        if not scholarship:
            raise AppException(404, "Scholarship not found")
        await self.repo.delete(scholarship)
