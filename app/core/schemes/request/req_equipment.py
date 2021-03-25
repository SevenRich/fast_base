from typing import Optional

from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    equipment_code: str
    equipment_name: str
    equipment_desc: Optional[str] = None
    remarks: Optional[str] = None
    is_active: Optional[bool] = True


class EquipmentUpdate(BaseModel):
    equipment_name: str
    equipment_desc: Optional[str] = None
    remarks: Optional[str] = None
    is_active: Optional[bool] = True
