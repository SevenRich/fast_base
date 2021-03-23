from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    
    
class RoleInDBBase(RoleBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Role(RoleInDBBase):
    pass
