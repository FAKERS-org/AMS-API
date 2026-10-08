from app.core.exceptions import AppException
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

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

    async def get_published_by_id(self, project_id: int):
        project = await self.repo.get_published_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        return project

    async def create(self, data: ProjectCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, project_id: int, data: ProjectUpdate):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        return await self.repo.update(project, data.model_dump(exclude_unset=True))

    async def delete(self, project_id: int):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise AppException(404, "Project not found")
        await self.repo.delete(project)

