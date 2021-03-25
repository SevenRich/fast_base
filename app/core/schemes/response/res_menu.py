from typing import List, Optional

from pydantic import BaseModel


class MenuBase(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    parent_id: Optional[int] = None
    
    
class MenuInDBBase(MenuBase):
    id: Optional[int] = None
    
    class Config:
        orm_mode = True
        
        
class Menu(MenuInDBBase):
    children: List[MenuInDBBase] = []
