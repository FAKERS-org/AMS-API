from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hashed_password,
    verify_password,
)
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse, UserProfileResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise AppException(status_code=401, detail="Invalid email or password")

        if user.is_active is False:
            raise AppException(status_code=403, detail="User account is inactive")

        return TokenResponse(
            access_token=create_access_token(
                user.id, extra={"role": user.role.value}
            ),
            refresh_token=create_refresh_token(user.id),
        )

    async def register_user(
        self, email: str, password: str, full_name: str
    ) -> TokenResponse:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise AppException(status_code=409, detail="Email already registered")

        new_user = await self.user_repository.create(
            {
                "email": email,
                "hashed_password": hashed_password(password),
                "full_name": full_name,
                "role": Role.STUDENT,
                "is_active": True,
            }
        )

        return TokenResponse(
            access_token=create_access_token(
                new_user.id, extra={"role": new_user.role.value}
            ),
            refresh_token=create_refresh_token(new_user.id),
        )

    async def refresh_tokens(self, refresh_token_str: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token_str)
            if payload.get("type") != "refresh":
                raise ValueError
            user_id = int(payload["sub"])
        except Exception:
            raise AppException(status_code=401, detail="Invalid or expired refresh token")

        user = await self.user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise AppException(status_code=401, detail="User account not found or inactive")

        return TokenResponse(
            access_token=create_access_token(
                user.id, extra={"role": user.role.value}
            ),
            refresh_token=create_refresh_token(user.id),
        )

    async def get_profile(self, user: User) -> UserProfileResponse:
        # Check if student or faculty profile exists
        db = self.user_repository.db

        student_res = await db.execute(select(Student.id).where(Student.user_id == user.id))
        student_id = student_res.scalar_one_or_none()

        faculty_res = await db.execute(select(Faculty.id).where(Faculty.user_id == user.id))
        faculty_id = faculty_res.scalar_one_or_none()

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            student_id=student_id,
            faculty_id=faculty_id,
        )
