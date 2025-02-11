import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest_asyncio
from typing import AsyncGenerator, Dict
import json
import redis.asyncio as redis
from jose import jwt

# Importar a aplicação principal
from app.main import app
from app.core.config.settings import get_settings
from app.core.config.database import get_database_settings

settings = get_settings()
db_settings = get_database_settings()

# Fixtures
@pytest.fixture
def client():
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def test_tenant_headers():
    return {
        "X-Tenant-ID": "test_tenant",
        "Content-Type": "application/json"
    }

@pytest.fixture
def redis_client():
    return redis.Redis.from_url(settings.REDIS_URL)

# Testes de Health Check
def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database" in data
    assert "redis" in data

# Testes de Autenticação
class TestAuth:
    def test_register_user(self, client, test_tenant_headers):
        user_data = {
            "email": "test@example.com",
            "password": "Test123!",
            "full_name": "Test User"
        }
        response = client.post(
            "/api/v1/auth/register",
            json=user_data,
            headers=test_tenant_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == user_data["email"]

    def test_login_user(self, client, test_tenant_headers):
        login_data = {
            "username": "test@example.com",
            "password": "Test123!"
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data,
            headers=test_tenant_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_invalid_login(self, client, test_tenant_headers):
        login_data = {
            "username": "test@example.com",
            "password": "wrong_password"
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data,
            headers=test_tenant_headers
        )
        assert response.status_code == 401

# Testes de Tenant
class TestTenant:
    def test_tenant_isolation(self, client):
        # Teste com tenant1
        headers_tenant1 = {"X-Tenant-ID": "tenant1"}
        response1 = client.get("/api/v1/users/me", headers=headers_tenant1)
        assert response1.status_code == 401  # Não autorizado sem token

        # Teste com tenant2
        headers_tenant2 = {"X-Tenant-ID": "tenant2"}
        response2 = client.get("/api/v1/users/me", headers=headers_tenant2)
        assert response2.status_code == 401  # Não autorizado sem token

    def test_missing_tenant_header(self, client):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 400
        assert "tenant" in response.json()["detail"].lower()

# Testes de RBAC
class TestRBAC:
    @pytest.fixture
    def admin_token(self, client, test_tenant_headers):
        # Login como admin
        login_data = {
            "username": "admin@example.com",
            "password": "admin123"
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data,
            headers=test_tenant_headers
        )
        return response.json()["access_token"]

    def test_admin_access(self, client, test_tenant_headers, admin_token):
        headers = {
            **test_tenant_headers,
            "Authorization": f"Bearer {admin_token}"
        }
        response = client.get("/api/v1/users", headers=headers)
        assert response.status_code == 200

# Testes de Rate Limiting
class TestRateLimiting:
    async def test_rate_limiting(self, async_client, test_tenant_headers):
        # Fazer múltiplas requisições rápidas
        responses = []
        for _ in range(100):
            response = await async_client.get(
                "/api/v1/health",
                headers=test_tenant_headers
            )
            responses.append(response.status_code)

        # Deve haver alguns 429 (Too Many Requests)
        assert 429 in responses

if __name__ == "__main__":
    pytest.main(["-v", __file__])
