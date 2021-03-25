# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List

from fastapi import (
    APIRouter, Body, Depends, HTTPException, Response
)
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, IdentityModel
from ...core.schemes import request, response
from ...core import crud
from ...config import settings


router = APIRouter()


@router.get(
    '/identities', 
    response_model=List[response.Identity], 
    summary='权限列表'
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    权限列表 - ID 降序
    """
    identities = db.query(IdentityModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return identities


@router.post(
    '/identities', 
    summary='创建权限标识', 
    response_model=response.Identity
)
def store(
    form_data: dict = Depends(request.IdentityCreate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建权限标识
    """
    existing_name = crud.identity.get_by_name(db, name=form_data.name)
    if existing_name is not None:
        raise HTTPException(400, 'Identity name is exist')
    
    return crud.identity.create(db, obj_in=form_data)


@router.get(
    '/identities/{identity_id}', 
    summary='权限详情', 
    response_model=response.Identity
)
def show(
    identity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    obj_info = crud.identity.get(db, id=identity_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
    return obj_info


@router.put(
    '/identities/{identity_id}', 
    summary='更新权限', 
    response_model=response.Identity
)
def update(
    identity_id: int,
    form_data: dict = Depends(request.IdentityUpdate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_identity = crud.identity.get(db, id=identity_id)
    if existing_identity is None:
        raise HTTPException(400, 'Not Found!')
    
    return crud.identity.update(db, db_obj=existing_identity, obj_in=form_data)


@router.delete(
    '/identities/{identity_id}', 
    status_code=204, 
    response_class=Response,
    summary='删除权限'
)
def delete(
    identity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_user = crud.user.get(db, id=identity_id)
    if existing_user is not None:
        crud.user.remove(db, id=identity_id)
    