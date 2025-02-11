from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.services.master.tenant import TenantService
from app.services.master.user import UserService
from app.services.master.role import RoleService
from app.core.security.crypto import generate_encryption_key
from app.core.db.tenant_manager import create_tenant_database
from app.schemas.master.tenant import TenantCreate
from app.schemas.master.user import UserCreate
from app.models.master.user import User


class TenantWizardService:
    def __init__(self, db: Session):
        self.db = db
        self.tenant_service = TenantService(db)
        self.user_service = UserService(db)
        self.role_service = RoleService(db)

    async def create_tenant(
        self,
        tenant_data: TenantCreate,
        admin_data: UserCreate,
        current_user: User,
        template_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wizard to create a new tenant with all necessary setup:
        1. Create tenant record
        2. Create tenant database
        3. Create admin user
        4. Setup roles and permissions
        5. Apply template if specified
        """
        try:
            # Start transaction
            self.db.begin()

            # 1. Create tenant record
            tenant = self.tenant_service.create_tenant(tenant_data, current_user)

            # 2. Create tenant database with security
            db_name = f"tenant_{tenant.tenant_id}"
            encryption_key = generate_encryption_key()
            await create_tenant_database(
                db_name=db_name,
                encryption_key=encryption_key
            )

            # 3. Create admin user
            admin_user = self.user_service.create_user(
                user_data=admin_data,
                tenant_id=tenant.tenant_id,
                is_admin=True
            )

            # 4. Setup default roles
            await self._setup_default_roles(tenant.tenant_id)

            # 5. Apply template if specified
            if template_id:
                await self._apply_template(
                    tenant_id=tenant.tenant_id,
                    template_id=template_id
                )

            # Commit transaction
            self.db.commit()

            return {
                "tenant": tenant,
                "admin_user": admin_user,
                "database": db_name
            }

        except Exception as e:
            # Rollback in case of error
            self.db.rollback()
            # Log error details
            raise Exception(f"Failed to create tenant: {str(e)}")

    async def _setup_default_roles(self, tenant_id: int) -> None:
        """Setup default roles and permissions for new tenant"""
        
        # Create default roles
        roles = [
            {
                "name": "Admin",
                "description": "Full system access",
                "permissions": [
                    "MANAGE_USERS",
                    "MANAGE_ROLES",
                    "VIEW_AUDIT_LOGS",
                    "MANAGE_SETTINGS"
                ]
            },
            {
                "name": "Manager",
                "description": "Department manager access",
                "permissions": [
                    "VIEW_REPORTS",
                    "APPROVE_TRANSACTIONS",
                    "MANAGE_TEAM"
                ]
            },
            {
                "name": "User",
                "description": "Basic user access",
                "permissions": [
                    "VIEW_OWN_DATA",
                    "CREATE_TRANSACTIONS",
                    "VIEW_BASIC_REPORTS"
                ]
            }
        ]

        for role_data in roles:
            role = await self.role_service.create_role(
                name=role_data["name"],
                description=role_data["description"],
                tenant_id=tenant_id
            )
            
            # Assign permissions
            for permission in role_data["permissions"]:
                await self.role_service.assign_permission(
                    role_id=role.role_id,
                    permission_code=permission
                )

    async def _apply_template(self, tenant_id: int, template_id: int) -> None:
        """Apply template configuration to new tenant"""
        # TODO: Implement template system
        pass

    async def validate_tenant_name(self, name: str) -> bool:
        """Check if tenant name is available"""
        existing = self.tenant_service.get_tenant_by_name(name)
        return existing is None

    async def get_available_templates(self) -> list:
        """Get list of available templates"""
        # TODO: Implement template listing
        return []
