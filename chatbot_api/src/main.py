import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from src.agents.hospital_rag_agent import hospital_rag_agent_executor
from src.models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput
from src.utils.async_utils import async_retry

# Security & Logic Imports
from src.utils.config import settings
from src.utils.auth import verify_api_key
from src.utils.rate_limiter import check_rate_limit, r as redis_client
from src.utils.cost_guard import check_budget, record_usage

# Structured Logging
logging.basicConfig(
    level=settings.LOG_LEVEL, 
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}'
)
logger = logging.getLogger(__name__)

# Lifecycle State
_is_ready = False
_in_flight_requests = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup/shutdown events, including Redis connectivity checks 
    and graceful shutdown waiting for in-flight requests.
    """
    global _is_ready
    logger.info("Hospital Chatbot API starting up...")
    
    # Pre-startup checks (e.g., Redis connection)
    try:
        redis_client.ping()
        _is_ready = True
        logger.info("✅ Connected to Redis successfully")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis on startup: {e}")
        logger.info("⚠️ Falling back to In-Memory security storage")
        # Set _is_ready to True anyway because we have Memory Fallback
        _is_ready = True
    
    yield
    
    # Graceful Shutdown
    _is_ready = False
    logger.info("🔄 Shutdown initiated. Waiting for active requests to drain...")
    
    # Wait for in-flight requests to finish with a 10s timeout
    timeout = 10
    start = time.time()
    while _in_flight_requests > 0 and (time.time() - start) < timeout:
        logger.info(f"Waiting for {_in_flight_requests} active requests...")
        time.sleep(0.5)
    
    logger.info("✅ Shutdown complete")

app = FastAPI(
    title="Hospital Chatbot",
    description="Hardened Pro-Agent for hospital graph RAG system",
    lifespan=lifespan
)

@app.middleware("http")
async def track_requests(request, call_next):
    """
    Middleware to track in-flight requests for graceful shutdown.
    """
    global _in_flight_requests
    _in_flight_requests += 1
    try:
        response = await call_next(request)
        return response
    finally:
        _in_flight_requests -= 1

@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """
    return await hospital_rag_agent_executor.ainvoke({"input": query})

@app.get("/")
async def get_status():
    return {
        "status": "running", 
        "environment": settings.ENVIRONMENT,
        "active_requests": _in_flight_requests
    }

@app.get("/health")
async def health_check():
    """Liveness check for Docker/Kubernetes"""
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    """Readiness check: only returns 200 if startup was successful"""
    if not _is_ready:
        raise HTTPException(status_code=503, detail="Service not ready (Redis connection issues)")
    return {"status": "ready"}

@app.post("/hospital-rag-agent")
async def ask_hospital_agent(
    query: HospitalQueryInput,
    user_id: str = Depends(verify_api_key)
) -> HospitalQueryOutput:
    """
    Main RAG Agent endpoint. Protected by:
    - API Key Auth (X-API-Key header)
    - Rate Limiting (Redis-backed)
    - Budget Guard (Redis-backed)
    """
    # Enforce security limits
    check_rate_limit(user_id)
    check_budget(user_id)
    
    # Invoke Agent
    query_response = await invoke_agent_with_retry(query.text)
    
    # Record simulated cost ($0.01 per query)
    record_usage(user_id, 0.01)
    
    # Format intermediate steps for JSON response
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
