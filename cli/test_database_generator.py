# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Test Database Generator

# This program generates a test database for the banking system. The database contains 50 clients, each with 2 accounts. Each account has 40 transactions. 
# The first client is an administrator. The password for the administrator account is "Happymeal1". The program uses the Faker library to generate fake 
# data for the clients, accounts, and transactions. The random library is used to generate random data for the accounts and transactions. The program 
# creates a new SQLite database called test_database.db and writes the test data to the database. The client ID of the  administrator account and the 
# password for the administrator account.

ADMIN_EMAIL = "lmath56@hotmail.com" # Email address of the administrator account


from faker import Faker
import class_account
import class_client
import class_transaction
from connection import login, add_client, add_account, add_transaction, logout
import argparse
import random
import datetime
import hashlib 
import uuid

def generate_hash():  # Creates a hash for a password
    seed = str(random.random()).encode('utf-8')
    return hashlib.sha512(seed).hexdigest()

def generate_uuid(): # Generates a unique identifier for transactions
    return str(uuid.uuid4())

def generate_uuid_short(): # Generates a short uuid for accounts and clients
    return str(uuid.uuid4())[:8]

def timestamp(): # Returns the current timestamp
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

fake = Faker()  # Create a Faker instance

all_account_ids = []  # List to store all account IDs

# Set up argument parsing
parser = argparse.ArgumentParser(description="Generate test database for the banking system.")
parser.add_argument('-u', '--username', required=True, help="Username for admin login")
parser.add_argument('-p', '--password', required=True, help="Password for admin login")

args = parser.parse_args()

# Log in as the admin using provided username and password
client_id = args.username
client_hash = hashlib.sha512(args.password.encode()).hexdigest()
client = login(client_id, client_hash)

if client is not None:  # Check if login was successful
    print("Admin logged in successfully")

    for i in range(50):  # Generate 50 clients
        is_administrator = 1 if i == 0 else 0  # Set the first client as an administrator
        # Set the password hash for the first account so that the password is "Happymeal1"
        password = "Happymeal1" if i == 0 else generate_hash()
        client_id = generate_uuid_short()
        client_name = "ADMIN" if i == 0 else fake.name()
        birthdate = "ADMIN" if i == 0 else fake.date_of_birth(minimum_age=18, maximum_age=90)
        opening_timestamp = timestamp() if i == 0 else fake.date_this_century()
        address = "ADMIN" if i == 0 else fake.address()
        phone_number = "ADMIN" if i == 0 else fake.phone_number()
        email = ADMIN_EMAIL if i == 0 else fake.email()
        notes = fake.text(max_nb_chars=50)

        # Add client using add_client function
        client_response = add_client(
            name=client_name,
            birthdate=birthdate,
            address=address,
            phone_number=phone_number,
            email=email,
            password=password,
            notes=notes
        )
        print(client_response[1])  # Print the response message

        for j in range(2):  # Each client has 2 accounts
            account_id = generate_uuid_short()
            balance = 1000  # Initialize balance to 1000
            account_type = random.choice(['Spending', 'Savings'])
            account_notes = fake.text(max_nb_chars=50)

            # Add account using add_account function
            account_response = add_account(
                client_id=client_id,
                description=fake.text(max_nb_chars=200),
                account_type=account_type,
                notes=account_notes
            )
            print(account_response[1])  # Print the response message

            for k in range(40):  # Each account has 40 transactions
                if not all_account_ids:  # Skip creating a transaction if there are no accounts yet
                    continue

                transaction_type = random.choice(['Deposit', 'Withdrawal'])
                amount = random.randint(1, 200)

                if transaction_type == 'Withdrawal' and balance - amount < 0:  # Skip withdrawal if it would make balance negative
                    continue

                if transaction_type == 'Deposit':  # Update balance based on transaction type
                    balance += amount
                elif transaction_type == 'Withdrawal':
                    balance -= amount

                transaction_description = fake.text(max_nb_chars=50)
                recipient_account_id = random.choice(all_account_ids)

                # Add transaction using add_transaction function
                transaction_response = add_transaction(
                    amount=amount,
                    account_id=account_id,
                    recipient_account_id=recipient_account_id,
                    otp_code=123456,  # Replace with actual OTP verification code
                    description=transaction_description
                )
                print(transaction_response[1])  # Print the response message

            all_account_ids.append(account_id)
    logout()  # Log out of the admin account
    print(f"The client_id of the administrator account of this test database is: {all_account_ids[0]}. The password is: Happymeal1")
else:
    print("Admin login failed.")