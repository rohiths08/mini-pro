import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

load_dotenv()

class Settings:
    """Application configuration"""
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")
    
    # Database
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    
    # URLs
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "3600"))

settings = Settings()

# Global MongoDB client
mongo_client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_to_mongo():
    """Initialize MongoDB connection"""
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    db = mongo_client["ai_codedoc_studio"]
    # Test connection
    await db.command("ping")
    print("Connected to MongoDB")

async def close_mongo():
    """Close MongoDB connection"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("Disconnected from MongoDB")

def get_db() -> AsyncIOMotorDatabase:
    """Dependency for getting database instance"""
    return db
