import time
import redis
from fastapi import HTTPException
from src.utils.config import settings

# Shared Redis client
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

# In-memory fallback for environments without Redis (like Render Free)
_MEMORY_RATE_LIMITS = {} # dict[user_id, list_of_timestamps]

def check_rate_limit(user_id: str):
    """
    Sliding window rate limiter. Tries Redis first, falls back to Memory.
    """
    now = time.time()
    window = 60 # 1 minute
    
    try:
        # 1. Attempt Redis (Standard Production Path)
        r.ping() 
        key = f"rate_limit:{user_id}"
        r.zremrangebyscore(key, 0, now - window)
        request_count = r.zcard(key)
        
        if request_count >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded ({settings.RATE_LIMIT_PER_MINUTE} req/min). Redis enforced."
            )
        
        r.zadd(key, {str(now): now})
        r.expire(key, window)
        
    except (redis.ConnectionError, redis.TimeoutError):
        # 2. Fallback to Memory (Render Free Path)
        print(f"Warning: Redis unavailable. Falling back to Memory for rate limiting user: {user_id}")
        
        if user_id not in _MEMORY_RATE_LIMITS:
            _MEMORY_RATE_LIMITS[user_id] = []
        
        # Clean old timestamps
        _MEMORY_RATE_LIMITS[user_id] = [t for t in _MEMORY_RATE_LIMITS[user_id] if t > now - window]
        
        if len(_MEMORY_RATE_LIMITS[user_id]) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded ({settings.RATE_LIMIT_PER_MINUTE} req/min). Memory enforced."
            )
        
        _MEMORY_RATE_LIMITS[user_id].append(now)
