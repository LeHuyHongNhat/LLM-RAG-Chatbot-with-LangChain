from fastapi import Header, HTTPException
from src.utils.config import settings

def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency to verify API Key.
    Expects X-API-Key header.
    """
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return "user_hospital_admin" # Mock user ID for this project
