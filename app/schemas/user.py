from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.permissions import Role


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool
    name: str | None = None
    status: bool | None = None
    avatar: str | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.full_name
        if self.status is None:
            self.status = self.is_active


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    full_name: str | None = None
    name: str | None = None
    role: Role = Role.STUDENT
    role_id: int | None = None
    status: bool | None = None
    avatar: str | None = None

    def model_post_init(self, __context):
        if not self.full_name and self.name:
            self.full_name = self.name
        elif not self.full_name:
            self.full_name = self.email.split("@")[0]

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return password


class UserUpdate(BaseModel):
    full_name: str | None = None
    name: str | None = None
    role: Role | None = None
    role_id: int | None = None
    is_active: bool | None = None
    status: bool | None = None
    avatar: str | None = None

    def model_post_init(self, __context):
        if not self.full_name and self.name:
            self.full_name = self.name
        if self.is_active is None and self.status is not None:
            self.is_active = self.status


class UserPage(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    page_size: int
    total_pages: int
