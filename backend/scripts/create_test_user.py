"""Script to create a test user."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.settings import get_settings
from app.models.master.user import User
from app.core.auth.security import get_password_hash

settings = get_settings()

# Create database URL
DATABASE_URL = (
    f"mssql+pyodbc://{settings.MASTER_DB_USER}:{settings.MASTER_DB_PASS}"
    f"@{settings.MASTER_DB_HOST}:{settings.MASTER_DB_PORT}"
    f"/{settings.MASTER_DB_NAME}?"
    f"driver={settings.DB_DRIVER}"
    f"&encrypt={settings.DB_ENCRYPT}"
    f"&trustServerCertificate={settings.DB_TRUST_SERVER_CERTIFICATE}"
    f"&connection+timeout={settings.DB_CONNECTION_TIMEOUT}"
)

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_test_user():
    """Create a test user."""
    try:
        # Check if user already exists
        user = db.query(User).filter(
            User.username == "admin",
            User.tenant_id == 1
        ).first()
        
        if user:
            print("Test user already exists")
            return
        
        # Create test user
        user = User(
            username="admin",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            hashed_password=get_password_hash("admin"),
            tenant_id=1,
            is_active=True,
            is_superuser=True
        )
        
        db.add(user)
        db.commit()
        print("Test user created successfully")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
