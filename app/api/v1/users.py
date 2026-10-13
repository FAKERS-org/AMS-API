from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserPage, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN)(current_user)


class UpdatePasswordDto(BaseModel):
    oldPassword: str
    newPassword: str


class UpdateRoleDto(BaseModel):
    role_id: int


@router.get("", response_model=list[UserRead] | UserPage)
async def list_users(
    paginate: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: UserService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    if paginate:
        result = await service.list_users(page=page, page_size=page_size)
        return UserPage(
            **{
                **result,
                "items": [UserRead.model_validate(user) for user in result["items"]],
            }
        )
    users = await service.get_all()
    return [UserRead.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_user(user_id)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(_service),
    actor: User = Depends(_require_admin),
):
    return await service.create_user(data, actor)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(_service),
    actor: User = Depends(_require_admin),
):
    return await service.update_user(user_id, data, actor)


@router.patch("/{user_id}/password")
async def update_password(
    user_id: int,
    dto: UpdatePasswordDto,
    service: UserService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.update_password(user_id, dto.oldPassword, dto.newPassword)
    return {"message": "Password updated successfully"}


@router.patch("/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: int,
    dto: UpdateRoleDto,
    service: UserService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update_role(user_id, dto.role_id)


@router.get("/{user_id}/sessions")
async def get_user_sessions(
    user_id: int,
    _actor: User = Depends(_require_admin),
):
    return []


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(_service),
    actor: User = Depends(_require_admin),
):
    await service.delete_user(user_id, actor)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
