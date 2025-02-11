"""Authentication router."""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db.session import get_db
from app.core.auth.jwt import create_access_token, create_refresh_token
from app.core.auth.dependencies import get_current_user, get_tenant_id
from app.core.auth.schemas import Token, RefreshToken as RefreshTokenSchema
from app.core.auth.schemas import TwoFactorSetup, TwoFactorEnable, TwoFactorVerify
from app.core.auth.totp import generate_totp_secret, get_totp_uri, verify_totp
from app.core.auth.security import verify_password
from app.core.config.settings import get_settings
from app.models.master.user import User
from app.models.master.auth import RefreshToken

router = APIRouter()
settings = get_settings()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    tenant_id: Optional[int] = Depends(get_tenant_id)
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Authenticate user
    user = db.query(User).filter(
        User.username == form_data.username,
        User.tenant_id == tenant_id
    ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )

    # Check if 2FA is enabled
    if user.two_factor_auth and user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Two-factor authentication required",
            headers={"X-2FA-Required": "true"},
        )

    # Create access token
    access_token = create_access_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "access"
        }
    )

    # Create refresh token
    refresh_token = create_refresh_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "refresh"
        }
    )

    # Store refresh token in database
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        expires_at=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(db_refresh_token)
    db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: RefreshTokenSchema,
    db: Session = Depends(get_db)
) -> Token:
    """
    Get a new access token using a refresh token.
    """
    # Verify refresh token exists and is valid
    db_refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token.refresh_token,
        RefreshToken.is_valid == True
    ).first()

    if not db_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Get user
    user = db.query(User).filter(User.id == db_refresh_token.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )

    # Create new access token
    access_token = create_access_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "access"
        }
    )

    # Create new refresh token
    new_refresh_token = create_refresh_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "refresh"
        }
    )

    # Invalidate old refresh token
    db_refresh_token.is_valid = False
    db.add(db_refresh_token)

    # Store new refresh token
    new_db_refresh_token = RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        tenant_id=user.tenant_id,
        expires_at=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_db_refresh_token)
    db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=new_refresh_token
    )


@router.post("/2fa/setup", response_model=TwoFactorSetup)
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TwoFactorSetup:
    """
    Setup two-factor authentication for the current user.
    """
    if current_user.two_factor_auth and current_user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication is already enabled"
        )

    # Generate secret
    secret = generate_totp_secret()
    
    # Store secret temporarily (it will be saved permanently when 2FA is enabled)
    current_user.two_factor_secret = secret
    db.add(current_user)
    db.commit()

    # Generate QR code
    qr_code = get_totp_uri(
        secret=secret,
        username=current_user.username,
        issuer=settings.APP_NAME
    )

    return TwoFactorSetup(secret=secret, qr_code=qr_code)


@router.post("/2fa/enable")
async def enable_2fa(
    data: TwoFactorEnable,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enable two-factor authentication for the current user.
    """
    if current_user.two_factor_auth and current_user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication is already enabled"
        )

    if not current_user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication has not been setup"
        )

    # Verify code
    if not verify_totp(current_user.two_factor_secret, data.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication code"
        )

    # Enable 2FA
    current_user.two_factor_auth.is_enabled = True
    db.add(current_user)
    db.commit()

    return {"message": "Two-factor authentication enabled successfully"}


@router.post("/2fa/verify", response_model=Token)
async def verify_2fa(
    data: TwoFactorVerify,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    tenant_id: Optional[int] = Depends(get_tenant_id)
) -> Token:
    """
    Verify two-factor authentication code and get access token.
    """
    # Authenticate user
    user = db.query(User).filter(
        User.username == form_data.username,
        User.tenant_id == tenant_id
    ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )

    if not user.two_factor_auth or not user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication is not enabled"
        )

    # Verify 2FA code
    if not verify_totp(user.two_factor_secret, data.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication code"
        )

    # Create access token
    access_token = create_access_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "access"
        }
    )

    # Create refresh token
    refresh_token = create_refresh_token(
        data={
            "sub": user.username,
            "tenant_id": user.tenant_id,
            "type": "refresh"
        }
    )

    # Store refresh token
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        tenant_id=user.tenant_id,
        expires_at=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(db_refresh_token)
    db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )
