"""
Financial System - Enterprise Multi-tenant Solution
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.auth.router import router as auth_router
from app.core.config.settings import get_settings
from app.core.tenant.middleware import TenantMiddleware
from app.api.v1.api import api_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Tenant Middleware
app.add_middleware(TenantMiddleware)

# Test route
@app.get("/test")
async def test():
    return {"message": "API is working!"}

# Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """
    Redirect to API documentation
    """
    return RedirectResponse(url="/docs")
