from typing import Optional

from pydantic import BaseModel


class IdentityBase(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    
    
class IdentityInDBBase(IdentityBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Identity(IdentityInDBBase):
    pass
