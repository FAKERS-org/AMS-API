from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectPagination, ProjectRead
from app.services.project_service import ProjectService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(ProjectRepository(db))


@router.get("", response_model=ProjectPagination)
async def list_public_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    status: str | None = Query(None),
    service: ProjectService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
    )


@router.get("/{project_id}", response_model=ProjectRead)
async def get_public_project(
    project_id: int,
    service: ProjectService = Depends(_service),
):
    return await service.get_published_by_id(project_id)

