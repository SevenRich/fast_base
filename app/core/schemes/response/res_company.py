from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class CompanyBase(BaseModel):
    uuid_code: Optional[str] = None
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
    company_name: Optional[str] = None
    company_full_name: Optional[str] = None


class CompanyInDBBase(CompanyBase):
    id: Optional[int] = None
    
    class Config:
        orm_mode = True


# Additional properties to return via API
class Company(CompanyInDBBase):
    pass


# Additional properties stored in DB
class CompanyInDB(CompanyInDBBase):
    code_table_name: str
