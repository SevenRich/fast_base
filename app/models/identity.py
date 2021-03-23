from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .db import Base


class Identity(Base):
    __tablename__ = 'identities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, comment='权限 name')
    desc = Column(String(64), comment='权限描述')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
    def __repr__(self):
        return "<%s identities.name: %s>" % (self.id, self.name)
