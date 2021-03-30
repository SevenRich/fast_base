# _*_ coding:utf-8 _*_

from app.models import role
from datetime import timedelta
from typing import Any, List, Optional

from fastapi import (
    APIRouter, Body, Depends, HTTPException, Path, Query, Response
)
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, CompanyModel
from ...core.schemes import response
from ...core import crud
from ...config import settings
from ...core.schemes import request
from ...models.codes import get_model, create_table


router = APIRouter()


@router.get(
    '/companies', 
    summary='商户列表', 
    response_model=List[response.Company]
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    商户列表 - ID 降序
    """
    companies = db.query(CompanyModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return companies


@router.post(
    '/companies', 
    summary='创建商户', 
    response_model=response.Company
)
def store(
    form_data: dict = Depends(response.CompanyCreate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建商户
    """
    existing_info = crud.company.get_by_code(db, code=form_data.company_code)
    if existing_info is not None:
        raise HTTPException(400, 'company code is exist')
    existing_info = crud.company.get_by_uuid(db, uuid=form_data.uuid_code)
    if existing_info is not None:
        raise HTTPException(400, 'company uuid is exist')
    obj_info = crud.company.create(db, obj_in=form_data)
    # 创建码表
    create_table(form_data.uuid_code)
    
    return obj_info


@router.get(
    '/companies/{company_id}', 
    summary='商户详情', 
    response_model=response.Company
)
def show(
    company_id: int = Path(..., title="The ID of the Company to get"),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    obj_info = crud.company.get(db, id=company_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
      
    return obj_info


@router.put(
    '/companies/{company_id}', 
    summary='更新商户', 
    response_model=response.Company
)
def update(
    company_id: int,
    form_data: dict = Depends(request.CompanyUpdate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_info = crud.company.get(db, id=company_id)
    if existing_info is None:
        raise HTTPException(400, 'Not Found!')
    update_obj = crud.company.update(db, db_obj=existing_info, obj_in=form_data)
    # 检测码表是否存在
    create_table(update_obj.uuid_code)
    
    return update_obj


@router.delete(
    '/companies/{company_id}', 
    status_code=204, 
    response_class=Response,
    summary='删除商户'
)
def delete(
    company_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    删除商户 - 逻辑删除，激活状态改为 False [当前直接删除]
    """
    return
    existing_user = crud.company.get(db, id=company_id)
    if existing_user is not None:
        crud.company.remove(db, id=company_id)
