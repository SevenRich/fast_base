from typing import Optional, List, Union, Set

from pydantic import BaseModel


class Role(BaseModel):
    id: Optional[int] = None
    

class UserUpdate(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    password: Optional[str] = None
    