"""Health check schemas."""
from pydantic import BaseModel
from typing import Dict, Literal

ServiceStatus = Literal["ok", "error"]

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    services: Dict[str, ServiceStatus]
