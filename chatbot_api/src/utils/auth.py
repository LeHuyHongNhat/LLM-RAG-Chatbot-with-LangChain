from typing import Optional
from fastapi import Header, HTTPException
from src.utils.config import settings

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Dependency to verify API Key.
    Expects X-API-Key header.
    Returns 401 instead of FastAPI's default 422 for missing headers.
    """
    if not x_api_key or x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return "user_hospital_admin"
