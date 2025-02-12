DECLARE @sql NVARCHAR(MAX) = '';

SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id)) + 
               '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) + 
               ' DROP CONSTRAINT ' + QUOTENAME(name) + ';' + CHAR(13)
FROM sys.foreign_keys;

IF @sql <> '' 
    EXEC sp_executesql @sql;



SELECT 
    OBJECT_NAME(parent_object_id) AS TableName,
    name AS ForeignKeyName,
    OBJECT_NAME(referenced_object_id) AS ReferencedTableName
FROM sys.foreign_keys;
