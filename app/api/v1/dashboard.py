from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.schemas.dashboard import DashboardOverviewResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    return DashboardService(db)


def _require_staff_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/overview", response_model=DashboardOverviewResponse)
async def get_dashboard_overview(
    service: DashboardService = Depends(_service),
    _actor: User = Depends(_require_staff_or_admin),
):
    return await service.get_overview()

