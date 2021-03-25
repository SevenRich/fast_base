from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel


class MenuRequest(BaseModel):
    name: str 
    desc: str 
    parent_id: Optional[int] = None 
