from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request
from redis.asyncio import Redis
import json
import uuid
from app.core.config.settings import get_settings

settings = get_settings()

class SessionManager:
    def __init__(self):
        self.redis: Redis = Redis.from_url(settings.REDIS_URL)
        self.session_timeout = settings.SESSION_TIMEOUT_MINUTES * 60  # Convert to seconds

    async def create_session(self, user_id: int, tenant_id: str) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
        
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session_data)
        )
        
        return session_id

    async def validate_session(self, session_id: str) -> dict:
        session_data = await self.redis.get(f"session:{session_id}")
        if not session_data:
            raise HTTPException(status_code=401, detail="Session expired")
        
        session = json.loads(session_data)
        
        # Update last activity
        session["last_activity"] = datetime.utcnow().isoformat()
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session)
        )
        
        return session

    async def end_session(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")

    async def get_active_sessions(self, user_id: int) -> list:
        pattern = "session:*"
        sessions = []
        
        async for key in self.redis.scan_iter(match=pattern):
            session_data = await self.redis.get(key)
            if session_data:
                session = json.loads(session_data)
                if session.get("user_id") == user_id:
                    sessions.append({
                        "session_id": key.decode().split(":")[1],
                        **session
                    })
        
        return sessions

class SessionMiddleware:
    def __init__(self):
        self.session_manager = SessionManager()

    async def __call__(self, request: Request, call_next):
        # Skip session validation for certain paths
        if request.url.path in settings.SESSION_EXCLUDE_PATHS:
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=401, detail="No session found")

        # Validate and update session
        session = await self.session_manager.validate_session(session_id)
        
        # Add session info to request state
        request.state.session = session
        
        response = await call_next(request)
        return response
