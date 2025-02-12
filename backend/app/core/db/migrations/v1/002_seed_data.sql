-- Initial Data Migration
-- Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
-- All rights reserved.

-- Enable IDENTITY_INSERT and insert Master Tenant
SET IDENTITY_INSERT [dbo].[Tenants] ON;

INSERT INTO [dbo].[Tenants] ([TenantID], [Name], [Domain], [IsActive])
VALUES (1, 'Master', 'master', 1);

SET IDENTITY_INSERT [dbo].[Tenants] OFF;

-- Create admin role
INSERT INTO [dbo].[Roles] (
    [Name],
    [Description],
    [IsActive],
    [TenantID]
)
VALUES (
    'admin',
    'System Administrator',
    1,
    1
);

-- Create admin user (password: Admin@123)
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
    'admin@bcontroltech.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNfh/geL.SoVu',
    'System',
    'Administrator',
    1,
    1,
    1,
    'admin'
);

-- Assign admin role to admin user
INSERT INTO [dbo].[UserRoles] (
    [UserID],
    [RoleID]
)
SELECT u.UserID, r.RoleID
FROM [dbo].[Users] u
CROSS JOIN [dbo].[Roles] r
WHERE u.Email = 'admin@bcontroltech.com'
AND r.Name = 'admin';
