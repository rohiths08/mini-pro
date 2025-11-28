import httpx
from typing import Optional
from app.config import settings
from app.auth.user_model import UserModel
from app.auth.auth_utils import generate_jwt

async def get_github_oauth_url() -> str:
    """Generate GitHub OAuth URL"""
    redirect_uri = f"{settings.BACKEND_URL}/auth/github/callback"
    
    url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={settings.GITHUB_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"scope=repo%20user"
    )
    return url

async def exchange_github_code(code: str, db) -> Optional[dict]:
    """Exchange GitHub authorization code for token"""
    redirect_uri = f"{settings.BACKEND_URL}/auth/github/callback"
    
    token_url = "https://github.com/login/oauth/access_token"
    
    async with httpx.AsyncClient() as client:
        # Get access token
        response = await client.post(
            token_url,
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": redirect_uri
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code != 200:
            error_detail = response.text
            print(f"❌ GitHub token exchange failed: {response.status_code}")
            print(f"Error details: {error_detail}")
            return None
        
        print("✅ GitHub token exchange successful")
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        # Fetch user profile
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if user_response.status_code != 200:
            error_detail = user_response.text
            print(f"❌ GitHub user info fetch failed: {user_response.status_code}")
            print(f"Error details: {error_detail}")
            return None
        
        print("✅ GitHub user info fetched successfully")
        user_info = user_response.json()
        print(f"📧 User: {user_info.get('login')}")
        
        # Get user email if not public
        email = user_info.get("email")
        if not email:
            emails_response = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if emails_response.status_code == 200:
                emails = emails_response.json()
                email = next((e["email"] for e in emails if e["primary"]), user_info.get("login"))
        
        # Upsert user in MongoDB
        user_model = UserModel(db)
        user = await user_model.find_or_create_github_user(
            email=email or user_info.get("login"),
            name=user_info.get("name") or user_info.get("login"),
            picture=user_info.get("avatar_url"),
            github_token=access_token
        )
        print(f"✅ User authenticated: {user.get('email')}")
        
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
