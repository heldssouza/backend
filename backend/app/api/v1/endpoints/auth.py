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
    
    # Check if username exists
    if user_service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
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
        entity_id=user.id,
        user_id=user.id,
        tenant_id=None,
        changes=user_data.model_dump(exclude={"password"})
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
    security_service = SecurityService()
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Authenticate user
    user = user_service.get_user_by_username(form_data.username)
    if not user or not security_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate 2FA code if enabled
    if user.two_factor_enabled:
        two_factor_auth.generate_code(user.id)
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="2FA code required",
            headers={"X-2FA-Required": "true"},
        )
    
    # Create access token
    access_token = security_service.create_access_token(
        data={"sub": user.username}
    )
    
    # Create refresh token
    refresh_token = security_service.create_access_token(
        data={"sub": user.username, "type": "refresh"},
        expires_delta=timedelta(days=30)
    )
    
    # Log audit
    await audit_service.log_action(
        action="LOGIN",
        entity_type="USER",
        entity_id=user.id,
        user_id=user.id,
        tenant_id=None
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/verify-2fa", response_model=Token)
async def verify_2fa(
    code: str,
    username: str,
    db: Session = Depends(get_db)
):
    """
    Verify 2FA code and get access token.
    """
    security_service = SecurityService()
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Get user
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify 2FA code
    if not two_factor_auth.verify_code(user.id, code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 2FA code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = security_service.create_access_token(
        data={"sub": user.username}
    )
    
    # Create refresh token
    refresh_token = security_service.create_access_token(
        data={"sub": user.username, "type": "refresh"},
        expires_delta=timedelta(days=30)
    )
    
    # Log audit
    await audit_service.log_action(
        action="2FA_VERIFY",
        entity_type="USER",
        entity_id=user.id,
        user_id=user.id,
        tenant_id=None
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Get a new access token using refresh token.
    """
    security_service = SecurityService()
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    try:
        # Verify refresh token
        payload = security_service.verify_token(refresh_token_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user
        user = user_service.get_user_by_username(refresh_token_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create new access token
        access_token = security_service.create_access_token(
            data={"sub": user.username}
        )
        
        # Create new refresh token
        new_refresh_token = security_service.create_access_token(
            data={"sub": user.username, "type": "refresh"},
            expires_delta=timedelta(days=30)
        )
        
        # Log audit
        await audit_service.log_action(
            action="REFRESH_TOKEN",
            entity_type="USER",
            entity_id=user.id,
            user_id=user.id,
            tenant_id=None
        )
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout current user.
    """
    # Log audit
    audit_service = AuditService(db)
    await audit_service.log_action(
        action="LOGOUT",
        entity_type="USER",
        entity_id=current_user.id,
        user_id=current_user.id,
        tenant_id=None
    )
    
    return {"message": "Successfully logged out"}
