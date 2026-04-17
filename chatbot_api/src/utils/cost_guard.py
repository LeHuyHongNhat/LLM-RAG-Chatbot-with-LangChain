import redis
from datetime import datetime
from fastapi import HTTPException
from src.utils.config import settings

# Initialize Redis client (same as rate_limiter)
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_budget(user_id: str):
    """
    Check if user has reached their monthly budget.
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    try:
        current_spending = float(r.get(key) or 0)
        
        if current_spending >= settings.MONTHLY_BUDGET_USD:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "Budget exceeded",
                    "monthly_limit": settings.MONTHLY_BUDGET_USD,
                    "current_spending": current_spending
                }
            )
    except redis.RedisError as e:
        print(f"Redis Error in Cost Guard (check): {e}")
        return True
    
    return True

def record_usage(user_id: str, cost: float):
    """
    Increment user spending by the cost of the current request.
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    try:
        # Increment spending and set expiration to 32 days to cover the month
        r.incrbyfloat(key, cost)
        r.expire(key, 32 * 24 * 3600)
    except redis.RedisError as e:
        print(f"Redis Error in Cost Guard (record): {e}")
