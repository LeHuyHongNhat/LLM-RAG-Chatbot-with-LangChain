import redis
from datetime import datetime
from fastapi import HTTPException
from src.utils.config import settings

# Shared Redis client
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

# In-memory fallback
_MEMORY_BUDGETS = {} # dict[str, float] where key is user:YYYY-MM

def _get_budget_key(user_id: str):
    month_key = datetime.now().strftime("%Y-%m")
    return f"{user_id}:{month_key}"

def check_budget(user_id: str):
    """
    Ensures the user hasn't exceeded their monthly budget. Falls back to Memory if Redis is down.
    """
    key = f"budget:{_get_budget_key(user_id)}"
    
    try:
        r.ping()
        current_spending = float(r.get(key) or 0)
    except (redis.ConnectionError, redis.TimeoutError):
        # Fallback to Memory
        mem_key = _get_budget_key(user_id)
        current_spending = _MEMORY_BUDGETS.get(mem_key, 0.0)
        
    if current_spending >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=402, 
            detail=f"Monthly budget of ${settings.MONTHLY_BUDGET_USD} exceeded."
        )

def record_usage(user_id: str, cost: float):
    """
    Updates the user's monthly spending. Falls back to Memory if Redis is down.
    """
    key = f"budget:{_get_budget_key(user_id)}"
    try:
        r.ping()
        r.incrbyfloat(key, cost)
        r.expire(key, 32 * 24 * 3600)
    except (redis.ConnectionError, redis.TimeoutError):
        # Fallback to Memory
        mem_key = _get_budget_key(user_id)
        _MEMORY_BUDGETS[mem_key] = _MEMORY_BUDGETS.get(mem_key, 0.0) + cost
