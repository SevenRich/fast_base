# _*_ coding:utf-8 _*_

from app.models import role
from datetime import timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, RoleModel
from ...core.schemes import response
from ...core import crud
from ...config import settings
from ...core.schemes import request


router = APIRouter()


@router.get(
    '/users', 
    summary='用户列表', 
    response_model=List[response.User]
)
def index_users(
    # keyword: Optional[str] = None,
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
    user_info = crud.user.create(db, obj_in=form_data)
    # 分配角色
    user_info.roles.append(crud.role.get(db, id=form_data.role_id))
    db.commit()
    return user_info


@router.get(
    '/users/{user_id}', 
    summary='用户详情', 
    response_model=response.User
)
def show_users(
    user_id: int = Path(..., title="The ID of the User to get"),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    user_info = crud.user.get(db, id=user_id)
    if user_info is None:
        raise HTTPException(400, 'Not Found!')
    return user_info


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
    update_user = crud.user.update(db, db_obj=existing_user, obj_in=form_data)
    # 清空旧角色
    for user_role in update_user.roles:
        update_user.roles.remove(user_role)
    # 追加新角色
    update_user.roles.append(crud.role.get(db, id=role_id))
    db.commit()
    return update_user


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
    """
    删除用户 - 逻辑删除，激活状态改为 False [当前直接删除]
    """
    existing_user = crud.user.get(db, id=user_id)
    if existing_user is not None:
        crud.user.remove(db, id=user_id)
