from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import create_equipment_key
from .base import CRUDBase
from ...models import EquipmentModel
from ..schemes.scheme import EquipmentCreate, EquipmentUpdate


class CRUDEquipment(CRUDBase[EquipmentModel, EquipmentCreate, EquipmentUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[EquipmentModel]:
        return db.query(EquipmentModel).filter(EquipmentModel.equipment_code == code).first()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[EquipmentModel]:
        return db.query(EquipmentModel).filter(EquipmentModel.equipment_name == name).first()
    
    def create(self, db: Session, *, obj_in: EquipmentCreate) -> EquipmentModel:
        db_obj = EquipmentModel(
            equipment_code=obj_in.equipment_code,
            equipment_name=obj_in.equipment_name,
            equipment_desc=obj_in.equipment_desc,
            remarks=obj_in.remarks,
            is_active=obj_in.is_active,
            equipment_key=create_equipment_key(obj_in.equipment_code), # 创建设备 secret key
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: EquipmentModel, obj_in: Union[EquipmentUpdate, Dict[str, Any]]
    ) -> EquipmentModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

equipment = CRUDEquipment(EquipmentModel)
