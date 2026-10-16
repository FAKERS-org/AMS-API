from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    login: str | None = None
    password: str

    @model_validator(mode="after")
    def check_email_or_login(self):
        if not self.email and not self.login:
            raise ValueError("Either email or login must be provided")
        return self

    @property
    def identifier(self) -> str:
        return str(self.email or self.login)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    full_name: str

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return password


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    accessToken: str | None = None
    refreshToken: str | None = None

    model_config = {"populate_by_name": True}

    def model_post_init(self, __context):
        if not self.accessToken:
            self.accessToken = self.access_token
        if not self.refreshToken:
            self.refreshToken = self.refresh_token


class RefreshRequest(BaseModel):
    refresh_token: str | None = None
    refreshToken: str | None = None

    @property
    def token_value(self) -> str | None:
        return self.refresh_token or self.refreshToken


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    student_id: int | None = None
    faculty_id: int | None = None

    model_config = {"from_attributes": True}
