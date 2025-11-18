from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import get_db
from app.core.github_handler import list_user_repos, list_repo_contents, get_file_content
from app.auth.auth_utils import decode_jwt
from fastapi import Header

router = APIRouter(prefix="/github", tags=["github"])

async def get_current_user(authorization: str = Header(...), db: AsyncIOMotorDatabase = Depends(get_db)):
    """Extract and verify user from JWT token"""
    try:
        token = authorization.split(" ")[1]
        payload = decode_jwt(token)
        if not payload or "user_id" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

@router.get("/repos")
async def get_repos(current_user = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get user's GitHub repositories"""
    from app.auth.user_model import UserModel
    user_model = UserModel(db)
    user = await user_model.find_by_id(current_user["user_id"])
    
    if not user or not user.get("github_token"):
        raise HTTPException(status_code=400, detail="GitHub not connected")
    
    result = await list_user_repos(user["github_token"])
    return result

@router.get("/contents")
async def get_contents(
    owner: str = Query(...),
    repo: str = Query(...),
    path: str = Query(default=""),
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get repository contents"""
    from app.auth.user_model import UserModel
    user_model = UserModel(db)
    user = await user_model.find_by_id(current_user["user_id"])
    
    if not user or not user.get("github_token"):
        raise HTTPException(status_code=400, detail="GitHub not connected")
    
    result = await list_repo_contents(owner, repo, path, user["github_token"])
    return result

@router.get("/file")
async def get_file(
    owner: str = Query(...),
    repo: str = Query(...),
    path: str = Query(...),
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get file content from repository"""
    from app.auth.user_model import UserModel
    user_model = UserModel(db)
    user = await user_model.find_by_id(current_user["user_id"])
    
    if not user or not user.get("github_token"):
        raise HTTPException(status_code=400, detail="GitHub not connected")
    
    result = await get_file_content(owner, repo, path, user["github_token"])
    return result
