from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, class_mapper, Query

from ..config import settings

class DbRoot(object):

    def __init__(self, **kwargs):
        """
        orm基础db对象，通过实例化该对象得到db实例，然后创建类对象继承自db.Model，便可以对相应表进行操作
        :param kwargs: dialect 数据库类型
                        driver 数据库驱动
                        user 用户名
                        password 用户密码
                        host 数据库地址
                        port 端口
                        database 数据库名
        """
        url = settings.SQLALCHEMY_DATABASE_URI
        engine = create_engine(url, echo=False)

        class Base(object):

            @declared_attr
            def __table__(cls):
                return Table(cls.__tablename__, MetaData(), autoload=True, autoload_with=engine)

        self._base = Base
        self.Model = self.make_declarative_base()
        self.session = sessionmaker(bind=engine)

    def make_declarative_base(self):
        base = declarative_base(cls=self._base)
        base.query = _QueryProperty(self)
        base.query_class = Query
        return base


class _QueryProperty(object):
    
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, t):
        """
        这里一定要注意，session要每次重新生成，不然session会话会自动关闭，导致下一次操作句柄为空
        :param obj:
        :param t:
        :return:
        """
        try:
            mapper = class_mapper(t)
            if mapper:
                return t.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


def gen_orm_class( db=None, table_name=None):
    """
    动态生成数据库表映射Model类
    :param db: db对象
    :param table_name: 表名称
    :return:
    """
    return type(
        table_name.title(),
        (db.Model,),
        {
            '__tablename__': table_name
        }
    )
    