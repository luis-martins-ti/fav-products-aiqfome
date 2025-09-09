from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False


class UserOut(UserBase):
    id: int

    model_config = {"from_attributes": True}
