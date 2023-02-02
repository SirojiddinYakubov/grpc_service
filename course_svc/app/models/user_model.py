from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field

from .base_model import BaseModel


class Roles(BaseModel, table=True):
    role_name: str
    display_name: str


class Permissions(BaseModel, table=True):
    permission_name: str
    display_name: str


class RolePermissions(BaseModel, table=True):
    role_id: int = Field(default=None, foreign_key="Roles.id")
    permission_id: int = Field(default=None, foreign_key="Permissions.id")


class Users(BaseModel, table=True):
    first_name: Optional[str]
    last_name: Optional[str]
    mobile: Optional[str]
    verified_at: Optional[datetime]
    email: EmailStr


class UserRoles(BaseModel, table=True):
    user_id: int = Field(default=None, foreign_key="Users.id")
    role_id: int = Field(default=None, foreign_key="Roles.id")
