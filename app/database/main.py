"""
Seed runner — executes all seeders in dependency order.

Usage:
    python -m seeds.main                  # Run all seeders
    python -m seeds.main --fresh          # Wipe DB first, then seed
    python -m seeds.main --only students  # Run only the student seeder
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Ensure project root is on sys.path so `app.*` imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine, AsyncSessionLocal
from app.database.seeders import users_seeder

SEEDER_CLASSES = [
    users_seeder.UserSeeder,
]

async def wipe_database() -> None:
    from app.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("🗑  Database wiped and recreated.\n")


async def run_seeder(seeder_cls, db: AsyncSession, context: dict) -> int:
    seeder = seeder_cls(db)
    seeder.context = context
    count = await seeder.run()
    context.update(seeder.context)
    return count


async def main(fresh: bool = False, only: str | None = None) -> None:
    print("\n" + "=" * 60)
    print("🌱  UNIVERSITY MANAGEMENT SYSTEM — SEEDER")
    print("=" * 60 + "\n")

    if fresh:
        await wipe_database()

    if only:
        seeders_to_run = [s for s in SEEDER_CLASSES if s.__name__.lower().startswith(only.lower())]
        if not seeders_to_run:
            print(f"❌ No seeder found matching '{only}'")
            return
    else:
        seeders_to_run = SEEDER_CLASSES

    shared_context: dict = {}
    total_created = 0

    async with AsyncSessionLocal() as db:
        try:
            for seeder_cls in seeders_to_run:
                print(f"▶ Running {seeder_cls.name}...")
                count = await run_seeder(seeder_cls, db, shared_context)
                total_created += count
                print(f"  → {count} record(s) created\n")

            await db.commit()
            print("=" * 60)
            print(f"✅  Seeding complete! Total records created: {total_created}")
            print("=" * 60 + "\n")

        except Exception as exc:
            await db.rollback()
            print(f"\n❌  Seeding failed: {exc}")
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run database seeders")
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Wipe and recreate all tables before seeding",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Run only a specific seeder (e.g., 'students', 'faculty')",
    )
    args = parser.parse_args()

    asyncio.run(main(fresh=args.fresh, only=args.only))