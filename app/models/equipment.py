from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql.sqltypes import BigInteger

from .db import Base


class Equipment(Base):
    __tablename__ = 'equipments'
    
    id = Column(BigInteger(), primary_key=True, index=True)
    equipment_code = Column(String(64), unique=True, index=True, comment='设备编号')
    equipment_name = Column(String(64), comment='设备名称')
    equipment_desc = Column(String(125), comment='设备描述')
    remarks = Column(String(125), comment='备注')
    is_active = Column(Boolean(), default=True, comment='激活状态')
    equipment_key = Column(String(256), comment='通信密钥')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
    def __repr__(self):
        return "<%s equipments.equipment_name: %s>" % (self.id, self.equipment_name)
