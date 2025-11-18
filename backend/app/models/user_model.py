from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    picture: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None

class UserDB(BaseModel):
    _id: str
    email: str
    name: str
    picture: Optional[str] = None
    google_sub: Optional[str] = None
    github_token: Optional[str] = None
    created_at: datetime
