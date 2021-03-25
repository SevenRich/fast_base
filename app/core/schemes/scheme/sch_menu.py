from typing import Optional

from pydantic import BaseModel


class MenuBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
class MenuCreate(MenuBase):
    name: str
    desc: Optional[str] = None
    parent_id: Optional[str] = None


# Properties to receive via API on update
class MenuUpdate(MenuBase):
    name: str
    desc: Optional[str] = None
    
    
class MenuInDBBase(MenuBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Menu(MenuInDBBase):
    pass
