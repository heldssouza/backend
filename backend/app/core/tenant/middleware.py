"""
Tenant Middleware
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.tenant.context import TenantContext
from app.core.config.settings import Settings, get_settings
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

TEST_TENANT_ID = UUID("00000000-0000-0000-0000-000000000001")

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle tenant context in requests.
    """
    def __init__(self, app, settings: Settings = None):
        super().__init__(app)
        self.settings = settings or get_settings()
        self.public_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/test",
            "/",
            "/api/v1/docs",
            "/api/v1/openapi.json",
            "/api/v1/health/"
        }

    async def dispatch(self, request: Request, call_next):
        """
        Process the request, setting the tenant context.
        """
        path = request.url.path

        # Skip tenant check for public paths
        if path in self.public_paths:
            try:
                response = await call_next(request)
                return response
            finally:
                TenantContext.clear()

        # Get tenant from header
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            raise HTTPException(
                status_code=400,
                detail="X-Tenant-ID header is required"
            )

        try:
            # Handle test tenant
            if tenant_id == "test_tenant":
                tenant_uuid = TEST_TENANT_ID
            else:
                tenant_uuid = UUID(tenant_id)

            TenantContext.set_tenant_id(tenant_uuid)
            response = await call_next(request)
            return response
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid tenant ID format. Must be a valid UUID."
            )
        finally:
            TenantContext.clear()
