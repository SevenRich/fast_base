import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, BigInteger, SmallInteger, Text, JSON, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .db import Base


if TYPE_CHECKING:
    from .company import Company


class CodeRelevanceEnum(enum.Enum):
    before = 1
    after = 2


class CodeTypeEnum(enum.Enum):
    standard = 1
    group = 2


class CodeStatusEnum(enum.Enum):
    wait = 0
    begin = 1
    done = 2
    cancel = 3
    fail = 4


class CodeOrder(Base):
    __tablename__ = 'orders'
    
    id = Column(BigInteger, primary_key=True, index=True)
    code_sn = Column(String(64), unique=True, index=True, comment='生码编号')
    batch_sn = Column(String(64), unique=True, index=True, comment='码批次')
    counts = Column(Numeric, nullable=True, default=1, comment='生码量')
    company_code = Column(String(64), ForeignKey('companies.company_code'), comment='商户名称')
    relevance_type = Column(SmallInteger(), default=1, comment='关联 before 1 前关联 after 2 后关联')
    code_type = Column(SmallInteger(), default=1, comment='码类型 standard 1 标准码 group 2 套标')
    """
    生码规则配置:
        # code_type 1 全数字 2 全字母 3 数字字母
        # type 1 数字码随机数字  2 数字码顺序流水号 3 乱码
        'big_code': {'status': 0, 'type': 1, 'code_type': 1, 'length': 6},
        'middle_code': {'status': 0, 'type': 1, 'code_type': 1, 'length': 7},
        'small_code': {'status': 1, 'type': 1, 'code_type': 1, 'length': 8},
        'security_code': {'status': 1, 'type': 1, 'code_type': 3, 'length': 8},
        'verify_code': {'status': 1, 'type': 1, 'code_type': 1, 'length': 4},
    """
    code_config = Column(Text(), comment='生码规则配置')
    status = Column(SmallInteger(), default=0, comment='生码状态 wait 0 等待 begin 1 开始 done 2 完成 cancel 3 取消 fail 4 失败')
    url_prefix = Column(String(500), comment='Url 前缀')
    """
    导出规则：
        'url': {
            'status': 1,
            'format': '{url_prefix}/{batch_sn}-{security_code}'
        },
        'query': {
            'status': 1,
            'list': ['small_code', 'url', 'verify_code']
        }
    """
    export_config = Column(Text(), comment='导出码配置')
    export_key = Column(String(500), comment='导码密钥')
    
    created_at = Column(DateTime(), default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='更新时间')
 
    def __repr__(self):
        return "<%s orders.code_sn: %s %s>" % (self.id, self.code_sn, self.company_code)
