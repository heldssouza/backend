from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.dependencies import get_current_admin_user
from app.services.master.tenant_wizard import TenantWizardService
from app.schemas.master.tenant import TenantCreate
from app.schemas.master.user import UserCreate
from app.models.master.user import User

router = APIRouter()


@router.post("/wizard/validate-name")
async def validate_tenant_name(
    name: str,
    db: Session = Depends(get_db)
):
    """
    Validate if tenant name is available
    """
    wizard = TenantWizardService(db)
    is_valid = await wizard.validate_tenant_name(name)
    return {"valid": is_valid}


@router.get("/wizard/templates")
async def list_templates(
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    """
    List available tenant templates.
    Requires admin access.
    """
    wizard = TenantWizardService(db)
    templates = await wizard.get_available_templates()
    return templates


@router.post("/wizard/create", response_model=Dict[str, Any])
async def create_tenant(
    tenant_data: TenantCreate,
    admin_data: UserCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db),
    template_id: int = None
):
    """
    Create new tenant with complete setup:
    - Tenant record
    - Admin user
    - Basic roles and permissions
    - Template data (if template_id provided)
    
    Requires admin access.
    """
    wizard = TenantWizardService(db)
    
    # Validate tenant name
    if not await wizard.validate_tenant_name(tenant_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant name is not available"
        )
    
    # Create tenant with complete setup
    result = await wizard.create_tenant_complete(
        tenant_data=tenant_data,
        admin_data=admin_data,
        template_id=template_id
    )
    
    return result
