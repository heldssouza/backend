import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio
from uuid import UUID
from datetime import datetime, timedelta
from app.main import app
from app.models.master.role import Role
from app.models.master.permission import Permission
from app.models.master.user import User
from app.core.auth.jwt import create_access_token

# Test tenant ID
TEST_TENANT_ID = "00000000-0000-0000-0000-000000000002"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def admin_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
        json={
            "email": "admin@example.com",
            "username": "adminuser",
            "password": "admin123!@#",
            "is_active": True,
            "is_superuser": True
        }
    )
    return response.json()

@pytest.fixture
async def regular_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
        json={
            "email": "user@example.com",
            "username": "regularuser",
            "password": "user123!@#",
            "is_active": True,
            "is_superuser": False
        }
    )
    return response.json()

@pytest.fixture
async def test_role(client, admin_token):
    response = await client.post(
        "/api/v1/roles",
        headers={
            "X-Tenant-ID": TEST_TENANT_ID,
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "test_role",
            "description": "Role for testing",
            "permissions": ["read:users", "write:users"]
        }
    )
    return response.json()

@pytest.fixture
def admin_token(client):
    # Register admin user
    client.post(
        "/api/v1/auth/register",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
        json={
            "email": "admin@example.com",
            "username": "adminuser",
            "password": "admin123!@#",
            "is_active": True,
            "is_superuser": True
        }
    )

    # Login and get token
    response = client.post(
        "/api/v1/auth/login",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
        json={
            "username": "adminuser",
            "password": "admin123!@#"
        }
    )
    return response.json()["access_token"]

class TestHealthCheck:
    async def test_health_check(self, client):
        response = await client.get(
            "/api/v1/health",
            headers={"X-Tenant-ID": TEST_TENANT_ID}
        )
        assert response.status_code == 200
        data = response.json()
        assert "services" in data
        assert "database" in data["services"]
        assert data["services"]["database"] in ["ok", "error"]

class TestAuth:
    async def test_register_user(self, client):
        response = await client.post(
            "/api/v1/auth/register",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
                "is_active": True,
                "is_superuser": False
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "email" in data
        assert data["email"] == "test@example.com"

    async def test_login_user(self, client):
        # First register a user
        client.post(
            "/api/v1/auth/register",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "email": "login@example.com",
                "username": "loginuser",
                "password": "testpass123",
                "is_active": True,
                "is_superuser": False
            }
        )

        # Then try to login
        response = await client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "username": "loginuser",
                "password": "testpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    async def test_invalid_login(self, client):
        response = await client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "username": "nonexistent",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

class TestTenant:
    async def test_tenant_isolation(self, client):
        # Create a user in tenant 1
        response = await client.post(
            "/api/v1/auth/register",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "email": "tenant1@example.com",
                "username": "tenant1user",
                "password": "testpass123",
                "is_active": True,
                "is_superuser": False
            }
        )
        assert response.status_code == 201

        # Try to login with the same credentials but different tenant
        response = await client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": "00000000-0000-0000-0000-000000000001"},  # Master tenant
            json={
                "username": "tenant1user",
                "password": "testpass123"
            }
        )
        assert response.status_code == 401

    async def test_missing_tenant_header(self, client):
        response = await client.get("/api/v1/health")  # No X-Tenant-ID header
        assert response.status_code == 400
        assert "X-Tenant-ID header is required" in response.json()["detail"]

class TestRoles:
    async def test_create_role(self, client, admin_token):
        response = await client.post(
            "/api/v1/roles",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name": "manager",
                "description": "Manager role",
                "permissions": ["read:all", "write:users"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "manager"
        assert "created_at" in data
        assert "created_by" in data

    async def test_role_tenant_isolation(self, client, admin_token):
        # Create role in tenant 1
        response1 = await client.post(
            "/api/v1/roles",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name": "isolated_role",
                "description": "Test isolation",
                "permissions": ["read:users"]
            }
        )
        assert response1.status_code == 201

        # Try to access role from tenant 2
        other_tenant = "00000000-0000-0000-0000-000000000003"
        response2 = await client.get(
            "/api/v1/roles/isolated_role",
            headers={
                "X-Tenant-ID": other_tenant,
                "Authorization": f"Bearer {admin_token}"
            }
        )
        assert response2.status_code == 404

class TestAudit:
    async def test_audit_fields_on_create(self, client, admin_token):
        response = await client.post(
            "/api/v1/roles",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name": "audit_test",
                "description": "Test audit fields",
                "permissions": ["read:users"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "created_at" in data
        assert "created_by" in data
        assert data["created_at"] is not None
        assert data["created_by"] is not None
        assert "updated_at" in data
        assert "updated_by" in data
        assert not data["is_deleted"]

class TestTwoFactorAuth:
    async def test_enable_2fa(self, client, regular_user):
        # Request 2FA setup
        response = await client.post(
            "/api/v1/auth/2fa/setup",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={"user_id": regular_user["id"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "secret" in data
        assert "qr_code" in data

    async def test_verify_2fa(self, client, regular_user):
        # Setup 2FA first
        setup_response = await client.post(
            "/api/v1/auth/2fa/setup",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={"user_id": regular_user["id"]}
        )
        secret = setup_response.json()["secret"]

        # Generate test TOTP code
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()

        # Verify the code
        response = await client.post(
            "/api/v1/auth/2fa/verify",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "user_id": regular_user["id"],
                "code": code
            }
        )
        assert response.status_code == 200

class TestRefreshToken:
    async def test_refresh_token_flow(self, client, regular_user):
        # Login to get initial tokens
        login_response = await client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "username": regular_user["username"],
                "password": "user123!@#"
            }
        )
        assert login_response.status_code == 200
        tokens = login_response.json()
        refresh_token = tokens["refresh_token"]

        # Use refresh token to get new access token
        response = await client.post(
            "/api/v1/auth/refresh",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        new_tokens = response.json()
        assert "access_token" in new_tokens
        assert new_tokens["access_token"] != tokens["access_token"]

class TestSecurityLogs:
    async def test_security_event_logging(self, client, admin_token):
        # Perform a security-sensitive action
        response = await client.post(
            "/api/v1/roles",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name": "logged_role",
                "description": "Test security logging",
                "permissions": ["admin:all"]
            }
        )
        assert response.status_code == 201

        # Check security logs
        logs_response = await client.get(
            "/api/v1/security/logs",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            }
        )
        assert logs_response.status_code == 200
        logs = logs_response.json()
        assert len(logs) > 0
        latest_log = logs[0]
        assert latest_log["event_type"] == "role_created"
        assert latest_log["tenant_id"] == TEST_TENANT_ID
        assert "timestamp" in latest_log
        assert "user_id" in latest_log
