import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.database import get_database_settings
from app.core.db.base import Base
from app.main import app
from app.core.db.session import get_db
import os
import logging

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database settings
os.environ["ENV_FILE"] = ".env.test"
db_settings = get_database_settings()

# Test database URL (use a separate database for testing)
TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    db_settings.get_tenant_database_url("test_db")
)

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(
        TEST_DB_URL,
        pool_pre_ping=True,
        pool_size=db_settings.DB_POOL_SIZE,
        max_overflow=db_settings.DB_MAX_OVERFLOW
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    return engine

@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """Create test database session factory"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

@pytest.fixture(scope="function")
def db_session(TestingSessionLocal):
    """Create a fresh database session for a test"""
    connection = TestingSessionLocal()

    # Begin a nested transaction
    transaction = connection.begin_nested()

    yield connection

    # Rollback the nested transaction
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a test database session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_tenant(db_session):
    """Create a test tenant"""
    from app.models.master.tenant import Tenant

    tenant = Tenant(
        name="Test Tenant",
        subdomain="test",
        database_name="test_db",
        is_active=True
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant

@pytest.fixture(scope="function")
def test_user(db_session, test_tenant):
    """Create a test user"""
    from app.models.master.user import User
    from app.core.security.auth import get_password_hash

    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpassword"),
        first_name="Test",
        last_name="User",
        is_active=True,
        tenant_id=test_tenant.id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_role(db_session):
    """Create a test role"""
    from app.models.master.role import Role

    role = Role(
        name="test_role",
        description="Test Role"
    )
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role

@pytest.fixture(scope="function")
def test_permission(db_session):
    """Create a test permission"""
    from app.models.master.role import Permission

    permission = Permission(
        code="test_permission",
        description="Test Permission"
    )
    db_session.add(permission)
    db_session.commit()
    db_session.refresh(permission)
    return permission

@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Create authentication headers for test user"""
    from app.core.security.auth import SecurityService
    from datetime import timedelta

    access_token = SecurityService.create_access_token(
        data={"sub": test_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}
