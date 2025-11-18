from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class AnalysisCreate(BaseModel):
    project_id: str
    files: List[str]
    analysis_type: str  # "documentation", "explain", "tests", "optimize", "flowchart"

class AnalysisResponse(BaseModel):
    id: str
    project_id: str
    analysis_type: str
    output: Dict[str, Any]
    created_at: datetime

class AnalysisDB(BaseModel):
    _id: str
    project_id: str
    files: List[str]
    outputs: Dict[str, Any]
    stats: Dict[str, Any]
    created_at: datetime
