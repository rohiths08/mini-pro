from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests: int = 100, window_seconds: int = 3600):
        self.requests = requests
        self.window_seconds = window_seconds
        self.user_requests: Dict[str, list] = {}
    
    async def check_limit(self, user_id: str) -> bool:
        """Check if user is within rate limit"""
        
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
        
        # Remove old requests outside the window
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.user_requests[user_id]) < self.requests:
            self.user_requests[user_id].append(now)
            return True
        
        return False
