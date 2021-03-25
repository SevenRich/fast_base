from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class RoleBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    name: str


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    name: Optional[str] = None


class RoleInDBBase(RoleBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    pass
