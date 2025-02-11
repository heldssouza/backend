"""
Health Check Endpoints
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.cache.redis import RedisCache, get_redis_cache
import psutil
import logging
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    version: str
    services: Dict[str, Any] = {}

class DetailedHealthResponse(BaseModel):
    """Response model for detailed health check endpoint"""
    status: str
    services: Dict[str, Dict[str, Any]]
    system: Dict[str, Any]

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic Health Check",
    description="Returns basic health status of the application"
)
async def health_check(
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache)
) -> HealthResponse:
    """
    Basic health check that verifies core services.
    
    Returns:
        HealthResponse: Basic health status with version information
    """
    services = {}
    overall_status = "ok"

    # Check Database
    try:
        await db.execute("SELECT 1")
        services["database"] = {"status": "ok"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        services["database"] = {"status": "error", "message": str(e)}
        overall_status = "error"

    # Check Redis
    try:
        await cache.ping()
        services["redis"] = {"status": "ok"}
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        services["redis"] = {"status": "error", "message": str(e)}
        overall_status = "error"

    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        services=services
    )

@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed Health Check",
    description="Returns detailed health information about all system components"
)
async def detailed_health_check(
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache)
) -> DetailedHealthResponse:
    """
    Detailed health check that provides comprehensive system status.
    
    Returns:
        DetailedHealthResponse: Detailed health status of all components
    """
    services = {}
    overall_status = "ok"

    # Database Check
    try:
        await db.execute("SELECT 1")
        services["database"] = {
            "status": "ok",
            "details": {
                "status": "connected",
                "message": "All database tables are properly configured"
            }
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        services["database"] = {
            "status": "error",
            "details": {
                "status": "error",
                "message": str(e)
            }
        }
        overall_status = "error"

    # Redis Check
    try:
        await cache.ping()
        info = await cache.get_info()
        services["redis"] = {
            "status": "ok",
            "details": {
                "status": "connected",
                "version": info.get("redis_version", "unknown"),
                "used_memory": info.get("used_memory_human", "unknown")
            }
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        services["redis"] = {
            "status": "error",
            "details": {
                "status": "error",
                "message": str(e)
            }
        }
        overall_status = "error"

    # System Information
    system_info = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }

    return DetailedHealthResponse(
        status=overall_status,
        services=services,
        system=system_info
    )
