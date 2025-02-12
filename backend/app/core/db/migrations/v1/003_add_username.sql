-- Add Username column to Users table
ALTER TABLE dbo.Users
ADD Username NVARCHAR(100) NULL;
GO

-- Update existing users to have a username based on their email
UPDATE dbo.Users
SET Username = LEFT(Email, CHARINDEX('@', Email) - 1)
WHERE Username IS NULL;
GO

-- Add unique index
CREATE UNIQUE NONCLUSTERED INDEX IX_Users_Username
ON dbo.Users(Username)
WHERE Username IS NOT NULL;
GO

-- Make Username column not null 
ALTER TABLE dbo.Users
ALTER COLUMN Username NVARCHAR(100) NOT NULL;
GO
