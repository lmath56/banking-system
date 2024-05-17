# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Client Class

from sqlalchemy import Column, String, Boolean

from class_base import Base

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column("client_id", String, primary_key=True)
    name = Column("name", String)
    birthdate = Column("birthdate", String)
    opening_timestamp = Column("opening_timestamp", String)
    address = Column("address", String)
    phone_number = Column("phone_number", String)
    email = Column("email", String)
    hash = Column("hash", String)
    notes = Column("notes", String)
    enabled = Column("enabled", Boolean)
    administrator = Column("administrator", Boolean)
    accounts = Column("accounts", String)

    def __init__(self, client_id, name, birthdate, opening_timestamp, address, phone_number, email, hash, notes, enabled, administrator, accounts):
        self.client_id = client_id
        self.name = name
        self.birthdate = birthdate
        self.opening_timestamp = opening_timestamp
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.hash = hash
        self.notes = notes
        self.enabled = enabled
        self.administrator = administrator
        self.accounts = accounts
    
    def __repr__(self):
        return f"Client ID: {self.client_id}, Name: {self.name}, Birthdate: {self.birthdate}, Address: {self.address}, Phone Number: {self.phone_number}, Email: {self.email}, Enabled: {self.enabled}, Accounts: {self.accounts}"