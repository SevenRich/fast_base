from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import get_password_hash, verify_password
from .base import CRUDBase
from ...models import IdentityModel
from ..schemes.scheme import IdentityCreate, IdentityUpdate


class CRUDIdentity(CRUDBase[IdentityModel, IdentityCreate, IdentityUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[IdentityModel]:
        return db.query(IdentityModel).filter(IdentityModel.name == name).first()
    
    def create(self, db: Session, *, obj_in: IdentityCreate) -> IdentityModel:
        db_obj = IdentityModel(
            name=obj_in.name,
            desc=obj_in.desc,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: IdentityModel, obj_in: Union[IdentityUpdate, Dict[str, Any]]
    ) -> IdentityModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

identity = CRUDIdentity(IdentityModel)
