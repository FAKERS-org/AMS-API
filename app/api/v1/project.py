from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectPagination, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(ProjectRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=ProjectPagination)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    is_published: bool | None = Query(None),
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        status=status_filter,
        is_published=is_published,
    )


@router.get("/{project_id}/view", response_model=ProjectRead)
async def view_project(
    project_id: int,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(project_id)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(project_id)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{project_id}", response_model=ProjectRead)
async def replace_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(project_id, data)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
