from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class LoginRequest(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    permissions: list


class UserDB(UserBase):
    id: int
    password_hash: str
    permissions: dict
    is_active: bool
    created_at: datetime


class UserOut(UserBase):
    id: int
    permissions: dict
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Permissions:
    CATALOGUE_READ = "catalogue:read"
    CATALOGUE_CREATE = "catalogue:create"
    CATALOGUE_UPDATE = "catalogue:update"
    CATALOGUE_DELETE = "catalogue:delete"

    ORDER_READ = "order:read"
    ORDER_CREATE = "order:create"
