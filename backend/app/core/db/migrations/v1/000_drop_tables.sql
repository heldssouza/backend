-- Try up to 3 times to drop everything
DECLARE @RetryCount INT = 0;
DECLARE @MaxRetries INT = 3;
DECLARE @Success BIT = 0;

WHILE @RetryCount <= @MaxRetries AND @Success = 0
BEGIN
    BEGIN TRY
        -- List all foreign keys and their tables
        SELECT 
            fk.name AS ForeignKeyName,
            OBJECT_NAME(fk.parent_object_id) AS TableName,
            COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ColumnName,
            OBJECT_NAME(fk.referenced_object_id) AS ReferencedTableName,
            COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ReferencedColumnName
        FROM sys.foreign_keys AS fk
        INNER JOIN sys.foreign_key_columns AS fkc 
            ON fk.object_id = fkc.constraint_object_id
        ORDER BY TableName, ForeignKeyName;

        -- First attempt to drop foreign keys and tables
        PRINT 'First attempt to drop foreign keys and tables';

        -- Drop all foreign key constraints
        DECLARE @DropFKSQL nvarchar(max) = N'';

        SELECT @DropFKSQL = @DropFKSQL + N'
            ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
            + '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) 
            + ' DROP CONSTRAINT '
            + QUOTENAME(name) + ';'
        FROM sys.foreign_keys;

        IF @DropFKSQL IS NOT NULL AND LEN(@DropFKSQL) > 0
        BEGIN
            PRINT 'Dropping foreign keys (First attempt):';
            PRINT @DropFKSQL;
            EXEC sp_executesql @DropFKSQL;
        END

        -- Drop all tables in correct order
        DECLARE @dropTables NVARCHAR(MAX) = '';

        -- Drop tables in correct order
        DECLARE @tables TABLE (
            TableName NVARCHAR(128),
            DropOrder INT
        )

        -- Define the order to drop tables
        INSERT INTO @tables (TableName, DropOrder) VALUES 
        ('AuditLogs', 1),
        ('TwoFactorAuth', 2),
        ('RefreshTokens', 3),
        ('UserRoles', 4),
        ('RolePermissions', 5),
        ('Roles', 7),
        ('Permissions', 8),
        ('Tenants', 9),
        ('Users', 10)

        -- Generate drop statements in order
        SELECT @dropTables = @dropTables + 
            'DROP TABLE IF EXISTS [dbo].[' + TableName + '];' + CHAR(13)
        FROM @tables
        ORDER BY DropOrder;

        PRINT 'Dropping tables (First attempt):';
        PRINT @dropTables;

        EXEC sp_executesql @dropTables;

        -- Wait for 2 seconds
        WAITFOR DELAY '00:00:02';

        -- Second attempt to drop foreign keys and tables
        PRINT 'Second attempt to drop foreign keys and tables';

        -- Drop all foreign key constraints again
        DECLARE @DropFKSQL2 nvarchar(max) = N'';

        SELECT @DropFKSQL2 = @DropFKSQL2 + N'
            ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
            + '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) 
            + ' DROP CONSTRAINT '
            + QUOTENAME(name) + ';'
        FROM sys.foreign_keys;

        IF @DropFKSQL2 IS NOT NULL AND LEN(@DropFKSQL2) > 0
        BEGIN
            PRINT 'Dropping foreign keys (Second attempt):';
            PRINT @DropFKSQL2;
            EXEC sp_executesql @DropFKSQL2;
        END

        -- Drop all tables in correct order again
        DECLARE @dropTables2 NVARCHAR(MAX) = '';

        -- Drop tables in correct order
        DECLARE @tables2 TABLE (
            TableName NVARCHAR(128),
            DropOrder INT
        )

        -- Define the order to drop tables
        INSERT INTO @tables2 (TableName, DropOrder) VALUES 
        ('AuditLogs', 1),
        ('TwoFactorAuth', 2),
        ('RefreshTokens', 3),
        ('UserRoles', 4),
        ('RolePermissions', 5),
        ('Users', 6),
        ('Roles', 7),
        ('Permissions', 8),
        ('Tenants', 9)

        -- Generate drop statements in order
        SELECT @dropTables2 = @dropTables2 + 
            'DROP TABLE IF EXISTS [dbo].[' + TableName + '];' + CHAR(13)
        FROM @tables2
        ORDER BY DropOrder;

        PRINT 'Dropping tables (Second attempt):';
        PRINT @dropTables2;

        EXEC sp_executesql @dropTables2;

        SET @Success = 1;
    END TRY
    BEGIN CATCH
        SET @RetryCount = @RetryCount + 1;
        IF @RetryCount <= @MaxRetries
        BEGIN
            PRINT 'Attempt ' + CAST(@RetryCount AS VARCHAR) + ' failed. Retrying...';
            WAITFOR DELAY '00:00:02';  -- Wait 2 seconds before retrying
        END
        ELSE
        BEGIN
            PRINT 'All attempts failed. Last error:';
            THROW;
        END
    END CATCH
END
GO
