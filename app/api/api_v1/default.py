# _*_ coding:utf-8 _*_

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Code Generation System!", "vesion": "v1.0.0", "author": "Chris Xu", "email": "SevenRich@163.com", "date": "2021-03-15"}
