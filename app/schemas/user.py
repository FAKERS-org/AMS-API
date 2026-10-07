from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.permissions import Role


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    full_name: str
    role: Role = Role.STUDENT

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return password


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: Role | None = None
    is_active: bool | None = None


class UserPage(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    page_size: int
    total_pages: int
