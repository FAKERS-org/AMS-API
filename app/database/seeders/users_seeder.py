from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.permissions import Role
from app.core.security import hashed_password
from app.database.base import BaseSeeder


class UserSeeder(BaseSeeder):
    name = "UserSeeder"

    async def run(self) -> int:
        data = self.load_json("users.json")
        created = 0

        for item in data:
            existing = await self.db.execute(
                select(User).where(User.email == item["email"])
            )
            if existing.scalar_one_or_none():
                self.log(f"⏭  Skipped (exists): {item['email']}")
                continue

            user = User(
                email=item["email"],
                hashed_password=hashed_password(item["password"]),
                full_name=item["full_name"],
                role=Role(item.get("role", "student")),
                is_active=True,
            )
            self.db.add(user)
            created += 1
            self.log(f"✅ Created user: {item['email']}")

        await self.db.flush()

        all_users = (await self.db.execute(select(User))).scalars().all()
        self.context["users_by_email"] = {u.email: u.id for u in all_users}

        return created