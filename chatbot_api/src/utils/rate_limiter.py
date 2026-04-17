import time
import redis
from fastapi import HTTPException
from src.utils.config import settings

# Initialize Redis client
# Note: Host 'redis' matches the service name in docker-compose
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str):
    """
    Sliding window rate limiter using Redis Sorted Set.
    """
    now = time.time()
    key = f"rate_limit:{user_id}"
    window = 60 # 1 minute
    
    try:
        # 1. Remove timestamps older than the window
        r.zremrangebyscore(key, 0, now - window)
        
        # 2. Count requests in the current window
        request_count = r.zcard(key)
        
        if request_count >= settings.RATE_LIMIT_PER_MINUTE:
            # Calculate retry-after time
            oldest_timestamp = r.zrange(key, 0, 0, withscores=True)
            retry_after = 0
            if oldest_timestamp:
                retry_after = int(window - (now - oldest_timestamp[0][1]))
            
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": settings.RATE_LIMIT_PER_MINUTE,
                    "window_seconds": window,
                    "retry_after_seconds": max(1, retry_after)
                }
            )
        
        # 3. Add current request timestamp
        r.zadd(key, {str(now): now})
        r.expire(key, window + 10) # Auto-cleanup
        
    except redis.RedisError as e:
        # Fail open or fail closed? Here we log and continue to avoid blocking users
        print(f"Redis Error in Rate Limiter: {e}")
        return True
    
    return True
