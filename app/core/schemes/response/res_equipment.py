from typing import Optional

from pydantic import BaseModel


class EquipmentBase(BaseModel):
    equipment_code: Optional[str] = None
    equipment_name: Optional[str] = None
    equipment_desc: Optional[str] = None
    remarks: Optional[str] = None
    is_active: Optional[bool] = True
    equipment_key: Optional[str] = None
    
    
class EquipmentInDBBase(EquipmentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Equipment(EquipmentInDBBase):
    pass
