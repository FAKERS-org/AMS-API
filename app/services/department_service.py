from app.core.exceptions import AppException
from app.repositories.department import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, repo: DepartmentRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "name", "label": "Name", "type": "text"},
            {"value": "slug", "label": "Slug", "type": "text"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Category",
            "fields": [
                {
                    "name": "name",
                    "value": "name",
                    "type": "text",
                    "label": "Name",
                    "is_required": True,
                },
                {
                    "name": "slug",
                    "value": "slug",
                    "type": "text",
                    "label": "Slug",
                    "is_required": False,
                },
            ],
        }

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        return await self.repo.list_departments(
            page=page,
            page_size=page_size,
            search=search,
        )

    async def get_by_id(self, department_id: int):
        dept = await self.repo.get_by_id(department_id)
        if not dept:
            raise AppException(404, "Department not found")
        return dept

    async def view(self, department_id: int):
        return await self.get_detail(department_id)

    async def get_detail(self, department_id: int):
        detail = await self.repo.get_with_counts(department_id)
        if not detail:
            raise AppException(404, "Department not found")
        return detail

    async def create(self, data: DepartmentCreate):
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise AppException(409, f"Department '{data.name}' already exists")
        return await self.repo.create({"name": data.name})

    async def update(self, department_id: int, data: DepartmentUpdate):
        dept = await self.get_by_id(department_id)

        update_dict = {}
        if data.name is not None:
            existing = await self.repo.get_by_name(data.name)
            if existing and existing.id != department_id:
                raise AppException(409, f"Department '{data.name}' already exists")
            update_dict["name"] = data.name

        if update_dict:
            await self.repo.update(dept, update_dict)
        return await self.get_by_id(department_id)

    async def delete(self, department_id: int):
        dept = await self.get_by_id(department_id)
        await self.repo.delete(dept)
