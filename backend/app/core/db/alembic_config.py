"""Alembic configuration utilities."""
from typing import List
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.core.config.database import get_database_settings
from app.core.db.base import Base
from app.models.master.base_model import BaseModel
from app.models.master.user import User  # Import all models here

# List of all models
models: List[type] = [
    User,
    # Add other models here as they are created
]

def get_url() -> str:
    """Get database URL based on environment."""
    settings = get_database_settings()
    return settings.MASTER_DATABASE_URL

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = context.config
    configuration.set_main_option("sqlalchemy.url", get_url())
    
    connectable = engine_from_config(
        configuration.get_section(configuration.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=get_url(),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()
