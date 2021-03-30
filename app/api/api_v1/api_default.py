# _*_ coding:utf-8 _*_

from fastapi import APIRouter
from pydantic.types import Json


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Code Generation System!", "vesion": "v1.0.0", "author": "Chris Xu", "email": "SevenRich@163.com", "date": "2021-03-15"}


@router.get(
    '/tables', 
    summary='tables'
)
def delete_users():
    # from ...utils.code_table import get_model, create_table
    # from ...models.db import Base, engine
    # from ...config import settings
    
    # suffix = '3333'
    # if create_table(suffix=suffix):
    #     print('create table success')
    
    # print('success')
    
    from ...models.codes import get_model, create_table
    
    t1 = get_model('t1')
    if create_table(suffix='t1'):
        print('create table t1 success')
    print(t1)
    print(t1.__tablename__)
    