"""
Database Migration Script
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

import os
import pyodbc
from typing import List
import logging
from app.core.config.database import get_database_settings
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """Create a database connection."""
    settings = get_database_settings()
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Build connection string - using simpler format
            conn_str = (
                "Driver={SQL Server};"
                f"Server={settings.MASTER_DB_HOST};"
                f"Database={settings.MASTER_DB_NAME};"
                f"UID={settings.MASTER_DB_USER};"
                f"PWD={settings.MASTER_DB_PASS};"
                "Encrypt=yes;"
                "TrustServerCertificate=yes"
            )
            
            # Try to establish connection
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")
            conn = pyodbc.connect(conn_str, timeout=30)
            logger.info("Successfully connected to database")
            return conn
            
        except pyodbc.Error as e:
            logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

def get_migration_files(directory: str) -> List[str]:
    """Get all SQL migration files in order."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.sql'):
                files.append(os.path.join(root, filename))
    return sorted(files)

def execute_migration(conn, file_path: str):
    """Execute a single migration file."""
    logger.info(f"Executing migration: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    cursor = conn.cursor()
    
    try:
        # Split the SQL file into individual statements
        statements = [stmt.strip() for stmt in sql.split('GO') if stmt.strip()]
        
        for statement in statements:
            logger.debug(f"Executing statement: {statement[:100]}...")  # Log first 100 chars
            cursor.execute(statement)
            
        conn.commit()
        logger.info(f"Successfully executed migration: {os.path.basename(file_path)}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Error executing migration {os.path.basename(file_path)}: {str(e)}")
        logger.error(f"Failed statement: {statement}")
        raise
    finally:
        cursor.close()

def main():
    """Main migration function."""
    conn = None
    try:
        # Get database connection
        conn = get_connection()
        
        # Get migration files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        migration_dir = os.path.join(current_dir, 'v1')
        migration_files = get_migration_files(migration_dir)
        
        logger.info(f"Found {len(migration_files)} migration files")
        
        # Execute each migration file
        for file_path in migration_files:
            execute_migration(conn, file_path)
            
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == '__main__':
    main()
