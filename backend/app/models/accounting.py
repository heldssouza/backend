from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class ChartOfAccounts(BaseModel):
    __tablename__ = "chart_of_accounts"
    
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    parent_id = Column(Integer, ForeignKey('chart_of_accounts.id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Self-referential relationship
    children = relationship("ChartOfAccounts", 
                          backref="parent",
                          remote_side=[id])
    
    # Indexes
    __table_args__ = (
        Index('idx_coa_code', 'code'),
        Index('idx_coa_parent', 'parent_id'),
    )

class FiscalYear(BaseModel):
    __tablename__ = "fiscal_years"
    
    year = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime)
    closed_by = Column(Integer, ForeignKey('users.id'))
    
    __table_args__ = (
        Index('idx_fiscal_year', 'year', unique=True),
    )

class JournalEntry(BaseModel):
    __tablename__ = "journal_entries"
    
    entry_date = Column(DateTime, nullable=False)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    reference_number = Column(String(50), nullable=False, unique=True)
    description = Column(String(500))
    status = Column(String(20), nullable=False)  # Draft, Posted, Voided
    posted_at = Column(DateTime)
    posted_by = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    fiscal_year = relationship("FiscalYear")
    details = relationship("JournalEntryDetail", back_populates="journal_entry")
    
    __table_args__ = (
        Index('idx_je_fiscal_year', 'fiscal_year_id'),
        Index('idx_je_reference', 'reference_number'),
        Index('idx_je_date', 'entry_date'),
    )

class JournalEntryDetail(BaseModel):
    __tablename__ = "journal_entry_details"
    
    journal_entry_id = Column(Integer, ForeignKey('journal_entries.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('chart_of_accounts.id'), nullable=False)
    debit_amount = Column(Numeric(20, 2), default=0)
    credit_amount = Column(Numeric(20, 2), default=0)
    description = Column(String(500))
    
    # Relationships
    journal_entry = relationship("JournalEntry", back_populates="details")
    account = relationship("ChartOfAccounts")
    
    __table_args__ = (
        Index('idx_jed_journal_entry', 'journal_entry_id'),
        Index('idx_jed_account', 'account_id'),
    )

class AccountBalance(BaseModel):
    __tablename__ = "account_balances"
    
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('chart_of_accounts.id'), nullable=False)
    period = Column(Integer, nullable=False)  # 1-12 for months
    debit_balance = Column(Numeric(20, 2), default=0)
    credit_balance = Column(Numeric(20, 2), default=0)
    
    # Relationships
    fiscal_year = relationship("FiscalYear")
    account = relationship("ChartOfAccounts")
    
    __table_args__ = (
        Index('idx_ab_fiscal_year_account', 'fiscal_year_id', 'account_id', 'period', unique=True),
    )
