from datetime import datetime

from sqlalchemy import Column, String, DateTime

from .db import Base


class Company(Base):
    __tablename__ = 'companies'
    
    uuid_code = Column(String(64), primary_key=True, index=True, comment='生码系统编号')
    company_code = Column(String(64), unique=True, index=True, comment='商户编号')
    company_name = Column(String(64), comment='商户名称')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
    def __repr__(self):
        return "<%s companies.company_name: %s %s>" % (self.id, self.uuid_code, self.company_name)
