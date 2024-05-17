# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Transaction Class

from sqlalchemy import Column, String, Integer, ForeignKey

from class_base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column("transaction_id", String, primary_key=True)
    transaction_type = Column("transaction_type", String)
    amount = Column("amount", Integer)
    timestamp = Column("timestamp", String)
    description = Column("description", String)
    account_id = Column(String, ForeignKey('accounts.account_id'))
    recipient_account_number = Column("recipient_account_number", Integer)

    def __init__(self, transaction_id, transaction_type, amount, timestamp, description, account_number, recipient_account_number = None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp
        self.description = description
        self.account_number = account_number
        self.recipient_account_number = recipient_account_number

    def __repr__(self):
        return f"Transaction ID: {self.transaction_id}, Transaction Type: {self.transaction_type}, Amount: {self.amount}, Timestamp: {self.timestamp}, Description: {self.description} From Account Number: {self.account_number}, Recipient Account Number: {self.recipient_account_number}"