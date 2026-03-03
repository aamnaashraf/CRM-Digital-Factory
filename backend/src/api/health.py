"""
Health Check Endpoints
System health and readiness checks
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.database.connection import get_db_session, get_db_manager
# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health_check():
    """
    Basic health check
    Returns 200 if service is running
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.app_env
    }


@router.get("/health/ready")
async def readiness_check(session: AsyncSession = Depends(get_db_session)):
    """
    Readiness check - verifies all dependencies
    Returns 200 if service is ready to accept traffic
    """
    checks = {
        "database": False,
        "redis": False,  # TODO: Implement Redis check
        "kafka": False,  # TODO: Implement Kafka check
    }

    # Check database
    try:
        db = get_db_manager()
        checks["database"] = await db.health_check()
    except Exception as e:
        checks["database"] = False

    # Overall status
    all_healthy = all(checks.values())
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_healthy else "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks
        }
    )


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - verifies service is alive
    Returns 200 if service should not be restarted
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
