from sqlalchemy import select

from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import hashed_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all(self):
        stmt = select(User).order_by(User.id.asc())
        result = await self.user_repository.db.execute(stmt)
        return result.scalars().all()

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

        full_name = data.full_name or data.name or str(data.email).split("@")[0]
        role_val = data.role
        if data.role_id:
            role_map = {1: Role.SUPER_ADMIN, 2: Role.ADMIN, 3: Role.FACULTY, 4: Role.STUDENT, 5: Role.STAFF}
            role_val = role_map.get(data.role_id, Role.STUDENT)

        return await self.user_repository.create(
            {
                "email": str(data.email),
                "hashed_password": hashed_password(data.password),
                "full_name": full_name,
                "role": role_val,
                "is_active": data.status if data.status is not None else True,
            }
        )

    async def update_user(
        self, user_id: int, data: UserUpdate, actor: User
    ) -> User:
        user = await self.get_user(user_id)
        changes = {}
        if data.full_name or data.name:
            changes["full_name"] = data.full_name or data.name
        if data.role is not None:
            changes["role"] = data.role
        elif data.role_id is not None:
            role_map = {1: Role.SUPER_ADMIN, 2: Role.ADMIN, 3: Role.FACULTY, 4: Role.STUDENT, 5: Role.STAFF}
            changes["role"] = role_map.get(data.role_id, user.role)
        if data.is_active is not None:
            changes["is_active"] = data.is_active
        elif data.status is not None:
            changes["is_active"] = data.status

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

    async def update_password(self, user_id: int, old_password: str, new_password: str) -> None:
        user = await self.get_user(user_id)
        if not verify_password(old_password, user.hashed_password):
            raise AppException(status_code=400, detail="Invalid old password")
        user.hashed_password = hashed_password(new_password)
        await self.user_repository.db.flush()

    async def update_role(self, user_id: int, role_id: int) -> User:
        user = await self.get_user(user_id)
        role_map = {1: Role.SUPER_ADMIN, 2: Role.ADMIN, 3: Role.FACULTY, 4: Role.STUDENT, 5: Role.STAFF}
        user.role = role_map.get(role_id, Role.STUDENT)
        await self.user_repository.db.flush()
        return user

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
