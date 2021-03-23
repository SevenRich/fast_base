from datetime import datetime, timedelta
from typing import Any, Union
from hashlib import md5

from jose import jwt
from passlib.context import CryptContext
from hashids import Hashids

from ..config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    hashids = Hashids(salt=settings.OAUTH_SECRET_KEY, min_length=6)
    to_encode = {'exp': expire, 'sub': str(hashids.encode(subject))}
    encoded_jwt = jwt.encode(to_encode, settings.OAUTH_SECRET_KEY, algorithm=settings.OAUTH_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_md5_token(access_token: str) -> str:
    return md5(access_token.encode('utf8')).hexdigest()
