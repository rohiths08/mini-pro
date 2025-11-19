from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, EmailStr
from app.config import get_db, settings
from app.auth.google_oauth import get_google_oauth_url, exchange_google_code
from app.auth.github_oauth import get_github_oauth_url, exchange_github_code
from app.auth.auth_utils import generate_jwt, decode_jwt
from app.auth.user_model import UserModel
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])


class DemoLoginRequest(BaseModel):
    email: EmailStr
    name: str | None = None

@router.get("/google/url")
async def google_login_url():
    """Get Google OAuth login URL"""
    url = await get_google_oauth_url()
    return {"url": url}

@router.get("/google/callback")
async def google_callback(code: str = Query(...), db: AsyncIOMotorDatabase = Depends(get_db)):
    """Handle Google OAuth callback"""
    result = await exchange_google_code(code, db)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Google")
    
    # Redirect to frontend with token
    token = result["token"]
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/login/success?token={token}",
        status_code=302
    )

@router.get("/github/url")
async def github_login_url():
    """Get GitHub OAuth login URL"""
    url = await get_github_oauth_url()
    return {"url": url}

@router.get("/github/callback")
async def github_callback(code: str = Query(...), db: AsyncIOMotorDatabase = Depends(get_db)):
    """Handle GitHub OAuth callback"""
    result = await exchange_github_code(code, db)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to authenticate with GitHub")
    
    token = result["token"]
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/login/success?token={token}",
        status_code=302
    )

@router.post("/logout")
async def logout():
    """Logout endpoint"""
    return {"message": "Logged out successfully"}


@router.post("/demo-login")
async def demo_login(
    payload: DemoLoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Developer-friendly login flow that provisions a demo user and issues a JWT."""
    user_model = UserModel(db)
    user = await user_model.find_by_email(payload.email)
    
    if not user:
        user = await user_model.create_demo_user(
            email=payload.email,
            name=payload.name or "CodeDoc User"
        )
    
    token = generate_jwt({"user_id": str(user["_id"]), "email": user["email"]})
    
    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name"),
            "picture": user.get("picture")
        }
    }


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


@router.get("/profile")
async def get_profile(
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get current user profile information"""
    user_model = UserModel(db)
    user = await user_model.find_by_id(current_user["user_id"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name"),
        "picture": user.get("picture"),
        "created_at": user.get("created_at")
    }
