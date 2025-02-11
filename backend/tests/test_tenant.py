import pytest
from fastapi import status

def test_create_tenant(client, auth_headers):
    """Test tenant creation"""
    response = client.post(
        "/api/v1/tenants/",
        headers=auth_headers,
        json={
            "name": "New Tenant",
            "domain": "new.example.com",
            "settings": {
                "timezone": "America/Sao_Paulo",
                "currency": "BRL"
            }
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Tenant"
    assert data["is_active"] == True

def test_get_tenant(client, test_tenant, auth_headers):
    """Test getting tenant details"""
    response = client.get(
        f"/api/v1/tenants/{test_tenant.tenant_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tenant_id"] == test_tenant.tenant_id
    assert data["name"] == test_tenant.name

def test_update_tenant(client, test_tenant, auth_headers):
    """Test updating tenant"""
    new_name = "Updated Tenant"
    response = client.put(
        f"/api/v1/tenants/{test_tenant.tenant_id}",
        headers=auth_headers,
        json={
            "name": new_name,
            "settings": {
                "timezone": "America/Sao_Paulo"
            }
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == new_name

def test_delete_tenant(client, test_tenant, auth_headers):
    """Test tenant deletion (soft delete)"""
    response = client.delete(
        f"/api/v1/tenants/{test_tenant.tenant_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_list_tenants(client, test_tenant, auth_headers):
    """Test listing tenants"""
    response = client.get(
        "/api/v1/tenants/",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(t["tenant_id"] == test_tenant.tenant_id for t in data)

def test_tenant_wizard(client, auth_headers):
    """Test tenant creation wizard"""
    response = client.post(
        "/api/v1/tenants/wizard/create",
        headers=auth_headers,
        json={
            "tenant": {
                "name": "Wizard Tenant",
                "domain": "wizard.example.com",
                "settings": {
                    "timezone": "America/Sao_Paulo",
                    "currency": "BRL"
                }
            },
            "admin": {
                "email": "admin@wizard.example.com",
                "password": "adminpass123",
                "full_name": "Admin User"
            },
            "template_id": "financial"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "tenant" in data
    assert "admin_user" in data
    assert "database" in data
