from typing import Optional

from pydantic import BaseModel


class IdentityCreate(BaseModel):
    name: str
    desc: Optional[str] = None


class IdentityUpdate(BaseModel):
    name: str
    desc: Optional[str] = None
