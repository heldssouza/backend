"""SQLAlchemy base class."""
from typing import Any
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr
from sqlalchemy.schema import MetaData

# Define naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create metadata with naming convention
metadata = MetaData(naming_convention=convention, schema="dbo")

@as_declarative(metadata=metadata)
class Base:
    """Base class for all database models."""
    
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
