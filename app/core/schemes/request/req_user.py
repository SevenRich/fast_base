from typing import Optional, List, Union, Set

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    
    
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    
    role_id: Optional[int] = 4


class UserUpdate(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    password: Optional[str] = None
    
    role_id: Optional[int] = 4
    
    