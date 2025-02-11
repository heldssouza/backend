"""Create database tables."""
from app.core.db.base import Base
from app.core.db.session import engine
from app.models.master import Tenant, User, Role, Permission, UserRoles, RolePermissions


def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    create_tables()
