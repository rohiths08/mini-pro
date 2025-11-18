from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import Optional
from bson import ObjectId

class UserModel:
    """User database operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]
    
    async def find_or_create_google_user(self, email: str, name: str, picture: str, google_sub: str):
        """Find or create user from Google OAuth"""
        user = await self.collection.find_one({"email": email})
        
        if user:
            # Update existing user
            await self.collection.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {
                        "google_sub": google_sub,
                        "picture": picture,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return user
        
        # Create new user
        new_user = {
            "email": email,
            "name": name,
            "picture": picture,
            "google_sub": google_sub,
            "github_token": None,
            "created_at": datetime.utcnow()
        }
        result = await self.collection.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return new_user
    
    async def find_or_create_github_user(self, email: str, name: str, picture: str, github_token: str):
        """Find or create user from GitHub OAuth"""
        user = await self.collection.find_one({"email": email})
        
        if user:
            await self.collection.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {
                        "github_token": github_token,
                        "picture": picture,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return user
        
        new_user = {
            "email": email,
            "name": name,
            "picture": picture,
            "github_token": github_token,
            "google_sub": None,
            "created_at": datetime.utcnow()
        }
        result = await self.collection.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return new_user
    
    async def find_by_id(self, user_id: str):
        """Find user by ID"""
        return await self.collection.find_one({"_id": ObjectId(user_id)})
    
    async def find_by_email(self, email: str):
        """Find user by email"""
        return await self.collection.find_one({"email": email})

    async def create_demo_user(self, email: str, name: str):
        """Create a simple demo user used for passwordless login"""
        now = datetime.utcnow()
        new_user = {
            "email": email,
            "name": name,
            "picture": f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}",
            "google_sub": None,
            "github_token": None,
            "created_at": now,
            "updated_at": now,
        }
        result = await self.collection.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return new_user
