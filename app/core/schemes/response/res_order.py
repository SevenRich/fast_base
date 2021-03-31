from typing import Optional, List, Text

from pydantic import BaseModel


# Shared properties
class OrderBase(BaseModel):
    company_code: Optional[str] = None
    relevance_type: Optional[int] = None
    code_type: Optional[int] = None


class Code(BaseModel):
    status: Optional[int] = 1
    type: Optional[int] = 1
    code_type: Optional[int] = 1
    length: Optional[int] = 6

class CodeConfig(BaseModel):
    big_code: Code
    middle_code: Code
    small_code: Code
    security_code: Code
    verify_code: Code
    

class ExportUrl(BaseModel):
    status: Optional[int] = 1
    format: Optional[str] = '{url_prefix}/{batch_sn}-{security_code}'


class ExportQuery(BaseModel):
    status: Optional[int] = 1
    export_list: List[Optional[str]] = ['small_code', 'url', 'verify_code']

    
class ExportConfig(BaseModel):
    url_format: ExportUrl
    export_query: ExportQuery


# Properties to receive via API on creation
class OrderCreate(OrderBase):
    company_code: str
    relevance_type: int
    counts: int
    code_type: int
    url_prefix: str
    export_key: str
    code_config: CodeConfig
    export_config: ExportConfig
    

# Properties to receive via API on update
class OrderUpdate(OrderBase):
    status: Optional[int] = 3
    code_config: Optional[CodeConfig]
    export_config: Optional[ExportConfig]


class OrderInDBBase(OrderBase):
    id: Optional[int] = None
    
    status: Optional[int] = None
    code_sn: Optional[str] = None
    
    class Config:
        orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    pass


# Additional properties stored in DB
class OrderInDB(OrderInDBBase):
    pass
