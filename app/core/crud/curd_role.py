from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import get_password_hash, verify_password
from .base import CRUDBase
from ...models import RoleModel
from ..schemes.scheme import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[RoleModel, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[RoleModel]:
        return db.query(RoleModel).filter(RoleModel.name == name).first()

    def create(self, db: Session, *, obj_in: RoleCreate) -> RoleModel:
        db_obj = RoleModel(
            name=obj_in.name,
            desc=obj_in.desc,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: RoleModel, obj_in: Union[RoleUpdate, Dict[str, Any]]
    ) -> RoleModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

role = CRUDRole(RoleModel)
