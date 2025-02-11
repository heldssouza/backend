"""
Application Settings
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from typing import Optional, Dict, Any
from pydantic import RedisDsn, validator
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings with validation and documentation.
    
    Features:
    1. Environment variable support
    2. Type validation
    3. Default values
    4. Secure secrets handling
    5. Connection string validation
    """
    
    # Application
    APP_NAME: str = "BControlTech Financial API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST_SIZE: int = 10
    RATE_LIMIT_WINDOW_SIZE: int = 60
    
    # Database
    SQL_SERVER: str
    SQL_USER: str
    SQL_PASSWORD: str
    SQL_PROD_DB: str
    SQL_TEST_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # Database Connection Settings
    DB_DRIVER: str = "ODBC Driver 18 for SQL Server"
    DB_ENCRYPT: bool = True
    DB_TRUST_SERVER_CERTIFICATE: bool = False
    DB_CONNECTION_TIMEOUT: int = 30
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        server = values.get("SQL_SERVER")
        username = values.get("SQL_USER")
        password = values.get("SQL_PASSWORD")
        db = values.get("SQL_PROD_DB")
        
        return f"mssql+pymssql://{username}:{password}@{server}/{db}"
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_URI: Optional[RedisDsn] = None
    REDIS_URL: Optional[str] = None
    
    @validator("REDIS_URI", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        host = values.get("REDIS_HOST")
        port = values.get("REDIS_PORT", 6379)
        password = values.get("REDIS_PASSWORD")
        db = values.get("REDIS_DB", 0)
        
        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        return f"redis://{host}:{port}/{db}"
    
    # Tenant
    TENANT_HEADER_KEY: str = "X-Tenant-ID"
    DEFAULT_TENANT_ID: str = "default"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []
    
    # Legacy Settings Support
    PROJECT_NAME: Optional[str] = None
    VERSION: Optional[str] = None
    API_V1_STR: Optional[str] = None
    
    model_config = ConfigDict(
        env_file=".env",
        extra="allow"  # Permite campos extras
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()
