import pyodbc
from app.core.config.settings import get_settings

settings = get_settings()

def create_database(tenant_id: str) -> None:
    """
    Create a new database for a tenant
    """
    # Connection string for master database
    conn_str = (
        f"DRIVER={{{settings.DB_DRIVER}}};"
        f"SERVER={settings.DB_HOST},{settings.DB_PORT};"
        f"DATABASE=master;"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASS}"
    )
    
    try:
        # Connect to master database
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # Create new database
        cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{tenant_id}')
        BEGIN
            CREATE DATABASE [{tenant_id}]
        END
        """)
        
        # Switch to new database and create schema
        cursor.execute(f"USE [{tenant_id}]")
        
        # Add your schema creation scripts here
        # Example:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
        BEGIN
            CREATE TABLE users (
                id INT PRIMARY KEY IDENTITY(1,1),
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                is_active BIT NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL DEFAULT GETUTCDATE(),
                updated_at DATETIME NOT NULL DEFAULT GETUTCDATE()
            )
        END
        """)
        
        print(f"Database '{tenant_id}' created successfully")
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Example usage
    create_database("tenant1")
