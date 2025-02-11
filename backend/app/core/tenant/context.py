from contextvars import ContextVar
from typing import Optional

class TenantContext:
    _tenant_id: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)
    
    @classmethod
    def get_tenant_id(cls) -> Optional[str]:
        return cls._tenant_id.get()
    
    @classmethod
    def set_tenant_id(cls, tenant_id: str) -> None:
        cls._tenant_id.set(tenant_id)
    
    @classmethod
    def clear(cls) -> None:
        cls._tenant_id.set(None)
