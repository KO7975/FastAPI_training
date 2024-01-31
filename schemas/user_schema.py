from pydantic import BaseModel, EmailStr
import models
from schemas.user_detail_schema import UserDetailBase


class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr
    # tags: list[str] = []
    

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserInDB(User):
    details: UserDetailBase | dict

    class Config:
        from_attributes = True
        exclude = ['password']