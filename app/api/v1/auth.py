from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()

def _service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, service: AuthService = Depends(_service)):
    return await service.authenticate(request.email, request.password)

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, service: AuthService = Depends(_service)):
    return await service.register_user(
        request.email, request.password, request.full_name
    )
