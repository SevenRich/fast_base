from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from .db import Base


if TYPE_CHECKING:
    from .identity import Identity


roleidToIdentityid = Table('role_identity', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('identity_id', Integer, ForeignKey('identities.id')),
)


class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    desc = Column(String(64))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
 
    identity = relationship('Identity', secondary=roleidToIdentityid, backref='roles')
 
    def __repr__(self):
        return "<%s roles.name: %s>" % (self.id, self.name)
    