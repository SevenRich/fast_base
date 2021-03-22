from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import get_password_hash, verify_password
from .base import CRUDBase
from ...models import UserModel
from ..schemes.scheme.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.username == username).first()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> UserModel:
        db_obj = UserModel(
            username=obj_in.username,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[UserModel]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        print(user.__dict__)
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: UserModel) -> bool:
        return user.is_active
    

user = CRUDUser(UserModel)
