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
    SQL_SERVER: str = "${SQL_SERVER}"
    SQL_USER: str = "${SQL_USER}"
    SQL_PASSWORD: str = "${SQL_PASSWORD}"
    SQL_PROD_DB: str = "${SQL_PROD_DB}"
    SQL_TEST_DB: str = "${SQL_TEST_DB}"
    SQL_PORT: int = 1433
    SQL_ENCRYPT: bool = True
    SQL_TRUST_SERVER_CERTIFICATE: bool = False
    SQL_CONNECTION_TIMEOUT: int = 30
    
    # Connection Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    def _build_connection_string(self, database: str) -> str:
        """Build SQL Server connection string with proper configuration."""
        return (
            f"mssql+pyodbc:///?odbc_connect="
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server=tcp:{self.SQL_SERVER},{self.SQL_PORT};"
            f"Database={database};"
            f"Uid={self.SQL_USER};"
            f"Pwd={self.SQL_PASSWORD};"
            f"Encrypt={'yes' if self.SQL_ENCRYPT else 'no'};"
            f"TrustServerCertificate={'yes' if self.SQL_TRUST_SERVER_CERTIFICATE else 'no'};"
            f"Connection Timeout={self.SQL_CONNECTION_TIMEOUT}"
        )

    @property
    def MASTER_DATABASE_URL(self) -> str:
        """Generate master database connection string."""
        return self._build_connection_string(self.SQL_PROD_DB)

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Generate test database connection string."""
        return self._build_connection_string(self.SQL_TEST_DB)

    def get_tenant_database_url(self, tenant_db_name: str) -> str:
        """Generate tenant-specific database connection string."""
        return self._build_connection_string(tenant_db_name)

    model_config = ConfigDict(env_file=".env.test", extra="allow")


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    """Get cached database settings."""
    return DatabaseSettings()
