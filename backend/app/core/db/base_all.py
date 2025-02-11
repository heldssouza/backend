"""Import all models for Alembic."""
from app.core.db.base import Base
from app.models.master.user import User

# Import all models here
__all__ = [
    "Base",
    "User",
]
