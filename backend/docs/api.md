# API Documentation

## Authentication

### Login
```http
POST /api/v1/auth/token
```
Login with email and password to get access token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Get Current User
```http
GET /api/v1/auth/me
```
Get details of currently authenticated user.

**Response:**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true
}
```

## Tenants

### Create Tenant
```http
POST /api/v1/tenants/
```
Create a new tenant.

**Request Body:**
```json
{
  "name": "New Tenant",
  "domain": "tenant.example.com",
  "settings": {
    "timezone": "America/Sao_Paulo",
    "currency": "BRL"
  }
}
```

### Create Tenant with Wizard
```http
POST /api/v1/tenants/wizard/create
```
Create a new tenant with complete setup.

**Request Body:**
```json
{
  "tenant": {
    "name": "New Tenant",
    "domain": "tenant.example.com",
    "settings": {
      "timezone": "America/Sao_Paulo",
      "currency": "BRL"
    }
  },
  "admin": {
    "email": "admin@tenant.example.com",
    "password": "adminpass123",
    "full_name": "Admin User"
  },
  "template_id": "financial"
}
```

## Users

### Create User
```http
POST /api/v1/users/
```
Create a new user.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "userpass123",
  "full_name": "New User",
  "role_ids": [1, 2]
}
```

### Assign Role
```http
POST /api/v1/users/{user_id}/roles/{role_id}
```
Assign a role to a user.

## Roles

### Create Role
```http
POST /api/v1/roles/
```
Create a new role.

**Request Body:**
```json
{
  "name": "Manager",
  "description": "Department manager",
  "permissions": ["VIEW_REPORTS", "APPROVE_TRANSACTIONS"]
}
```

## Health Checks

### System Health
```http
GET /health
```
Get overall system health status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": {
      "status": "healthy"
    },
    "redis": {
      "status": "healthy"
    }
  },
  "metrics": {
    "cpu_percent": 45.2,
    "memory_percent": 78.5,
    "disk_usage_percent": 62.1
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
