from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import hashed_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def list_users(self, *, page: int = 1, page_size: int = 20):
        return await self.user_repository.get_paginated(
            page=page, page_size=page_size
        )

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise AppException(status_code=404, detail="User not found")
        return user

    async def create_user(self, data: UserCreate, actor: User) -> User:
        if await self.user_repository.get_by_email(str(data.email)):
            raise AppException(status_code=409, detail="Email already registered")

        if data.role in (Role.ADMIN, Role.SUPER_ADMIN) and actor.role != Role.SUPER_ADMIN:
            raise AppException(
                status_code=403,
                detail="Only a super admin can create admin accounts",
            )

        return await self.user_repository.create(
            {
                "email": str(data.email),
                "hashed_password": hashed_password(data.password),
                "full_name": data.full_name,
                "role": data.role,
                "is_active": True,
            }
        )

    async def update_user(
        self, user_id: int, data: UserUpdate, actor: User
    ) -> User:
        user = await self.get_user(user_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)

        if actor.role != Role.SUPER_ADMIN:
            if user.role == Role.SUPER_ADMIN:
                raise AppException(
                    status_code=403,
                    detail="Only a super admin can modify a super admin account",
                )
            if changes.get("role") in (Role.ADMIN, Role.SUPER_ADMIN):
                raise AppException(
                    status_code=403,
                    detail="Only a super admin can assign admin roles",
                )

        return await self.user_repository.update(user, changes)

    async def delete_user(self, user_id: int, actor: User) -> None:
        user = await self.get_user(user_id)
        if actor.id == user.id:
            raise AppException(status_code=400, detail="You cannot delete your own account")
        if actor.role != Role.SUPER_ADMIN and user.role in (
            Role.ADMIN,
            Role.SUPER_ADMIN,
        ):
            raise AppException(
                status_code=403,
                detail="Only a super admin can delete admin accounts",
            )
        await self.user_repository.delete(user)
