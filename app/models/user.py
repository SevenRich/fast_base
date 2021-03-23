from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from .db import Base


if TYPE_CHECKING:
    from .role import Role
    
    
useridToRoleid = Table('user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, unique=True, comment='用户名')
    password = Column(String(120), nullable=False, comment='密码')
    email = Column(String(120), nullable=False, unique=True, comment='Email')
    is_active = Column(Boolean(), default=True, comment='激活状态')
    is_superuser = Column(Boolean(), default=True, comment='超级管理员')
    access_token = Column(String(300), nullable=True, comment='access token')
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
    roles = relationship('Role', secondary=useridToRoleid, backref='users')
 
    def __repr__(self):
        return "<%s users.username: %s>" % (self.id, self.username)
