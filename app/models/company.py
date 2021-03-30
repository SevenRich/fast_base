from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import relationship

from .db import Base


if TYPE_CHECKING:
    from .order import CodeOrder

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    uuid_code = Column(String(64), index=True, comment='生码系统编号')
    company_code = Column(String(64), unique=True, index=True, comment='商户编号')
    company_name = Column(String(64), comment='商户名称')
    company_full_name = Column(String(128), comment='公司名称')
    code_table_name = Column(String(64), comment='商户码表')
    is_active = Column(Boolean(), default=True, comment='激活状态')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    code_orders = relationship("CodeOrder")
 
    def __repr__(self):
        return "<%s companies.company_name: %s %s>" % (self.id, self.uuid_code, self.company_name)
