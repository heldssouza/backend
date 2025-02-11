"""
Tenant Middleware
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import logging
from app.core.tenant.context import TenantContext

logger = logging.getLogger(__name__)

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle tenant identification and validation.
    
    This middleware:
    1. Extracts tenant information from headers
    2. Validates tenant existence and access
    3. Sets tenant context for the request
    4. Handles errors appropriately
    """

    PUBLIC_PATHS = {
        "/api/v1/health",
        "/api/v1/health/detailed",
        "/api/v1/docs",
        "/api/v1/redoc",
        "/api/v1/openapi.json"
    }

    async def dispatch(self, request: Request, call_next):
        """
        Process the request to extract and validate tenant information.
        
        Args:
            request (Request): The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response: The response from the next handler
            
        Raises:
            HTTPException: If tenant validation fails
        """
        # Skip tenant check for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        tenant_id = self._get_tenant_id(request)
        
        if not tenant_id:
            logger.warning(f"Missing tenant header for path: {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header is required"
            )

        try:
            # Set tenant context
            TenantContext.set_tenant_id(tenant_id)
            
            # Process request
            response = await call_next(request)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing request for tenant {tenant_id}: {str(e)}")
            raise
        finally:
            # Always clear tenant context
            TenantContext.clear()

    def _get_tenant_id(self, request: Request) -> Optional[str]:
        """
        Extract tenant ID from request headers.
        
        Args:
            request (Request): The incoming request
            
        Returns:
            Optional[str]: The tenant ID if found, None otherwise
        """
        return request.headers.get("X-Tenant-ID")
