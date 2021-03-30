from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ...utils.security import create_equipment_key
from .base import CRUDBase
from ...models import CompanyModel
from ..schemes.scheme import CompanyCreate, CompanyUpdate
from ...config import settings


class CRUDCompany(CRUDBase[CompanyModel, CompanyCreate, CompanyUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[CompanyModel]:
        return db.query(CompanyModel).filter(CompanyModel.company_code == code).first()
    
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[CompanyModel]:
        return db.query(CompanyModel).filter(CompanyModel.uuid_code == uuid).first()
    
    def create(self, db: Session, *, obj_in: CompanyCreate) -> CompanyModel:
        db_obj = CompanyModel(
            uuid_code=obj_in.uuid_code,
            company_code=obj_in.company_code,
            company_name=obj_in.company_name,
            company_full_name=obj_in.company_full_name,
            code_table_name='{code_prefix}_{suffix}'.format(code_prefix=settings.CODE_PREFIX, suffix=obj_in.uuid_code), # 创建码 table
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: CompanyModel, obj_in: Union[CompanyUpdate, Dict[str, Any]]
    ) -> CompanyModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

company = CRUDCompany(CompanyModel)
