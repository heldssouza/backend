"""Base model with common fields and SQL Server conventions."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base import Base


class BaseModel(Base):
    """Base model with common SQL Server conventions."""
    __abstract__ = True

    CreatedAt: Mapped[datetime] = mapped_column(
        DATETIME2,
        server_default=text('GETDATE()'),
        nullable=False
    )
    CreatedBy: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('dbo.Users.UserID'),
        nullable=True  # Nullable for initial system records
    )
    UpdatedAt: Mapped[datetime] = mapped_column(
        DATETIME2,
        server_default=text('GETDATE()'),
        onupdate=text('GETDATE()'),
        nullable=False
    )
    UpdatedBy: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('dbo.Users.UserID'),
        nullable=True
    )
    IsDeleted: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('0'),
        nullable=False,
        index=True
    )

    __table_args__ = {
        'schema': 'dbo'
    }
