from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from app.core.config.settings import get_settings
from app.core.tenant.context import TenantContext
from typing import Dict, Optional
import pyodbc

settings = get_settings()

class DatabaseSessionManager:
    def __init__(self):
        self._engines: Dict[str, create_engine] = {}
        self._session_factories: Dict[str, sessionmaker] = {}
    
    def get_connection_string(self, tenant_id: str) -> str:
        return (
            f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{tenant_id}?"
            f"driver={settings.DB_DRIVER}"
        )
    
    def get_engine(self, tenant_id: str):
        if tenant_id not in self._engines:
            connection_string = self.get_connection_string(tenant_id)
            self._engines[tenant_id] = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800
            )
        return self._engines[tenant_id]
    
    def get_session_factory(self, tenant_id: str) -> sessionmaker:
        if tenant_id not in self._session_factories:
            engine = self.get_engine(tenant_id)
            self._session_factories[tenant_id] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        return self._session_factories[tenant_id]
    
    def get_session(self) -> Session:
        tenant_id = TenantContext.get_tenant_id()
        if not tenant_id:
            raise ValueError("Tenant ID not set in context")
        
        session_factory = self.get_session_factory(tenant_id)
        return session_factory()

db_manager = DatabaseSessionManager()

def get_db() -> Session:
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()
