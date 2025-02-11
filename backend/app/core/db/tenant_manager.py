from typing import Dict, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from app.core.config.database import get_database_url
from app.core.security.crypto import encrypt_connection_string
import logging

logger = logging.getLogger(__name__)

# Cache of tenant database engines
tenant_engines: Dict[int, 'Engine'] = {}


async def create_tenant_database(db_name: str, encryption_key: str) -> bool:
    """
    Create a new tenant database with encryption
    """
    try:
        # Get master database connection
        master_url = get_database_url()
        engine = create_engine(master_url)
        
        with engine.connect() as conn:
            # Create database with encryption
            conn.execute(f"""
                CREATE DATABASE {db_name}
                COLLATE Latin1_General_CI_AI
                WITH ENCRYPTION
            """)
            
            # Set encryption key
            conn.execute(f"""
                USE {db_name};
                CREATE MASTER KEY ENCRYPTION BY PASSWORD = '{encryption_key}';
            """)
            
            # Create audit schema
            conn.execute(f"""
                USE {db_name};
                CREATE SCHEMA audit;
            """)
            
            # Enable row-level security
            conn.execute(f"""
                USE {db_name};
                ALTER DATABASE {db_name} SET ALLOW_SNAPSHOT_ISOLATION ON;
                ALTER DATABASE {db_name} SET READ_COMMITTED_SNAPSHOT ON;
            """)
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to create tenant database: {str(e)}")
        raise


def get_tenant_session(tenant_id: int) -> Session:
    """
    Get a database session for a specific tenant
    """
    if tenant_id not in tenant_engines:
        # Create new engine for tenant
        db_url = get_tenant_database_url(tenant_id)
        engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
        tenant_engines[tenant_id] = engine
    
    # Create session
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=tenant_engines[tenant_id]
    )
    return SessionLocal()


def get_tenant_database_url(tenant_id: int) -> str:
    """
    Get database URL for tenant
    """
    base_url = get_database_url()
    return base_url.replace(
        "master",
        f"tenant_{tenant_id}"
    )


def close_tenant_connections():
    """
    Close all tenant database connections
    """
    for engine in tenant_engines.values():
        engine.dispose()
    tenant_engines.clear()


class TenantDatabaseManager:
    """
    Context manager for tenant database sessions
    """
    def __init__(self, tenant_id: int):
        self.tenant_id = tenant_id
        self.session: Optional[Session] = None

    async def __aenter__(self) -> Session:
        self.session = get_tenant_session(self.tenant_id)
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
