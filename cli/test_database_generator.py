# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Test Database Generator

# This program generates dumy data for the banking system. 
# This adds 50 clients, each with 2 accounts. Each account has 40 transactions. 

from faker import Faker
from connection import add_client, add_account, add_transaction, modify_balance
import random
import datetime
import time

passwd = "Happymeal1"


def timestamp(): # Returns the current timestamp
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def generate_test_database(client_id, password):
    fake = Faker()  # Create a Faker instance

    all_account_ids = []  # List to store all account IDs

    for i in range(3):  # Generate 50 clients
        password = passwd
        name = fake.name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=90)
        address = fake.address()
        phone_number = fake.phone_number()
        email =  fake.email()
        notes = fake.text(max_nb_chars=50)

        client_response = add_client(name, birthdate, address, phone_number, email, password, notes)
        client_id = client_response['message']
        print(f"Client {client_id} added successfully. Password: {password}")
        for j in range(2):  # Each client has 2 accounts
            
            account_type = random.choice(['Spending', 'Savings'])
            account_notes = fake.text(max_nb_chars=50)
            
            account_response = add_account(client_id=client_id, description=fake.text(max_nb_chars=15), account_type=account_type, notes=account_notes)
            
            response_dict = account_response
            account_id = response_dict['message']
            print(f"Account {account_id} added successfully.")
            balance = float(1000)
            balance_response = modify_balance(account_id, balance)

            for k in range(3):  # Each account has 40 transactions
                if not all_account_ids:  # Skip creating a transaction if there are no accounts yet
                    continue

                transaction_type = random.choice(['Deposit', 'Withdrawal'])
                amount = float(random.randint(1, 200))

                if transaction_type == 'Withdrawal' and balance - amount < 0:  # Skip withdrawal if it would make balance negative
                    continue

                if transaction_type == 'Deposit':  # Update balance based on transaction type
                    balance += amount
                elif transaction_type == 'Withdrawal':
                    balance -= amount

                transaction_description = fake.text(max_nb_chars=50)
                recipient_account_id = random.choice(all_account_ids)
                
                transaction_response = add_transaction(amount=amount, account_id=account_id, recipient_account_id=recipient_account_id, otp_code=123456, description=transaction_description)
                time.sleep(0.1)

            all_account_ids.append(account_id)

    print("Test data added successfully.")
