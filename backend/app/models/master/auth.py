"""Authentication models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.db.base import Base
from app.models.master.user import User


class RefreshToken(Base):
    """Refresh token model."""

    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("dbo.Users.UserID", ondelete="CASCADE"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens"
    )

    def __repr__(self):
        return f"<RefreshToken {self.token}>"


class TwoFactorAuth(Base):
    """Two-factor authentication model."""
    __tablename__ = "TwoFactorAuth"
    __table_args__ = {"schema": "dbo"}

    TwoFactorAuthID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("dbo.Users.UserID"), unique=True, nullable=False)
    SecretKey = Column(String(32), nullable=False)
    IsEnabled = Column(Boolean, server_default='0', nullable=False)
    CreatedAt = Column(DateTime, server_default=text('GETDATE()'), nullable=False)
    UpdatedAt = Column(DateTime, server_default=text('GETDATE()'), nullable=False)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="two_factor_auth")
