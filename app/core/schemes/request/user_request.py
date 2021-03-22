from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    password: str
