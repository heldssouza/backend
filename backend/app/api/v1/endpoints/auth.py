from datetime import timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.auth import SecurityService
from app.core.security.dependencies import get_current_user
from app.services.master.user import UserService
from app.services.master.audit import AuditService
from app.schemas.master.token import Token, RefreshToken
from app.schemas.master.user import UserCreate, UserInDB
from app.core.security.two_factor import two_factor_auth
from app.models.master.user import User

router = APIRouter()


@router.post("/register", response_model=UserInDB)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Check if email exists
    if user_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = user_service.create_user(user_data)
    
    # Log audit
    await audit_service.log_action(
        action="REGISTER_USER",
        entity_type="USER",
        entity_id=user.UserID,
        user_id=user.UserID,
        tenant_id=user.TenantID
    )
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user_service = UserService(db)
    audit_service = AuditService(db)
    security_service = SecurityService(db)
    
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Check if 2FA is enabled
    requires_2fa = two_factor_auth.is_2fa_enabled(user)
    if requires_2fa:
        return Token(
            access_token="",
            token_type="bearer",
            requires_2fa=True
        )
    
    # Generate tokens
    access_token = security_service.create_access_token(
        data={"sub": user.Email, "tenant_id": str(user.TenantID)}
    )
    refresh_token = security_service.create_refresh_token(user_id=user.UserID)
    
    # Log audit
    await audit_service.log_action(
        action="LOGIN",
        entity_type="USER",
        entity_id=user.UserID,
        user_id=user.UserID,
        tenant_id=user.TenantID
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        requires_2fa=False
    )


@router.post("/verify-2fa", response_model=Token)
async def verify_2fa(
    code: str,
    email: str,
    db: Session = Depends(get_db)
):
    """
    Verify 2FA code and get access token.
    """
    user_service = UserService(db)
    audit_service = AuditService(db)
    security_service = SecurityService(db)
    
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Verify 2FA code
    if not two_factor_auth.verify_2fa_code(user, code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 2FA code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate tokens
    access_token = security_service.create_access_token(
        data={"sub": user.Email, "tenant_id": str(user.TenantID)}
    )
    refresh_token = security_service.create_refresh_token(user_id=user.UserID)
    
    # Log audit
    await audit_service.log_action(
        action="2FA_VERIFY",
        entity_type="USER",
        entity_id=user.UserID,
        user_id=user.UserID,
        tenant_id=user.TenantID
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        requires_2fa=False
    )


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_token_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Get a new access token using refresh token.
    """
    user_service = UserService(db)
    audit_service = AuditService(db)
    security_service = SecurityService(db)
    
    # Validate refresh token
    user_id = security_service.validate_refresh_token(refresh_token_data.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Generate new access token
    access_token = security_service.create_access_token(
        data={"sub": user.Email, "tenant_id": str(user.TenantID)}
    )
    
    # Log audit
    await audit_service.log_action(
        action="REFRESH_TOKEN",
        entity_type="USER",
        entity_id=user.UserID,
        user_id=user.UserID,
        tenant_id=user.TenantID
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        requires_2fa=False
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout current user.
    """
    audit_service = AuditService(db)
    security_service = SecurityService(db)
    
    # Invalidate refresh token
    security_service.invalidate_refresh_token(current_user.UserID)
    
    # Log audit
    await audit_service.log_action(
        action="LOGOUT",
        entity_type="USER",
        entity_id=current_user.UserID,
        user_id=current_user.UserID,
        tenant_id=current_user.TenantID
    )
    
    return {"message": "Successfully logged out"}
