from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean, Index, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Account(BaseModel):
    __tablename__ = "accounts"
    
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Self-referential relationship
    children = relationship("Account",
                          backref="parent",
                          remote_side=[id])
    
    # Relationship with FSAccount
    fs_account_id = Column(Integer, ForeignKey('fs_accounts.id'), nullable=False)
    fs_account = relationship("FSAccount", back_populates="accounts")
    
    __table_args__ = (
        Index('idx_account_code', 'code'),
        Index('idx_account_parent', 'parent_id'),
        Index('idx_account_fs', 'fs_account_id'),
    )

class FSAccount(BaseModel):
    __tablename__ = "fs_accounts"
    
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    statement_type = Column(String(50), nullable=False)  # BS (Balance Sheet) or IS (Income Statement)
    category = Column(String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    subcategory = Column(String(50))
    sign = Column(Integer, nullable=False)  # 1 for debit, -1 for credit
    sequence = Column(Integer, nullable=False)  # For reporting order
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationship with Account
    accounts = relationship("Account", back_populates="fs_account")
    
    __table_args__ = (
        CheckConstraint('sign IN (1, -1)', name='check_sign_values'),
        Index('idx_fs_account_code', 'code'),
        Index('idx_fs_account_type', 'statement_type', 'category'),
        Index('idx_fs_account_sequence', 'sequence'),
    )

class AccountBalance(BaseModel):
    __tablename__ = "account_balances"
    
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    period = Column(String(7), nullable=False)  # Format: YYYY-MM
    initial_balance = Column(Numeric(20, 2), default=0)
    debit_amount = Column(Numeric(20, 2), default=0)
    credit_amount = Column(Numeric(20, 2), default=0)
    final_balance = Column(Numeric(20, 2), default=0)
    
    # Relationships
    account = relationship("Account")
    
    __table_args__ = (
        CheckConstraint("period ~ '^[0-9]{4}-(?:0[1-9]|1[0-2])$'", name='check_period_format'),
        Index('idx_balance_account_period', 'account_id', 'period', unique=True),
    )

class FSAccountBalance(BaseModel):
    __tablename__ = "fs_account_balances"
    
    fs_account_id = Column(Integer, ForeignKey('fs_accounts.id'), nullable=False)
    period = Column(String(7), nullable=False)  # Format: YYYY-MM
    initial_balance = Column(Numeric(20, 2), default=0)
    movement = Column(Numeric(20, 2), default=0)  # Net movement for the period
    final_balance = Column(Numeric(20, 2), default=0)
    
    # Relationships
    fs_account = relationship("FSAccount")
    
    __table_args__ = (
        CheckConstraint("period ~ '^[0-9]{4}-(?:0[1-9]|1[0-2])$'", name='check_period_format'),
        Index('idx_fs_balance_account_period', 'fs_account_id', 'period', unique=True),
    )
