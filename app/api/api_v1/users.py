# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel
from ...core.schemes import response
from ...core import crud
from ...config import settings
from ...core.schemes import request



router = APIRouter()


@router.get(
    '/users', 
    response_model=List[response.User], 
    summary='用户列表'
)
def index_users(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    用户列表 - ID 降序
    """
    users = db.query(UserModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return users


@router.post(
    '/users', 
    summary='创建用户', 
    response_model=response.User
)
def store_users(
    form_data: dict = Depends(response.UserCreate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建用户
    """
    existing_username = crud.user.get_by_username(db, username=form_data.username)
    if existing_username is not None:
        raise HTTPException(400, 'username is exist')
    
    existing_user = crud.user.get_by_email(db, email=form_data.email)
    if existing_user is not None:
        raise HTTPException(400, 'user is exist')
    
    # TODO: 分配角色
    return crud.user.create(db, obj_in=form_data)


@router.get(
    '/users/{user_id}', 
    summary='用户详情', 
    response_model=response.User
)
def show_users(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    return crud.user.get(db, id=user_id)


@router.put(
    '/users/{user_id}', 
    summary='更新用户', 
    response_model=response.User
)
def update_users(
    user_id: int,
    form_data: dict = Depends(request.UserUpdate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_user = crud.user.get(db, id=user_id)
    if existing_user is None:
        raise HTTPException(400, 'Not Found!')
    
    # TODO: 分配角色
    return crud.user.update(db, db_obj=existing_user, obj_in=form_data)


@router.delete(
    '/users/{user_id}', 
    status_code=204, 
    summary='删除用户'
)
def delete_users(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_user = crud.user.get(db, id=user_id)
    if existing_user is not None:
        crud.user.remove(db, id=user_id)
    