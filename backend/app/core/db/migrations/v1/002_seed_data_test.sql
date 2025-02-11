-- Initial Data Migration
-- Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
-- All rights reserved.

-- Enable IDENTITY_INSERT and insert Master Tenant
SET IDENTITY_INSERT [dbo].[tenants] ON
GO

INSERT INTO [dbo].[tenants] ([id], [name], [subdomain], [database_name], [is_active])
VALUES (1, 'Master', 'master', 'fdw00_test', 1)
GO

SET IDENTITY_INSERT [dbo].[tenants] OFF
GO

-- Create admin role
INSERT INTO [dbo].[roles] (
    [name],
    [description],
    [permissions],
    [is_active],
    [tenant_id]
)
VALUES (
    'admin',
    'System Administrator',
    'users.create,users.read,users.update,users.delete,roles.create,roles.read,roles.update,roles.delete,tenants.create,tenants.read,tenants.update,tenants.delete',
    1,
    1
)
GO

-- Create admin user (password: Admin@123)
INSERT INTO [dbo].[users] (
    [email],
    [username],
    [password_hash],
    [first_name],
    [last_name],
    [is_active],
    [is_superuser],
    [tenant_id]
)
VALUES (
    'admin@bcontroltech.com',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNfh/geL.SoVu',
    'System',
    'Administrator',
    1,
    1,
    1
)
GO

-- Assign admin role to admin user
INSERT INTO [dbo].[user_roles] (
    [user_id],
    [role_id]
)
SELECT u.id, r.id
FROM [dbo].[users] u
CROSS JOIN [dbo].[roles] r
WHERE u.username = 'admin'
AND r.name = 'admin'
GO
