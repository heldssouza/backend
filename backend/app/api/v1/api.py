"""
API Router Configuration
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, tenants, roles, health

api_router = APIRouter()

# Health Check
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

# Authentication
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# Users
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# Tenants
api_router.include_router(
    tenants.router,
    prefix="/tenants",
    tags=["tenants"]
)

# Roles
api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["roles"]
)
