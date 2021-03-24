from typing import Optional, List

from pydantic import BaseModel, EmailStr

from .role_response import Role


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    
    role_id: Optional[int] = 4


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    
    # 关联角色
    roles: List[Role] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
