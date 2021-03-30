from typing import Optional

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    uuid_code: str
    company_code: str
    company_name: str
    company_full_name: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    company_full_name: Optional[str] = None
