-- Initial Schema Migration
-- Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
-- All rights reserved.

-- Create Tenants Table
CREATE TABLE dbo.Tenants (
    TenantID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Domain NVARCHAR(200) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE()
)
GO

-- Create Permissions Table
CREATE TABLE dbo.Permissions (
    PermissionID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Code NVARCHAR(200) NOT NULL UNIQUE,
    Description NVARCHAR(255),
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE()
)
GO

-- Create Roles Table
CREATE TABLE dbo.Roles (
    RoleID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Description NVARCHAR(255),
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    TenantID INT NOT NULL,
    CONSTRAINT FK_Roles_Tenants FOREIGN KEY (TenantID) REFERENCES dbo.Tenants(TenantID)
)
GO

-- Create Users Table
CREATE TABLE dbo.Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(200) NOT NULL UNIQUE,
    HashedPassword NVARCHAR(200) NOT NULL,
    FirstName NVARCHAR(200),
    LastName NVARCHAR(200),
    IsActive BIT NOT NULL DEFAULT 1,
    IsSuperuser BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    TenantID INT NOT NULL,
    CONSTRAINT FK_Users_Tenants FOREIGN KEY (TenantID) REFERENCES dbo.Tenants(TenantID)
)
GO

-- Create Role Permissions Table
CREATE TABLE dbo.RolePermissions (
    RoleID INT NOT NULL,
    PermissionID INT NOT NULL,
    PRIMARY KEY (RoleID, PermissionID),
    CONSTRAINT FK_RolePermissions_Roles FOREIGN KEY (RoleID) REFERENCES dbo.Roles(RoleID),
    CONSTRAINT FK_RolePermissions_Permissions FOREIGN KEY (PermissionID) REFERENCES dbo.Permissions(PermissionID)
)
GO

-- Create User Roles Table
CREATE TABLE dbo.UserRoles (
    UserID INT NOT NULL,
    RoleID INT NOT NULL,
    PRIMARY KEY (UserID, RoleID),
    CONSTRAINT FK_UserRoles_Users FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID),
    CONSTRAINT FK_UserRoles_Roles FOREIGN KEY (RoleID) REFERENCES dbo.Roles(RoleID)
)
GO

-- Create Refresh Tokens Table
CREATE TABLE dbo.RefreshTokens (
    TokenID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    Token NVARCHAR(500) NOT NULL UNIQUE,
    ExpiresAt DATETIME2 NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    RevokedAt DATETIME2,
    CONSTRAINT FK_RefreshTokens_Users FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
)
GO

-- Create Two Factor Authentication Table
CREATE TABLE dbo.TwoFactorAuth (
    TwoFactorID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    Secret NVARCHAR(100) NOT NULL,
    IsEnabled BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_TwoFactorAuth_Users FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
)
GO

-- Create Audit Log Table
CREATE TABLE dbo.AuditLogs (
    AuditID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT,
    Action NVARCHAR(100) NOT NULL,
    EntityType NVARCHAR(100) NOT NULL,
    EntityID NVARCHAR(100),
    Details NVARCHAR(MAX),
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_AuditLogs_Users FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
)
GO
