"""Seed test data."""
from sqlalchemy.orm import Session
from app.core.db.session import SessionLocal
from app.models.master import Tenant, Role, User, Permission
from app.core.security.auth import get_password_hash
from app.core.security.permission_constants import PERMISSIONS


def seed_test_data():
    """Seed test data."""
    db = SessionLocal()
    try:
        # Create test tenant
        tenant = Tenant()
        tenant.Name = "Test Tenant"
        tenant.Domain = "test.com"
        tenant.IsActive = True
        db.add(tenant)
        db.flush()

        # Create permissions
        permissions = {}
        for perm_data in PERMISSIONS:
            permission = Permission()
            permission.Name = perm_data["name"]
            permission.Code = perm_data["code"]
            permission.Description = perm_data["description"]
            db.add(permission)
            permissions[permission.Code] = permission
        db.flush()

        # Create admin role with all permissions
        admin_role = Role()
        admin_role.Name = "Admin"
        admin_role.Description = "Administrator role"
        admin_role.IsActive = True
        admin_role.TenantID = tenant.TenantID
        admin_role.Permissions.extend(permissions.values())
        db.add(admin_role)

        # Create user role with basic permissions
        user_role = Role()
        user_role.Name = "User"
        user_role.Description = "Basic user role"
        user_role.IsActive = True
        user_role.TenantID = tenant.TenantID
        basic_permissions = [
            permissions["read_user"],
            permissions["read_role"],
            permissions["read_tenant"]
        ]
        user_role.Permissions.extend(basic_permissions)
        db.add(user_role)
        db.flush()

        # Create test admin user
        admin_user = User()
        admin_user.Email = "admin@test.com"
        admin_user.HashedPassword = get_password_hash("admin123")
        admin_user.FirstName = "Admin"
        admin_user.LastName = "User"
        admin_user.IsActive = True
        admin_user.IsSuperuser = True
        admin_user.TenantID = tenant.TenantID
        admin_user.Roles.append(admin_role)
        db.add(admin_user)

        # Create test regular user
        regular_user = User()
        regular_user.Email = "user@test.com"
        regular_user.HashedPassword = get_password_hash("user123")
        regular_user.FirstName = "Regular"
        regular_user.LastName = "User"
        regular_user.IsActive = True
        regular_user.IsSuperuser = False
        regular_user.TenantID = tenant.TenantID
        regular_user.Roles.append(user_role)
        db.add(regular_user)

        db.commit()
        print("Test data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding test data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_test_data()
