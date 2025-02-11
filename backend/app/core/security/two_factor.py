import pyotp
import qrcode
import base64
from io import BytesIO
from typing import Tuple
from datetime import datetime, timedelta
from fastapi import HTTPException
from redis.asyncio import Redis
from app.core.config.settings import get_settings

settings = get_settings()

class TwoFactorAuth:
    def __init__(self):
        self.redis: Redis = Redis.from_url(settings.REDIS_URL)
        self.backup_codes_count = 10
        self.backup_code_length = 10
        self.totp_issuer = settings.PROJECT_NAME
    
    def generate_secret(self) -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    def get_totp(self, secret: str) -> pyotp.TOTP:
        """Get TOTP object for the secret"""
        return pyotp.TOTP(secret)
    
    def generate_qr_code(self, email: str, secret: str) -> str:
        """Generate QR code for TOTP setup"""
        totp = self.get_totp(secret)
        provisioning_uri = totp.provisioning_uri(
            email,
            issuer_name=self.totp_issuer
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Create image and convert to base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def generate_backup_codes(self) -> list[str]:
        """Generate backup codes"""
        return [
            pyotp.random_base32()[:self.backup_code_length]
            for _ in range(self.backup_codes_count)
        ]
    
    def verify_totp(self, secret: str, code: str) -> bool:
        """Verify TOTP code"""
        totp = self.get_totp(secret)
        return totp.verify(code)
    
    async def store_temp_secret(self, user_id: int, secret: str):
        """Store temporary secret during 2FA setup"""
        key = f"2fa_setup:{user_id}"
        await self.redis.setex(key, 300, secret)  # Expires in 5 minutes
    
    async def get_temp_secret(self, user_id: int) -> str:
        """Get temporary secret during 2FA setup"""
        key = f"2fa_setup:{user_id}"
        secret = await self.redis.get(key)
        if not secret:
            raise HTTPException(status_code=400, detail="2FA setup expired")
        return secret.decode()
    
    async def clear_temp_secret(self, user_id: int):
        """Clear temporary secret after 2FA setup"""
        key = f"2fa_setup:{user_id}"
        await self.redis.delete(key)
    
    async def rate_limit_code_verification(self, user_id: int) -> bool:
        """Rate limit code verification attempts"""
        key = f"2fa_attempts:{user_id}"
        attempts = await self.redis.incr(key)
        
        if attempts == 1:
            await self.redis.expire(key, 300)  # 5 minutes window
        
        return attempts > 5  # Max 5 attempts per 5 minutes
    
    async def clear_verification_attempts(self, user_id: int):
        """Clear verification attempts after successful login"""
        key = f"2fa_attempts:{user_id}"
        await self.redis.delete(key)

class TwoFactorMiddleware:
    def __init__(self):
        self.two_factor = TwoFactorAuth()
        self.redis: Redis = Redis.from_url(settings.REDIS_URL)
    
    async def __call__(self, request, call_next):
        # Skip 2FA check for excluded paths
        if request.url.path in settings.TWO_FACTOR_EXCLUDE_PATHS:
            return await call_next(request)
        
        # Get user from request state (set by auth middleware)
        user = getattr(request.state, "user", None)
        if not user:
            return await call_next(request)
        
        # Check if user has 2FA enabled and verified
        if user.get("two_factor_enabled"):
            two_factor_verified = await self.redis.get(
                f"2fa_verified:{user['id']}"
            )
            if not two_factor_verified:
                raise HTTPException(
                    status_code=403,
                    detail="Two-factor authentication required"
                )
        
        return await call_next(request)

two_factor_auth = TwoFactorAuth()
