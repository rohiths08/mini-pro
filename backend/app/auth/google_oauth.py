import httpx
from typing import Optional
from app.config import settings
from app.auth.user_model import UserModel
from app.auth.auth_utils import generate_jwt

async def get_google_oauth_url() -> str:
    """Generate Google OAuth URL"""
    redirect_uri = f"{settings.BACKEND_URL}/auth/google/callback"
    scopes = "openid profile email"
    
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scopes}"
    )
    return url

async def exchange_google_code(code: str, db) -> Optional[dict]:
    """Exchange Google authorization code for token"""
    redirect_uri = f"{settings.BACKEND_URL}/auth/google/callback"
    
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, json=payload)
        if response.status_code != 200:
            return None
        
        data = response.json()
        id_token = data.get("id_token")
        
        # Verify ID token (simplified - in production use proper verification)
        # For now, we'll decode it assuming it's valid
        # In production, use google-auth library for proper verification
        
        # Fetch user info from Google
        info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {data.get('access_token')}"}
        )
        
        if info_response.status_code != 200:
            return None
        
        user_info = info_response.json()
        
        # Upsert user in MongoDB
        user_model = UserModel(db)
        user = await user_model.find_or_create_google_user(
            email=user_info.get("email"),
            name=user_info.get("name"),
            picture=user_info.get("picture"),
            google_sub=user_info.get("id")
        )
        
        # Generate JWT
        jwt_token = generate_jwt({"user_id": str(user["_id"]), "email": user["email"]})
        
        return {
            "token": jwt_token,
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "name": user["name"],
                "picture": user["picture"]
            }
        }
