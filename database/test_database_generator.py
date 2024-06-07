# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Test Database Generator

ADMIN_EMAIL = "lmath56@hotmail.com"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.class_base import Base
from class_account import Account
from class_client import Client
from class_transaction import Transaction
from faker import Faker
import random
import datetime
import hashlib
import uuid
from datetime import datetime, timedelta


def generate_hash():
    seed = str(random.random()).encode('utf-8')
    return hashlib.sha512(seed).hexdigest()

def generate_uuid():
    return str(uuid.uuid4())

def generate_uuid_short():
    return str(uuid.uuid4())[:8]

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def timestamp_this_year():
    start = datetime(datetime.now().year, 1, 1)
    end = datetime(datetime.now().year, 12, 31, 23, 59, 59)
    return random_date(start, end).strftime("%Y-%m-%d %H:%M:%S")

def timestamp_this_century():
    start = datetime(2000, 1, 1)
    end = datetime(2099, 12, 31, 23, 59, 59)
    return random_date(start, end).strftime("%Y-%m-%d %H:%M:%S")


engine = create_engine('sqlite:///bank.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()
all_account_ids = []

for i in range(50):
    is_administrator = 1 if i == 0 else 0
    password_hash = "7835062ec36ed529fe22cc63baf3ec18d347dacb21c9801da8ba0848cc18efdf1e51717dd5b1240f7556aca3947aa0722452858be6002c1d46b1f1c311b0e9d8" if i == 0 else generate_hash()
    client_id = generate_uuid_short()
    client = Client(
        client_id=client_id,
        name="ADMIN" if i == 0 else fake.name(),
        birthdate="ADMIN" if i == 0 else timestamp_this_century(),
        opening_timestamp=current_timestamp() if i == 0 else timestamp_this_century(),
        address="ADMIN" if i == 0 else fake.address(),
        phone_number="ADMIN" if i == 0 else fake.phone_number(),
        email=ADMIN_EMAIL if i == 0 else fake.email(),
        administrator=is_administrator,
        hash=password_hash,
        notes=fake.text(max_nb_chars=50),
        enabled=1,
        accounts=[]
    )
    session.add(client)

    for j in range(2):
        account_id = generate_uuid_short()
        balance = 1000

        for k in range(40):
            transaction_type = random.choice(['Deposit', 'Withdrawal'])
            amount = random.randint(1, 200)

            if transaction_type == 'Withdrawal' and balance - amount < 0:
                continue

            if transaction_type == 'Deposit':
                balance += amount
            else:
                balance -= amount

            transaction = Transaction(
                transaction_id=generate_uuid(),
                account_id=account_id,
                recipient_account_id=random.choice(all_account_ids) if all_account_ids else account_id,
                transaction_type=transaction_type,
                amount=amount,
                timestamp=timestamp_this_year(),
                description=fake.text(max_nb_chars=20)
            )
            session.add(transaction)

        account = Account(
            account_id=account_id,
            client_id=client_id,
            description=fake.text(max_nb_chars=20),
            open_timestamp=timestamp_this_year(),
            account_type=random.choice(['Spending', 'Savings']),
            balance=balance,
            enabled=1,
            notes=fake.text(max_nb_chars=50),
            transactions=[]
        )
        session.add(account)
        all_account_ids.append(account_id)

session.commit()

# Retrieve the client_id of the administrator account from the session
admin_client_id = session.query(Client.client_id).filter(Client.administrator == 1).first()[0]

# Print the client_id of the administrator account
print(f"The client_id of the administrator account of this test database is: {admin_client_id}")
print("The password is: Happymeal1")

session.close()