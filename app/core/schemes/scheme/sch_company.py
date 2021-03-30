from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    company_code: Optional[str] = None
    company_name: Optional[str] = None
    company_full_name: Optional[str] = None

# Properties to receive via API on creation
class CompanyCreate(CompanyBase):
    uuid_code: str
    company_code: str
    company_name: str
    company_full_name: str


# Properties to receive via API on update
class CompanyUpdate(CompanyBase):
    company_code: str
    company_name: str
    company_full_name: str
    
    
class CompanyInDBBase(CompanyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class Company(CompanyInDBBase):
    pass
