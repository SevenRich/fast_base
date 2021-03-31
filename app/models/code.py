
from sqlalchemy import Table, MetaData

from .db import Base, engine, SessionLocal

class Code(Base):
    
    table_name = 'code_first'
    
    __table__ = Table(table_name, MetaData(bind=engine), autoload=True)
    