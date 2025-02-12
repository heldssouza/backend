"""
Health Check Endpoints
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.core.db.session import get_db
from app.core.cache.redis import RedisCache, get_redis_client
from app.core.security.dependencies import rate_limit
import psutil
import logging
from pydantic import BaseModel
from app.schemas.master.health import HealthResponse
from app.core.config import Settings, get_settings

router = APIRouter()
logger = logging.getLogger(__name__)

class DetailedHealthResponse(BaseModel):
    """Response model for detailed health check endpoint"""
    status: str
    services: Dict[str, Dict[str, Any]]
    system: Dict[str, Any]

@router.get(
    "/",
    response_model=HealthResponse
)
async def health_check(
    request: Request,
    db: Session = Depends(get_db),
    redis: RedisCache = Depends(get_redis_client),
    settings: Settings = Depends(get_settings)
) -> HealthResponse:
    """
    Check the health of all services the application depends on.
    """
    services = {
        "database": "error",
        "redis": "error"
    }

    try:
        # Check database connection
        query = text("SELECT 1")
        result = db.execute(query)
        if result:
            services["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")

    try:
        # Check Redis connection
        if await redis.ping():
            services["redis"] = "ok"
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")

    # If any check fails, return 503
    if not all(s == "ok" for s in services.values()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

    return HealthResponse(services=services)


@router.get(
    "/detailed",
    response_model=DetailedHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed Health Check",
    description="Returns detailed health status of all system components"
)
async def detailed_health_check(
    db: Session = Depends(get_db),
    cache: RedisCache = Depends(get_redis_client)
) -> DetailedHealthResponse:
    """
    Detailed health check that provides comprehensive system status.

    Returns:
        DetailedHealthResponse: Detailed health status of all components
    """
    services = {
        "database": {
            "status": "error",
            "details": {}
        },
        "redis": {
            "status": "error",
            "details": {}
        }
    }

    system = {
        "cpu": {
            "percent": psutil.cpu_percent(),
            "count": psutil.cpu_count()
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        }
    }

    try:
        # Detailed database check
        query = text("SELECT version()")
        result = db.execute(query)
        version = result.scalar()
        
        services["database"] = {
            "status": "ok",
            "details": {
                "version": version,
                "connection": "active"
            }
        }
    except Exception as e:
        services["database"]["details"]["error"] = str(e)
        logger.error(f"Detailed database health check failed: {str(e)}")

    try:
        # Detailed Redis check
        info = await cache.info()
        services["redis"] = {
            "status": "ok",
            "details": {
                "version": info.get("redis_version", "unknown"),
                "used_memory": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", "unknown"),
                "uptime_days": info.get("uptime_in_days", "unknown")
            }
        }
    except Exception as e:
        services["redis"]["details"]["error"] = str(e)
        logger.error(f"Detailed Redis health check failed: {str(e)}")

    return DetailedHealthResponse(
        status="ok" if all(s["status"] == "ok" for s in services.values()) else "error",
        services=services,
        system=system
    )
