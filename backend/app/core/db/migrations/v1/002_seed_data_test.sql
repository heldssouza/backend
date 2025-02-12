-- Initial Data Migration
-- Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
-- All rights reserved.

-- Create test tenant
DECLARE @TestTenantID UNIQUEIDENTIFIER = '00000000-0000-0000-0000-000000000002';

INSERT INTO [dbo].[Tenants] ([TenantID], [Name], [Domain], [IsActive])
VALUES (@TestTenantID, 'Test', 'test', 1);

-- Create test admin role
INSERT INTO [dbo].[Roles] (
    [Name],
    [Description],
    [IsActive],
    [TenantID]
)
VALUES (
    'test_admin',
    'Test Administrator',
    1,
    @TestTenantID
);

-- Create test admin user (password: Test@123)
INSERT INTO [dbo].[Users] (
    [Email],
    [HashedPassword],
    [FirstName],
    [LastName],
    [IsActive],
    [IsSuperuser],
    [TenantID],
    [Username]
)
VALUES (
    'test@bcontroltech.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNfh/geL.SoVu',
    'Test',
    'Administrator',
    1,
    1,
    @TestTenantID,
    'test'
);

-- Assign test admin role to test admin user
INSERT INTO [dbo].[UserRoles] (
    [UserID],
    [RoleID]
)
SELECT u.UserID, r.RoleID
FROM [dbo].[Users] u
CROSS JOIN [dbo].[Roles] r
WHERE u.Email = 'test@bcontroltech.com'
AND r.Name = 'test_admin';
