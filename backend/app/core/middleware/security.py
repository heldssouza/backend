from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from app.core.security.rate_limit import RateLimiter
from app.core.security.audit import AuditTrail
from app.core.db.session import get_db
import logging

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        rate_limit_requests: int = 100,
        rate_limit_window: int = 60
    ):
        super().__init__(app)
        self.rate_limiter = RateLimiter(
            requests=rate_limit_requests,
            window=rate_limit_window
        )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else None
        
        # Check rate limit
        if not await self.rate_limiter.check_rate_limit(client_ip):
            return Response(
                content="Rate limit exceeded",
                status_code=429
            )
        
        # Security headers
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # Start timing
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        try:
            # Get current user if authenticated
            user_id = None
            if hasattr(request.state, "user"):
                user_id = request.state.user.id
            
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log successful request
            if 200 <= response.status_code < 400:
                # Get database session
                db = next(get_db())
                
                # Log audit trail
                AuditTrail.log_change(
                    session=db,
                    user_id=user_id,
                    action=f"{method} {url}",
                    table_name="http_requests",
                    record_id=str(int(time.time())),
                    new_values={
                        "method": method,
                        "url": url,
                        "status_code": response.status_code,
                        "duration": duration
                    },
                    ip_address=client_ip,
                    user_agent=user_agent
                )
                
                db.commit()
            
            return response
            
        except Exception as e:
            # Log error
            logger.error(
                f"Error processing request: {str(e)}",
                extra={
                    "method": method,
                    "url": url,
                    "client_ip": client_ip,
                    "user_agent": user_agent
                }
            )
            raise
