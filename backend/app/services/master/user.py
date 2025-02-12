from typing import Optional
from sqlalchemy.orm import Session
from app.models.master.user import User
from app.core.security import get_password_hash, verify_password
from app.schemas.master.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.Email == email).first()

    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            Email=user_data.email,
            Username=user_data.username,
            HashedPassword=hashed_password,
            IsActive=user_data.is_active,
            IsSuperuser=user_data.is_superuser,
            TenantID=user_data.tenant_id,
            FirstName=user_data.first_name,
            LastName=user_data.last_name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["HashedPassword"] = get_password_hash(update_data.pop("password"))
        
        # Map schema fields to model fields
        field_mapping = {
            "email": "Email",
            "username": "Username",
            "is_active": "IsActive",
            "first_name": "FirstName",
            "last_name": "LastName"
        }
        
        for field, value in update_data.items():
            model_field = field_mapping.get(field, field)
            setattr(user, model_field, value)
            
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.HashedPassword):
            return None
        return user


# Create a singleton instance
user_service = UserService(None)  # Will be initialized with DB session later
