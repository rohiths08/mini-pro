from datetime import datetime
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    repo_url: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    repo_url: str
    created_at: datetime

class ProjectDB(BaseModel):
    _id: str
    user_id: str
    name: str
    repo_url: str
    created_at: datetime
