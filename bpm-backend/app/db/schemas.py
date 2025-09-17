from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date

# --------- AUTH ---------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_id: int
    #process_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleOut
    is_active: bool
    #process_id: Optional[int] = None
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    #process_id: Optional[int] = None
    is_active: Optional[bool] = None

# --------- HIERARQUIA ---------
class ProcessBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProcessCreate(ProcessBase):
    bpmn_xml_json: str

class ProcessOut(ProcessBase):
    id: int
    bpmn_xml_json: str
    class Config:
       from_attributes = True

class ProcessUpdate(ProcessBase):
    bpmn_xml_json: str
