import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio
from uuid import UUID
from app.main import app

# Test tenant ID
TEST_TENANT_ID = "00000000-0000-0000-0000-000000000002"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get(
        "/api/v1/health",
        headers={"X-Tenant-ID": TEST_TENANT_ID}
    )
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert "database" in data["services"]
    assert data["services"]["database"] in ["ok", "error"]

class TestAuth:
    def test_register_user(self, client):
        response = client.post(
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
        print("Register response:", response.json())
        assert response.status_code == 201
        data = response.json()
        assert "email" in data
        assert data["email"] == "test@example.com"

    def test_login_user(self, client):
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
        response = client.post(
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

    def test_invalid_login(self, client):
        response = client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": TEST_TENANT_ID},
            json={
                "username": "nonexistent",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

class TestTenant:
    def test_tenant_isolation(self, client):
        # Create a user in tenant 1
        response = client.post(
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
        response = client.post(
            "/api/v1/auth/login",
            headers={"X-Tenant-ID": "00000000-0000-0000-0000-000000000001"},  # Master tenant
            json={
                "username": "tenant1user",
                "password": "testpass123"
            }
        )
        assert response.status_code == 401

    def test_missing_tenant_header(self, client):
        response = client.get("/api/v1/health")  # No X-Tenant-ID header
        assert response.status_code == 400
        assert "X-Tenant-ID header is required" in response.json()["detail"]

@pytest.fixture
def admin_token(client):
    # Register admin user
    client.post(
        "/api/v1/auth/register",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
        json={
            "email": "admin@example.com",
            "username": "adminuser",
            "password": "adminpass123",
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
            "password": "adminpass123"
        }
    )
    return response.json()["access_token"]

class TestRBAC:
    def test_admin_access(self, client, admin_token):
        response = client.get(
            "/api/v1/users",
            headers={
                "X-Tenant-ID": TEST_TENANT_ID,
                "Authorization": f"Bearer {admin_token}"
            }
        )
        assert response.status_code == 200

class TestRateLimiting:
    def test_rate_limiting(self, client):
        # Make multiple requests in quick succession
        for _ in range(5):
            client.get(
                "/api/v1/health",
                headers={"X-Tenant-ID": TEST_TENANT_ID}
            )

        # The next request should be rate limited
        response = client.get(
            "/api/v1/health",
            headers={"X-Tenant-ID": TEST_TENANT_ID}
        )
        assert response.status_code == 429  # Too Many Requests
