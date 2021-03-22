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
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=True)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
 
    roles = relationship('Role', secondary=useridToRoleid, backref='users')
 
    def __repr__(self):
        return "<%s users.username: %s>" % (self.id, self.username)
