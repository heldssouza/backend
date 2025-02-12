"""
Authentication service.
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security.password import get_password_hash, verify_password
from app.models.master.user import User
from app.schemas.master.user import UserCreate

settings = get_settings()


class SecurityService:
    """Security service for authentication and authorization."""

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username or email
            password: Plain password
            
        Returns:
            User if authenticated, None otherwise
        """
        # Try to find user by username or email
        user = (
            self.db.query(User)
            .filter(
                (User.username == username) | (User.email == username)
            )
            .first()
        )
        
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Token data
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
            
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

    def create_user(self, user_data: UserCreate) -> User:
        """
        Create new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user
        """
        # Check if username exists
        if (
            self.db.query(User)
            .filter(User.username == user_data.username)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email exists
        if (
            self.db.query(User)
            .filter(User.email == user_data.email)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
            tenant_id=user_data.tenant_id
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
