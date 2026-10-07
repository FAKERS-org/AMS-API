import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

JSON_DIR = Path(__file__).parent / "seeds"


class BaseSeeder(ABC):

    name: str = "BaseSeeder"

    def __init__(self, db: AsyncSession):
        self.db = db
        self.context: dict[str, Any] = {}

    @staticmethod
    def load_json(filename: str) -> list[dict]:
        file_path = JSON_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Seed file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @abstractmethod
    async def run(self) -> int:
        ...

    def log(self, message: str) -> None:
        print(f"  [{self.name}] {message}")