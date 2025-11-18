from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
import io
import zipfile
from app.auth.auth_utils import decode_jwt
from app.utils.file_utils import validate_file

router = APIRouter(prefix="/export", tags=["export"])

class ExportRequest(BaseModel):
    markdown: str
    filename: str = "documentation.md"

async def get_current_user(authorization: str = Header(...)):
    """Extract and verify user from JWT token"""
    try:
        token = authorization.split(" ")[1]
        payload = decode_jwt(token)
        if not payload or "user_id" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

@router.post("/markdown")
async def export_markdown(
    request: ExportRequest,
    current_user = Depends(get_current_user)
):
    """Export documentation as markdown file"""
    
    return {
        "content": request.markdown,
        "filename": request.filename,
        "format": "markdown"
    }

@router.post("/zip")
async def export_zip(
    request: ExportRequest,
    current_user = Depends(get_current_user)
):
    """Export documentation and code as ZIP"""
    
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("documentation.md", request.markdown)
        
        zip_buffer.seek(0)
        
        return {
            "message": "ZIP created successfully",
            "size": len(zip_buffer.getvalue())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
