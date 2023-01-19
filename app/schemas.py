from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str
    
class ResetPassword(BaseModel):
    access_token: str
    password: str
    
class ForgotPassword(BaseModel):
    email: EmailStr
    
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    created_at: datetime
    rating: Optional[str] = None
    owner_id: int
    owner: User
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
        
class TokenData(BaseModel):
    id: Optional[int] = None
    
class PostVote(BaseModel):
    post_id: int
    dir: conint(le=1)