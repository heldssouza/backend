from contextvars import ContextVar
from uuid import UUID
from typing import Optional

class TenantContext:
    """
    Thread-safe context manager for tenant information.
    Uses contextvars to ensure isolation between requests.
    """
    _tenant_id: ContextVar[Optional[UUID]] = ContextVar("tenant_id", default=None)

    @classmethod
    def get_tenant_id(cls) -> Optional[UUID]:
        """Get the current tenant ID."""
        return cls._tenant_id.get()

    @classmethod
    def set_tenant_id(cls, tenant_id: UUID) -> None:
        """Set the current tenant ID."""
        cls._tenant_id.set(tenant_id)

    @classmethod
    def clear(cls) -> None:
        """Clear the current tenant context."""
        cls._tenant_id.set(None)
