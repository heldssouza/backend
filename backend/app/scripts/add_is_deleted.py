from app.core.config.database import get_database_settings
from sqlalchemy import create_engine, text

def add_is_deleted_column():
    settings = get_database_settings()
    engine = create_engine(settings.MASTER_DATABASE_URL)
    
    with engine.connect() as conn:
        sql = """
        IF NOT EXISTS (
            SELECT * FROM sys.columns 
            WHERE object_id = OBJECT_ID(N'dbo.Users') 
            AND name = 'IsDeleted'
        )
        BEGIN
            ALTER TABLE dbo.Users
            ADD IsDeleted bit NOT NULL DEFAULT 0
        END
        """
        conn.execute(text(sql))
        conn.commit()
        print('Coluna IsDeleted adicionada com sucesso!')

if __name__ == '__main__':
    add_is_deleted_column()
