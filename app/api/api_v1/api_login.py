# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any

from fastapi import (
    APIRouter, Body, Depends, HTTPException
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...utils import deps, security
from ...models import UserModel
from ...core.schemes import response
from ...core import crud
from ...config import settings
from ...utils.common import (
    generate_password_reset_token,
    verify_password_reset_token,
)


router = APIRouter()


@router.post("/access-token", response_model=response.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    response_data = {
        'access_token': security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        'token_type': 'bearer',
    }
    # 更新用户表中的 access_token
    token_form = {
        'access_token': security.create_md5_token(response_data['access_token'])
    }
    crud.user.update_access_token(db, db_obj=user, obj_in=token_form)
    
    return response_data
    

@router.post("/test-token", response_model=response.User)
def test_token(current_user: UserModel = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.get(
    '/logout'
)
def logout(
    db: Session = Depends(deps.get_db), 
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    注销用户
    """
    crud.user.update_access_token(db, db_obj=current_user, obj_in={
        'access_token': None
    })
    return {'message': 'logout success'}