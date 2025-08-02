from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserUpdate(UserCreate):
    password: Optional[str] = None
    
    
class UserInDBBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    
    class Config:
        from_attributes = True
        
        
class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
