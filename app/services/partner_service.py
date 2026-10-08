from app.core.exceptions import AppException
from app.repositories.partner import PartnerRepository
from app.schemas.partner import PartnerCreate, PartnerUpdate


class PartnerService:
    def __init__(self, repo: PartnerRepository):
        self.repo = repo

    async def list_active(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        partner_type: str | None = None,
    ):
        return await self.repo.get_active(
            page=page,
            page_size=page_size,
            search=search,
            partner_type=partner_type,
        )

    async def get_active_by_id(self, partner_id: int):
        partner = await self.repo.get_active_by_id(partner_id)
        if not partner:
            raise AppException(404, "Partner not found")
        return partner

    async def create(self, data: PartnerCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, partner_id: int, data: PartnerUpdate):
        partner = await self.repo.get_by_id(partner_id)
        if not partner:
            raise AppException(404, "Partner not found")
        return await self.repo.update(partner, data.model_dump(exclude_unset=True))

    async def delete(self, partner_id: int):
        partner = await self.repo.get_by_id(partner_id)
        if not partner:
            raise AppException(404, "Partner not found")
        await self.repo.delete(partner)

