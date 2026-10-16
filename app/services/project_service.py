from app.core.exceptions import AppException
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "title", "label": "Title", "type": "text"},
            {"value": "partner", "label": "Partner", "type": "text"},
            {"value": "duration", "label": "Duration", "type": "text"},
            {"value": "funding", "label": "Funding", "type": "text"},
            {"value": "faculties", "label": "Faculties", "type": "text"},
            {"value": "students", "label": "Students", "type": "text"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Project",
            "fields": [
                {"name": "title", "value": "title", "type": "text", "label": "Title", "is_required": True},
                {"name": "partner", "value": "partner", "type": "text", "label": "Partner"},
                {"name": "duration", "value": "duration", "type": "text", "label": "Duration"},
                {"name": "funding", "value": "funding", "type": "text", "label": "Funding"},
                {"name": "investigators", "value": "investigators", "type": "text", "label": "Faculties"},
                {"name": "students", "value": "students", "type": "text", "label": "Students"},
                {"name": "description", "value": "description", "type": "textarea", "label": "Description"},
            ],
        }

    async def list_published(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        status: str | None = None,
    ):
        return await self.repo.get_published(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
        )

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        status: str | None = None,
        is_published: bool | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            is_published=is_published,
        )

    async def get_published_by_id(self, project_id: int):
        project = await self.repo.get_published_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        return project

    async def get_by_id(self, project_id: int):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        return project

    async def view(self, project_id: int):
        return await self.get_by_id(project_id)

    async def create(self, data: ProjectCreate):
        dump = data.model_dump()
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "partner", "duration", "funding", "investigators", "students", "status", "is_published"}
        }
        return await self.repo.create(filtered)

    async def update(self, project_id: int, data: ProjectUpdate):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        dump = data.model_dump(exclude_unset=True)
        filtered = {
            k: v
            for k, v in dump.items()
            if k in {"title", "description", "partner", "duration", "funding", "investigators", "students", "status", "is_published"}
        }
        return await self.repo.update(project, filtered)

    async def delete(self, project_id: int):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        await self.repo.delete(project)
