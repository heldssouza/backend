from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis import Redis
from app.core.db.session import get_db
from app.core.cache.redis import get_redis
import psutil
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
) -> Dict[str, Any]:
    """
    Comprehensive health check of the system
    """
    health_status = {
        "status": "healthy",
        "services": {}
    }

    # Check database
    try:
        db.execute("SELECT 1")
        health_status["services"]["database"] = {
            "status": "healthy"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        logger.error(f"Database health check failed: {str(e)}")

    # Check Redis
    try:
        redis.ping()
        health_status["services"]["redis"] = {
            "status": "healthy"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        logger.error(f"Redis health check failed: {str(e)}")

    # System metrics
    try:
        health_status["metrics"] = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage("/").percent
        }
    except Exception as e:
        logger.error(f"Failed to collect system metrics: {str(e)}")

    return health_status


@router.get("/health/database")
async def database_health(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Detailed database health check
    """
    try:
        # Check connection
        db.execute("SELECT 1")
        
        # Get database metrics
        metrics = db.execute("""
            SELECT 
                cntr_value
            FROM sys.dm_os_performance_counters
            WHERE counter_name IN (
                'User Connections',
                'Transactions/sec',
                'Batch Requests/sec'
            )
        """).fetchall()
        
        return {
            "status": "healthy",
            "metrics": {
                "connections": metrics[0][0] if len(metrics) > 0 else None,
                "transactions_per_second": metrics[1][0] if len(metrics) > 1 else None,
                "requests_per_second": metrics[2][0] if len(metrics) > 2 else None
            }
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/health/redis")
async def redis_health(redis: Redis = Depends(get_redis)) -> Dict[str, Any]:
    """
    Detailed Redis health check
    """
    try:
        # Check connection
        redis.ping()
        
        # Get Redis info
        info = redis.info()
        
        return {
            "status": "healthy",
            "metrics": {
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
                "total_connections_received": info.get("total_connections_received"),
                "total_commands_processed": info.get("total_commands_processed")
            }
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
