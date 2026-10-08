from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.partner import PartnerRepository
from app.schemas.partner import PartnerPagination, PartnerRead
from app.services.partner_service import PartnerService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> PartnerService:
    return PartnerService(PartnerRepository(db))


@router.get("", response_model=PartnerPagination)
async def list_public_partners(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    partner_type: str | None = Query(None),
    service: PartnerService = Depends(_service),
):
    return await service.list_active(
        page=page,
        page_size=page_size,
        search=search,
        partner_type=partner_type,
    )


@router.get("/{partner_id}", response_model=PartnerRead)
async def get_public_partner(
    partner_id: int,
    service: PartnerService = Depends(_service),
):
    return await service.get_active_by_id(partner_id)

