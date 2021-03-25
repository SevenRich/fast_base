# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List, Optional

from fastapi import (
    APIRouter, Body, Depends, HTTPException, Query, Response
)
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
    summary='角色列表', 
    response_model=List[response.Role]
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
    identity_ids: Optional[List[int]] = Query(..., ge=1),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建角色标识 - 并把权限标识写入关联表
    """
    existing_name = crud.role.get_by_name(db, name=form_data.name)
    if existing_name is not None:
        raise HTTPException(400, 'Role name is exist')
    role_info = crud.role.create(db, obj_in=form_data)
    # 分配权限
    [role_info.identity.append(crud.identity.get(db, id=identity_id)) for identity_id in identity_ids]
    db.commit()
    return crud.role.get_by_name(db, name=form_data.name)


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
    obj_info = crud.role.get(db, id=role_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
    return obj_info


@router.put(
    '/roles/{role_id}', 
    summary='更新角色', 
    response_model=response.Role
)
def update(
    role_id: int,
    form_data: dict = Depends(request.RoleUpdate),
    identity_ids: Optional[List[int]] = Query(..., ge=1),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    更新角色信息，并删除旧权限，重新分配新权限
    """
    existing_role = crud.role.get(db, id=role_id)
    if existing_role is None:
        raise HTTPException(400, 'Role Not Found!')
    role_info = crud.role.update(db, db_obj=existing_role, obj_in=form_data)
    # 清空旧权限
    [role_info.identity.remove(role_identity) for role_identity in role_info.identity]
    # 分配权限
    [role_info.identity.append(crud.identity.get(db, id=identity_id)) for identity_id in identity_ids]
    db.commit()
    return crud.role.get(db, id=role_id)


@router.delete(
    '/roles/{role_id}', 
    status_code=204, 
    response_class=Response,
    summary='删除角色'
)
def delete(
    role_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    删除角色
    """
    existing_user = crud.role.get(db, id=role_id)
    if existing_user is not None:
        crud.role.remove(db, id=role_id)
    