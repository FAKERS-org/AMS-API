from app.core.exceptions import AppException
from app.repositories.award import AwardRepository
from app.schemas.award import AwardCreate, AwardUpdate


class AwardService:
    def __init__(self, repo: AwardRepository):
        self.repo = repo

    async def list_published(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        return await self.repo.get_published(
            page=page,
            page_size=page_size,
            search=search,
        )

    async def get_published_by_id(self, award_id: int):
        award = await self.repo.get_published_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        return award

    async def create(self, data: AwardCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, award_id: int, data: AwardUpdate):
        award = await self.repo.get_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        return await self.repo.update(award, data.model_dump(exclude_unset=True))

    async def delete(self, award_id: int):
        award = await self.repo.get_by_id(award_id)
        if not award:
            raise AppException(404, "Award not found")
        await self.repo.delete(award)

