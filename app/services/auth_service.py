from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hashed_password,
    verify_password,
)

from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse

class AuthService:
    def __init__ (self, user_repository: UserRepository):
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
