# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, RoleModel
from ...core.schemes import request, response
from ...core import crud
from ...config import settings


router = APIRouter()


@router.get(
    '/roles', 
    response_model=List[response.Role], 
    summary='角色列表'
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    角色列表 - ID 降序
    """
    roles = db.query(RoleModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return roles


@router.post(
    '/roles', 
    summary='创建角色标识', 
    response_model=response.Role
)
def store(
    form_data: dict = Depends(request.RoleCreate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建角色标识
    """
    existing_name = crud.role.get_by_name(db, name=form_data.name)
    if existing_name is not None:
        raise HTTPException(400, 'Role name is exist')
    
    # TODO: 分配权限
    return crud.role.create(db, obj_in=form_data)


@router.get(
    '/roles/{role_id}', 
    summary='角色详情', 
    response_model=response.Role
)
def show(
    role_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    return crud.role.get(db, id=role_id)


@router.put(
    '/roles/{role_id}', 
    summary='更新角色', 
    response_model=response.Role
)
def update(
    role_id: int,
    form_data: dict = Depends(request.RoleUpdate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_role = crud.role.get(db, id=role_id)
    if existing_role is None:
        raise HTTPException(400, 'Role Not Found!')
    
    # TODO: 分配权限
    return crud.role.update(db, db_obj=existing_role, obj_in=form_data)


@router.delete(
    '/roles/{role_id}', 
    status_code=204, 
    summary='删除角色'
)
def delete(
    role_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_user = crud.role.get(db, id=role_id)
    if existing_user is not None:
        crud.role.remove(db, id=role_id)
    