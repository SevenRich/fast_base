from typing import Optional

from pydantic import BaseModel


class IdentityBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
class IdentityCreate(IdentityBase):
    name: str
    desc: Optional[str] = None


# Properties to receive via API on update
class IdentityUpdate(IdentityBase):
    name: str
    desc: Optional[str] = None
    
    
class IdentityInDBBase(IdentityBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Identity(IdentityInDBBase):
    pass
