"""Script para inicializar o banco de dados."""
import pyodbc
import logging
from app.core.config.settings import get_settings
from app.core.auth.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

def init_db():
    """Inicializa o banco de dados."""
    try:
        # Build connection string
        conn_str = (
            "Driver={SQL Server};"
            f"Server={settings.MASTER_DB_HOST};"
            f"Database={settings.MASTER_DB_NAME};"
            f"UID={settings.MASTER_DB_USER};"
            f"PWD={settings.MASTER_DB_PASS};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes"
        )
        
        # Connect to database
        logger.info("Conectando ao banco de dados...")
        conn = pyodbc.connect(conn_str, timeout=30)
        cursor = conn.cursor()
        
        # Create tables
        logger.info("Criando tabelas...")
        
        # Drop tables if they exist (for testing)
        logger.info("Removendo tabelas existentes...")
        
        # Drop foreign keys first
        cursor.execute("""
        DECLARE @sql NVARCHAR(MAX) = N'';
        
        SELECT @sql += N'
        ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
            + '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) + 
            ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
        FROM sys.foreign_keys
        WHERE referenced_object_id IN (
            SELECT object_id 
            FROM sys.tables 
            WHERE name IN ('user_roles', 'users', 'roles', 'tenants')
        );
        
        EXEC sp_executesql @sql;
        """)
        conn.commit()
        
        # Now drop the tables
        tables = ['user_roles', 'users', 'roles', 'tenants']
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            conn.commit()
        
        # Create tenants table
        logger.info("Criando tabela tenants...")
        cursor.execute("""
        CREATE TABLE tenants (
            tenant_id INT PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            domain NVARCHAR(100) NOT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NOT NULL DEFAULT GETDATE()
        )
        """)
        conn.commit()
        
        # Insert default tenant
        logger.info("Inserindo tenant padrão...")
        cursor.execute("""
        INSERT INTO tenants (tenant_id, name, domain, is_active)
        VALUES (1, 'Master', 'master', 1)
        """)
        conn.commit()
        
        # Create users table
        logger.info("Criando tabela users...")
        cursor.execute("""
        CREATE TABLE users (
            user_id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) NOT NULL,
            email NVARCHAR(255) NOT NULL,
            password_hash NVARCHAR(255) NOT NULL,
            first_name NVARCHAR(100) NOT NULL,
            last_name NVARCHAR(100) NOT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            is_superuser BIT NOT NULL DEFAULT 0,
            tenant_id INT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NOT NULL DEFAULT GETDATE(),
            last_login DATETIME,
            FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
        )
        """)
        conn.commit()
        
        # Create roles table
        logger.info("Criando tabela roles...")
        cursor.execute("""
        CREATE TABLE roles (
            role_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            description NVARCHAR(255),
            tenant_id INT NOT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NOT NULL DEFAULT GETDATE(),
            FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
        )
        """)
        conn.commit()
        
        # Create user_roles table
        logger.info("Criando tabela user_roles...")
        cursor.execute("""
        CREATE TABLE user_roles (
            user_id INT NOT NULL,
            role_id INT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
        """)
        conn.commit()
        
        # Insert admin user
        logger.info("Inserindo usuário admin...")
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, first_name, last_name, is_superuser, tenant_id, is_active)
        VALUES (?, ?, ?, ?, ?, 1, 1, 1)
        """, ('admin', 'admin@example.com', get_password_hash('admin'), 'Admin', 'User'))
        conn.commit()
        
        # Insert admin role
        logger.info("Inserindo role admin...")
        cursor.execute("""
        INSERT INTO roles (name, description, tenant_id, is_active)
        VALUES ('admin', 'Administrator role', 1, 1)
        """)
        conn.commit()
        
        # Assign admin role to admin user
        logger.info("Atribuindo role admin ao usuário admin...")
        cursor.execute("""
        INSERT INTO user_roles (user_id, role_id)
        SELECT u.user_id, r.role_id
        FROM users u
        CROSS JOIN roles r
        WHERE u.username = 'admin' AND r.name = 'admin'
        """)
        conn.commit()
        
        logger.info("Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()
