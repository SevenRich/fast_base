from typing import Optional

from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    desc: Optional[str] = None


class RoleUpdate(BaseModel):
    name: str
    desc: Optional[str] = None
