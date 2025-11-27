from pydantic import BaseModel 
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime 

    class Config:
        # orm_mode est déprécié, on utilise from_attributes
        from_attributes = True 
        
class Token(BaseModel):
    access_token: str
    token_type: str 
    
class TokenData(BaseModel):
    username: Optional[str] = None

class TranslateRequest(BaseModel):
    text: str
    source_language: str 
    target_language: str 
class TranslateResponse(BaseModel):
    translated_text: str