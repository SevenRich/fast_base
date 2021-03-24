from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: Optional(int) = 200
    message: Optional(str) = 'Success'
    data: Optional(List[Any]) = []
