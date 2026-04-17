import os

class Settings:
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "secret-key-123")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    MONTHLY_BUDGET_USD: float = float(os.getenv("MONTHLY_BUDGET_USD", "10.0"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

settings = Settings()
