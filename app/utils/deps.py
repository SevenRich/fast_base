from typing import Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from hashids import Hashids

from ..models import UserModel
from ..utils import security
from ..config import settings
from ..models.db import SessionLocal
from ..core import schemes, crud
from ..core.schemes import scheme

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/{settings.OAUTH_TOKEN_URL}"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.OAUTH_SECRET_KEY, algorithms=[settings.OAUTH_ALGORITHM]
        )
        token_data = scheme.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    hashids = Hashids(salt=settings.OAUTH_SECRET_KEY, min_length=6)
    user = crud.user.get(db, id=hashids.decode(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # access_token 与数据库保存的不一样
    if user.access_token != security.create_md5_token(token):
        raise HTTPException(status_code=401, detail="Access Token have expired")
    return user


def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_identity_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    pass