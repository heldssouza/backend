"""
Database Configuration
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import ConfigDict


class DatabaseSettings(BaseSettings):
    """
    Database settings with validation and documentation.
    
    Features:
    1. Environment variable support
    2. Type validation
    3. Default values
    4. Connection string generation
    5. Tenant database support
    """

    # Server Configuration
    SQL_SERVER: str = "localhost"
    SQL_USER: str = "sa"
    SQL_PASSWORD: str = ""
    SQL_PROD_DB: str = "fdw00"
    SQL_TEST_DB: str = "fdw00_test"
    
    # Connection Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    @property
    def MASTER_DATABASE_URL(self) -> str:
        """Generate master database connection string."""
        return f"mssql+pymssql://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{self.SQL_PROD_DB}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Generate test database connection string."""
        return f"mssql+pymssql://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{self.SQL_TEST_DB}"

    def get_tenant_database_url(self, tenant_db_name: str) -> str:
        """Generate tenant-specific database connection string."""
        return f"mssql+pymssql://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{tenant_db_name}"

    model_config = ConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    """Get cached database settings."""
    return DatabaseSettings()
