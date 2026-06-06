import hashlib
import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

class AICache:
    """MongoDB-based cache for AI response generation to save API costs and latency"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["ai_cache"]
        
    @staticmethod
    def compute_hash(code: str, language: str, analysis_type: str) -> str:
        """Compute a unique SHA-256 hash for the code content, language, and analysis type"""
        normalized_code = code.strip()
        data = f"{normalized_code}:{language.lower()}:{analysis_type}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
        
    async def get_cached_response(self, code: str, language: str, analysis_type: str) -> dict | None:
        """Retrieve cached response if it exists"""
        try:
            code_hash = self.compute_hash(code, language, analysis_type)
            cache_entry = await self.collection.find_one({"code_hash": code_hash})
            if cache_entry:
                logger.info(f"🎯 Cache HIT for type: {analysis_type} (hash: {code_hash})")
                return cache_entry.get("response_data")
            logger.info(f"⚡ Cache MISS for type: {analysis_type} (hash: {code_hash})")
            return None
        except Exception as e:
            logger.error(f"❌ Error reading from AI Cache: {str(e)}")
            return None
            
    async def set_cached_response(self, code: str, language: str, analysis_type: str, response_data: dict):
        """Cache the AI response data"""
        try:
            code_hash = self.compute_hash(code, language, analysis_type)
            await self.collection.update_one(
                {"code_hash": code_hash},
                {
                    "$set": {
                        "code_hash": code_hash,
                        "language": language.lower(),
                        "analysis_type": analysis_type,
                        "response_data": response_data,
                        "created_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            logger.info(f"💾 Successfully cached output for type: {analysis_type} (hash: {code_hash})")
        except Exception as e:
            logger.error(f"❌ Error writing to AI Cache: {str(e)}")
