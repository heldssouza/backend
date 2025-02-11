from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.core.db.tenant_manager import TenantDatabaseManager
import json
import logging

logger = logging.getLogger(__name__)


class TenantTemplate:
    """Base class for tenant templates"""
    
    name: str = ""
    description: str = ""
    
    async def apply(
        self,
        tenant_id: int,
        db: Session,
        config: Dict[str, Any] = None
    ) -> bool:
        """
        Apply template to tenant database
        
        Args:
            tenant_id: Tenant ID
            db: Master database session
            config: Optional template configuration
        
        Returns:
            bool: True if template was applied successfully
        """
        raise NotImplementedError


class FinancialTemplate(TenantTemplate):
    """Template for financial system setup"""
    
    name = "Financial System"
    description = "Complete financial system setup with chart of accounts"
    
    async def apply(
        self,
        tenant_id: int,
        db: Session,
        config: Dict[str, Any] = None
    ) -> bool:
        try:
            async with TenantDatabaseManager(tenant_id) as tenant_db:
                # Create schemas
                await self._create_schemas(tenant_db)
                
                # Create tables
                await self._create_tables(tenant_db)
                
                # Load initial data
                await self._load_initial_data(tenant_db, config)
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to apply template: {str(e)}")
            return False
    
    async def _create_schemas(self, db: Session):
        """Create database schemas"""
        db.execute("""
            CREATE SCHEMA IF NOT EXISTS accounting;
            CREATE SCHEMA IF NOT EXISTS financial;
            CREATE SCHEMA IF NOT EXISTS reports;
        """)
    
    async def _create_tables(self, db: Session):
        """Create database tables"""
        # Chart of Accounts
        db.execute("""
            CREATE TABLE accounting.accounts (
                account_id SERIAL PRIMARY KEY,
                code VARCHAR(20) NOT NULL,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20) NOT NULL,
                parent_id INTEGER REFERENCES accounting.accounts(account_id),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(code)
            );
            
            CREATE TABLE accounting.transactions (
                transaction_id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                type VARCHAR(20) NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'draft',
                created_by INTEGER NOT NULL,
                approved_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE accounting.entries (
                entry_id SERIAL PRIMARY KEY,
                transaction_id INTEGER REFERENCES accounting.transactions(transaction_id),
                account_id INTEGER REFERENCES accounting.accounts(account_id),
                debit DECIMAL(15,2) DEFAULT 0,
                credit DECIMAL(15,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Financial
        db.execute("""
            CREATE TABLE financial.cost_centers (
                cost_center_id SERIAL PRIMARY KEY,
                code VARCHAR(20) NOT NULL,
                name VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(code)
            );
            
            CREATE TABLE financial.budgets (
                budget_id SERIAL PRIMARY KEY,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                account_id INTEGER REFERENCES accounting.accounts(account_id),
                cost_center_id INTEGER REFERENCES financial.cost_centers(cost_center_id),
                amount DECIMAL(15,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    
    async def _load_initial_data(
        self,
        db: Session,
        config: Dict[str, Any] = None
    ):
        """Load initial data"""
        # Load chart of accounts
        accounts_data = self._get_default_accounts()
        for account in accounts_data:
            db.execute(
                """
                INSERT INTO accounting.accounts (code, name, type)
                VALUES (:code, :name, :type)
                """,
                account
            )
        
        # Load cost centers
        if config and "cost_centers" in config:
            for cc in config["cost_centers"]:
                db.execute(
                    """
                    INSERT INTO financial.cost_centers (code, name)
                    VALUES (:code, :name)
                    """,
                    cc
                )
    
    def _get_default_accounts(self) -> List[Dict[str, str]]:
        """Get default chart of accounts"""
        return [
            {"code": "1", "name": "Assets", "type": "asset"},
            {"code": "1.1", "name": "Current Assets", "type": "asset"},
            {"code": "1.2", "name": "Fixed Assets", "type": "asset"},
            {"code": "2", "name": "Liabilities", "type": "liability"},
            {"code": "2.1", "name": "Current Liabilities", "type": "liability"},
            {"code": "2.2", "name": "Long Term Liabilities", "type": "liability"},
            {"code": "3", "name": "Equity", "type": "equity"},
            {"code": "4", "name": "Revenue", "type": "revenue"},
            {"code": "5", "name": "Expenses", "type": "expense"},
        ]


class HRTemplate(TenantTemplate):
    """Template for HR system setup"""
    
    name = "HR System"
    description = "Human Resources management system setup"
    
    async def apply(
        self,
        tenant_id: int,
        db: Session,
        config: Dict[str, Any] = None
    ) -> bool:
        # TODO: Implement HR template
        pass


# Registry of available templates
TEMPLATES = {
    "financial": FinancialTemplate(),
    "hr": HRTemplate()
}


def get_available_templates() -> List[Dict[str, str]]:
    """Get list of available templates"""
    return [
        {
            "id": template_id,
            "name": template.name,
            "description": template.description
        }
        for template_id, template in TEMPLATES.items()
    ]


async def apply_template(
    template_id: str,
    tenant_id: int,
    db: Session,
    config: Dict[str, Any] = None
) -> bool:
    """
    Apply template to tenant
    
    Args:
        template_id: Template identifier
        tenant_id: Tenant ID
        db: Database session
        config: Optional template configuration
    
    Returns:
        bool: True if template was applied successfully
    """
    if template_id not in TEMPLATES:
        raise ValueError(f"Template {template_id} not found")
    
    template = TEMPLATES[template_id]
    return await template.apply(tenant_id, db, config)
