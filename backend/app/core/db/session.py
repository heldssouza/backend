"""Database session configuration."""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config.database import get_database_settings

settings = get_database_settings()

# Create SQLAlchemy engine
engine = create_engine(
    settings.MASTER_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DBSessionManager:
    """Manager for tenant-specific database sessions."""
    
    def __init__(self):
        self.engines = {}
        self.session_factories = {}
    
    def get_tenant_session(self, tenant_db_name: str) -> Session:
        """
        Get session for specific tenant.
        
        Args:
            tenant_db_name: Name of tenant database
            
        Returns:
            Session: Database session for tenant
        """
        if tenant_db_name not in self.engines:
            # Create new engine for tenant
            engine = create_engine(
                settings.get_tenant_database_url(tenant_db_name),
                pool_pre_ping=True,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW
            )
            self.engines[tenant_db_name] = engine
            self.session_factories[tenant_db_name] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        
        return self.session_factories[tenant_db_name]()
