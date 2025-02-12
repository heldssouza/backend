-- Initial Data Migration
-- Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
-- All rights reserved.

-- Insert Master Tenant
DECLARE @MasterTenantID UNIQUEIDENTIFIER = '00000000-0000-0000-0000-000000000001';

INSERT INTO [dbo].[Tenants] ([TenantID], [Name], [Domain], [IsActive])
VALUES (@MasterTenantID, 'Master', 'master', 1);

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
    @MasterTenantID
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
    @MasterTenantID,
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
