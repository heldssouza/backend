from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    __tablename__ = "transactions"
    
    period = Column(String(7), nullable=False)  # Format: YYYY-MM
    transaction_date = Column(DateTime, nullable=False)
    reference_number = Column(String(50), nullable=False, unique=True)
    description = Column(String(500))
    status = Column(String(20), nullable=False)  # Draft, Posted, Voided
    posted_at = Column(DateTime)
    posted_by = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    details = relationship("TransactionDetail", back_populates="transaction")
    
    __table_args__ = (
        CheckConstraint("period ~ '^[0-9]{4}-(?:0[1-9]|1[0-2])$'", name='check_period_format'),
        CheckConstraint("status IN ('Draft', 'Posted', 'Voided')", name='check_status_values'),
        Index('idx_transaction_period', 'period'),
        Index('idx_transaction_date', 'transaction_date'),
        Index('idx_transaction_reference', 'reference_number'),
        Index('idx_transaction_status', 'status'),
    )

class TransactionDetail(BaseModel):
    __tablename__ = "transaction_details"
    
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    debit_amount = Column(Numeric(20, 2), default=0)
    credit_amount = Column(Numeric(20, 2), default=0)
    description = Column(String(500))
    
    # Relationships
    transaction = relationship("Transaction", back_populates="details")
    account = relationship("Account")
    
    __table_args__ = (
        CheckConstraint(
            '(debit_amount > 0 AND credit_amount = 0) OR (credit_amount > 0 AND debit_amount = 0)',
            name='check_amount_values'
        ),
        Index('idx_transaction_detail_transaction', 'transaction_id'),
        Index('idx_transaction_detail_account', 'account_id'),
    )

class PeriodStatus(BaseModel):
    __tablename__ = "period_status"
    
    period = Column(String(7), nullable=False, unique=True)  # Format: YYYY-MM
    status = Column(String(20), nullable=False)  # Open, Closed, Locked
    closed_at = Column(DateTime)
    closed_by = Column(Integer, ForeignKey('users.id'))
    locked_at = Column(DateTime)
    locked_by = Column(Integer, ForeignKey('users.id'))
    
    __table_args__ = (
        CheckConstraint("period ~ '^[0-9]{4}-(?:0[1-9]|1[0-2])$'", name='check_period_format'),
        CheckConstraint("status IN ('Open', 'Closed', 'Locked')", name='check_status_values'),
        Index('idx_period_status', 'period', 'status'),
    )
