from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class UserID(BaseUser):
    id: int = None

    class Config:
        orm_mode = True


class CreateUser(UserID):
    email: str
    hashed_password: str


class User(UserID):
    pass
