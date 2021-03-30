from datetime import datetime, timedelta
from typing import List, Optional

import jwt

from ..config import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.OAUTH_SECRET_KEY, algorithm=settings.OAUTH_ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.OAUTH_SECRET_KEY, algorithms=[settings.OAUTH_ALGORITHM])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


async def common_parameters(page: int = 0, limit: int = 10):
    if page <= 0:
        page = 1
        skip = 0
    else:
        skip = limit * (page - 1)
    return {"skip": skip, "limit": limit}


def create_order_sn() -> Optional[str]:
    import time
    return str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
