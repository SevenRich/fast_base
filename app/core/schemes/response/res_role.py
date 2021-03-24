from typing import Optional, List

from pydantic import BaseModel

from .res_identity import Identity


class RoleBase(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    
    
    
    
class RoleInDBBase(RoleBase):
    id: Optional[int] = None
    
    # 关联角色
    identity: List[Identity] = []

    class Config:
        orm_mode = True
        
        
class Role(RoleInDBBase):
    pass
