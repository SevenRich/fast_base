from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from .db import Base

if TYPE_CHECKING:
    from .identity import Identity


menuidToIdentityid = Table('menu_identity', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id')),
    Column('identity_id', Integer, ForeignKey('identities.id')),
)


class Menu(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, comment='菜单 name')
    desc = Column(String(64), comment='菜单描述')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    identities = relationship('Identity', secondary=menuidToIdentityid, backref='menus')
 
    def __repr__(self):
        return "<%s menus.name: %s>" % (self.id, self.name)
