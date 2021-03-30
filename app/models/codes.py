from datetime import datetime

from sqlalchemy import Column, String, DateTime, BigInteger

from ..config import settings
from .db import Base, engine

def get_model(suffix):
    class CodeModel(Base):
        __tablename__ = '{code_prefix}_{suffix}'.format(code_prefix=settings.CODE_PREFIX, suffix=suffix)
        
        __table_args__ = {'extend_existing': True}
        
        id = Column(BigInteger, primary_key=True, autoincrement=True)
        code_sn = Column(String(64), comment='生码单号')
        batch_sn = Column(String(64), comment='生码批次')
        big_code = Column(String(64), comment='大标')
        middle_code = Column(String(64), comment='中标')
        small_code = Column(String(64), comment='小标 物流码 流水号 三码为一种码')
        security_code = Column(String(64), comment='二维码防伪码')
        verify_code = Column(String(64), comment='验证码')
        
        created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
        updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
        def __repr__(self):
            return "<%s codes.code_sn: %s>" % (self.id, self.code_sn)

    return CodeModel


def create_table(suffix):
    table_model = get_model(suffix);
    
    if engine.dialect.has_table(engine, table_model.__tablename__) is False:
        Base.metadata.create_all(engine)
    
    return True
