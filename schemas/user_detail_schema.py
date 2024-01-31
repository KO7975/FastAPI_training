from pydantic import BaseModel
from typing import Optional


class UserDetailBase(BaseModel):
    adress: Optional[str]
    phone: Optional[str]


class UserDetailCreate(UserDetailBase):
    user_id: int


class UserDetail(UserDetailBase):
    id: int
    user_id: int

    class Config:
        from_atributes = True


class UserDetailInDB(UserDetail):
    class Config:
        from_atributes = True