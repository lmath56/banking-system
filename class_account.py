# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Account Class

from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from class_base import Base

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column("account_id", String, primary_key=True)
    client_id = Column(String, ForeignKey('clients.client_id'))
    description = Column("description", String)
    open_timestamp = Column("open_timestamp", String)
    account_type = Column("account_type", String)
    balance = Column("balance", Integer)
    enabled = Column("enabled", Boolean)
    notes = Column("notes", String)
    transactions = relationship("Transaction", foreign_keys='Transaction.account_id', backref="account")
                    
    def __init__(self, account_id, client_id, description, open_timestamp, account_type, balance, enabled, notes, transactions):
        """Initialises the account object."""
        self.account_id = account_id
        self.client_id = client_id
        self.description = description
        self.open_timestamp = open_timestamp
        self.account_type = account_type
        self.balance = balance
        self.enabled = enabled
        self.notes = notes
        self.transactions = transactions if transactions is not None else []
    
    def to_dict(self):
        """Returns the account as a dictionary."""
        return {
            "account_id": self.account_id,
            "client_id": self.client_id,
            "description": self.description,
            "open_timestamp": self.open_timestamp,
            "account_type": self.account_type,
            "balance": self.balance,
            "notes": self.notes
        }