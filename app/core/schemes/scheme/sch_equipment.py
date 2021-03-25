from typing import Optional

from pydantic import BaseModel


class EquipmentBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
class EquipmentCreate(EquipmentBase):
    name: str
    desc: Optional[str] = None


# Properties to receive via API on update
class EquipmentUpdate(EquipmentBase):
    name: str
    desc: Optional[str] = None
    
    
class EquipmentInDBBase(EquipmentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Equipment(EquipmentInDBBase):
    pass
