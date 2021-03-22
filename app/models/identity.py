from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .db import Base

class Identity(Base):
    __tablename__ = 'identities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    desc = Column(String(64))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
 
    def __repr__(self):
        return "<%s identities.name: %s>" % (self.id, self.name)
