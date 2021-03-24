from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel


class IdentityRequest(BaseModel):
    identity_id: Optional[int] = None

class MenuRequest(BaseModel):
    id: int 
    name: str 
