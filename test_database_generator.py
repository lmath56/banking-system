# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Test Database Generator

# This program generates a test database for the banking system. The database contains 50 clients, each with 2 accounts. Each account has 40 transactions. 
# The first client is an administrator. The password for the administrator account is "Happymeal1". The program uses the Faker library to generate fake 
# data for the clients, accounts, and transactions. The random library is used to generate random data for the accounts and transactions. The program 
# creates a new SQLite database called test_database.db and writes the test data to the database. The client ID of the  administrator account and the 
# password for the administrator account.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from class_base import Base
import hashlib 
import uuid
from class_account import Account
from class_client import Client
from class_transaction import Transaction
from faker import Faker
import random

def generate_hash():  # Creates a hash for a password
    seed = str(random.random()).encode('utf-8')
    return hashlib.sha512(seed).hexdigest()

def generate_uuid(): # Generates a unique identifier for transactions
    return str(uuid.uuid4())

def generate_uuid_short(): # Generates a short uuid for accounts and clients
    return str(uuid.uuid4())[:8]

engine = create_engine('sqlite:///test_database.db')# Create a new engine for the test database
Base.metadata.create_all(engine) # Create all tables in the test database
Session = sessionmaker(bind=engine) # Create a new sessionmaker bound to the test engine
session = Session() # Create a new session

fake = Faker() # Create a Faker instance

all_account_ids = [] # List to store all account IDs

for i in range(50): # Generate 50 clients
    is_administrator = 1 if i == 0 else 0 # Set the first client as an administrator
    # Set the password hash for the first account so that the password is "Happymeal1"
    password_hash = "7835062ec36ed529fe22cc63baf3ec18d347dacb21c9801da8ba0848cc18efdf1e51717dd5b1240f7556aca3947aa0722452858be6002c1d46b1f1c311b0e9d8" if i == 0 else generate_hash()
    client_id = generate_uuid_short()
    all_account_ids.append(client_id)  # Add the client ID to the list of account IDs
    client = Client(
        client_id=client_id,
        name=fake.name(), 
        birthdate=fake.date_of_birth(minimum_age=18, maximum_age=90), 
        opening_timestamp=fake.date_this_century(), 
        address=fake.address(), 
        phone_number=fake.phone_number(), 
        email=fake.email(), 
        administrator=is_administrator, 
        hash=password_hash,
        notes=fake.text(max_nb_chars=50),  # Generate fake notes
        enabled=1, 
        accounts=[])  # Empty list for accounts, you can add accounts later)
    session.add(client)

    for j in range(2):# Each client has 2 accounts
        account_id = generate_uuid_short()
        balance = 1000  # Initialize balance to 1000

        for k in range(40): # Each account has 40 transactions
            if not all_account_ids: # Skip creating a transaction if there are no accounts yet
                continue

            transaction_type = random.choice(['Deposit', 'Withdrawal'])
            amount = random.randint(1, 200)

            if transaction_type == 'Withdrawal' and balance - amount < 0: # Skip withdrawal if it would make balance negative
                continue

            if transaction_type == 'Deposit': # Update balance based on transaction type
                balance += amount
            elif transaction_type == 'Withdrawal':
                balance -= amount

            transaction = Transaction(
                transaction_id=generate_uuid(),
                account_id=account_id,
                recipient_account_id=random.choice(all_account_ids),
                transaction_type=transaction_type,
                amount=amount,
                timestamp=fake.date_this_year(),
                description=fake.text(max_nb_chars=50)
            )
            session.add(transaction)

        account = Account(
            account_id=account_id,
            client_id=client_id,
            description=fake.text(max_nb_chars=200),
            open_timestamp=fake.date_this_century(),
            account_type=random.choice(['Spending', 'Savings']),
            balance=balance,  # Set balance to calculated balance
            enabled=1,
            notes=fake.text(max_nb_chars=50),
            transactions=[])
        session.add(account)
        all_account_ids.append(account_id)

session.commit() # Commit the session to write the test data to the database

print(f"The client_id of the administrator account of this test database is: {all_account_ids[0]}. The password is: Happymeal1")

session.close() # Close the session