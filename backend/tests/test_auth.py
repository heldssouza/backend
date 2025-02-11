import pytest
from fastapi import status
from app.core.security.auth import verify_password

def test_login(client, test_user):
    """Test user login"""
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, test_user):
    """Test login with invalid password"""
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(client, test_user, auth_headers):
    """Test getting current user"""
    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email

def test_change_password(client, test_user, auth_headers, db_session):
    """Test password change"""
    new_password = "newpassword123"
    response = client.post(
        "/api/v1/auth/change-password",
        headers=auth_headers,
        json={
            "current_password": "testpassword",
            "new_password": new_password
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Verify password was changed
    db_session.refresh(test_user)
    assert verify_password(new_password, test_user.hashed_password)

def test_refresh_token(client, auth_headers):
    """Test token refresh"""
    response = client.post(
        "/api/v1/auth/refresh",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
