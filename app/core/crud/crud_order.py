import json
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from fastapi.encoders import jsonable_encoder

from ...utils.security import create_md5_string
from ...utils import common
from .base import CRUDBase
from ...models import CodeOrderModel
from ..schemes.response import OrderCreate, OrderUpdate


class CRUDCodeOrder(CRUDBase[CodeOrderModel, OrderCreate, OrderUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[CodeOrderModel]:
        return db.query(CodeOrderModel).filter(CodeOrderModel.code_sn == code).first()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[CodeOrderModel]:
        return db.query(CodeOrderModel).filter(CodeOrderModel.equipment_name == name).first()
    
    def get_max_batch_sn(self, db: Session, *, field: str) -> Optional[CodeOrderModel]:
        return db.query(CodeOrderModel).order_by(desc(CodeOrderModel.batch_sn)).first()
    
    def create(self, db: Session, *, obj_in: OrderCreate) -> CodeOrderModel:
        """ 
        生码批次规则：
            a0000 => 655360  fffff => 1048575 == 393215
            a00000 => 10485760 ffffff => 16777215 == 6291455
        """
        start_num = 10485760
        info = self.get_max_batch_sn(db, field='batch_sn')
        if info is not None:
            start_num = int(info.batch_sn) + 1
        
        db_obj = CodeOrderModel(
            company_code=obj_in.company_code, # 商户名称
            code_sn=common.create_order_sn(), # 生码编号
            relevance_type=obj_in.relevance_type,  # 关联 before 1 前关联 after 2 后关联
            code_type=obj_in.code_type,  # 码类型 standard 1 标准码 group 2 套标
            batch_sn=start_num, # 码批次
            counts=obj_in.counts, # 码量
            status=0,
            url_prefix=obj_in.url_prefix, # Url 前缀
            export_key=create_md5_string(obj_in.export_key), # 导码密钥 忘记密码所有码不可找回
            code_config=json.dumps(jsonable_encoder(obj_in.code_config)),
            export_config=json.dumps(jsonable_encoder(obj_in.export_config)),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: CodeOrderModel, obj_in: Union[OrderUpdate, Dict[str, Any]]
    ) -> CodeOrderModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

order = CRUDCodeOrder(CodeOrderModel)
