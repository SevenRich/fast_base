from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import get_password_hash, verify_password
from .base import CRUDBase
from ...models import MenuModel
from ..schemes.scheme import MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[MenuModel, MenuCreate, MenuUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[MenuModel]:
        return db.query(MenuModel).filter(MenuModel.name == name).first()
    
    def create(self, db: Session, *, obj_in: MenuCreate) -> MenuModel:
        db_obj = MenuModel(
            name=obj_in.name,
            desc=obj_in.desc,
            parent_id=obj_in.parent_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: MenuModel, obj_in: Union[MenuUpdate, Dict[str, Any]]
    ) -> MenuModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

menu = CRUDMenu(MenuModel)
