from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from class_base import Base
import hashlib # hashlib for password hashing
import uuid # uuid for unique identifiers
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

def generate_uuid_short(): # Generates a short uuid
    return str(uuid.uuid4())[:8]

# Create a new engine for the test database
engine = create_engine('sqlite:///test_database.db')

# Create all tables in the test database
Base.metadata.create_all(engine)

# Create a new sessionmaker bound to the test engine
Session = sessionmaker(bind=engine)

# Create a new session
session = Session()

# Create a Faker instance
fake = Faker()

# List to store all account IDs
all_account_ids = []

# Generate 50 clients
for i in range(50):
    client_id = generate_uuid_short()
    client = Client(
        client_id=client_id,
        name=fake.name(), 
        birthdate=fake.date_of_birth(minimum_age=18, maximum_age=90), 
        opening_timestamp=fake.date_this_century(), 
        address=fake.address(), 
        phone_number=fake.phone_number(), 
        email=fake.email(), 
        administrator=random.choice([0, 1]), 
        hash=generate_hash(),  # Replace with appropriate value
        notes=fake.text(max_nb_chars=50),  # Generate fake notes
        enabled=1, 
        accounts=[])  # Empty list for accounts, you can add accounts later)
    session.add(client)

    # Each client has 2 accounts
    for j in range(2):
        account_id = generate_uuid_short()
        account = Account(
            account_id=account_id, 
            client_id=client_id, 
            description=fake.text(max_nb_chars=200),
            open_timestamp=fake.date_this_century(), 
            account_type=random.choice(['Spending', 'Savings']), 
            balance=random.randint(100, 10000), 
            enabled=1, 
            notes=fake.text(max_nb_chars=50), 
            transactions=[])
        session.add(account)
        all_account_ids.append(account_id)

        # Each account has 40 transactions
        for k in range(40):
            transaction = Transaction(
            transaction_id=generate_uuid(),  # Call the function here
            account_id=account_id,
            recipient_account_id=random.choice(all_account_ids),
            transaction_type=random.choice(['Deposit', 'Withdrawal']), 
            amount=random.randint(1, 20), 
            timestamp=fake.date_this_year(), 
            description=fake.text(max_nb_chars=50)
        )
    session.add(transaction)

# Commit the session to write the test data to the database
session.commit()

# Close the session
session.close()