# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

from class_client import Client
from class_account import Account
from class_transaction import Transaction
from flask import jsonify
import hashlib # hashlib for password hashing
import datetime # datetime for timestamps
import uuid # uuid for unique identifiers


from database import * # Importing the database connection

##############
### System ###
##############

def timestamp(): # Returns the current timestamp
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def password_hash(password:str): # Converts a string to SHA512 hash
    return hashlib.sha512(password.encode()).hexdigest()

def generate_uuid(): # Generates a unique identifier for transactions
    return str(uuid.uuid4())

def generate_uuid_short(): # Generates a short uuid
    return str(uuid.uuid4())[:8]

##############
### Client ###
##############

def get_client(client_id:int): # Returns a specific client in the database
    client = session.query(Client).filter_by(client_id=client_id).one_or_none()
    if client is None:
        return jsonify({"error": "Client not found"}), 404
    if client is not None:
        return jsonify({"name": client.name, "birthdate": client.birthdate, "opening_timestamp": client.opening_timestamp, "address": client.address, "phone_number": client.phone_number, "email": client.email}), 200

def change_password(client_id, password:str, new_password:str): # Changes the password of a client
    old_hash = password_hash(password)
    new_hash = password_hash(new_password)
    for client in session.query(Client).all():
        if client.client_id == client_id:
            if client.hash == old_hash:
                client.hash = new_hash
                session.commit()
                return "Password changed successfully.", 200
            return "Incorrect old password.", 400
    return f"client_id: {client_id} is not found.", 404

def add_client(name:str, birthdate:str, address:str, phone_number:str, email:str, password:str, **kwargs): # Adds a new client to the database
    client_id = generate_uuid_short()
    notes = kwargs.get("notes", None)
    new_client = Client(client_id, name, birthdate, timestamp(), address, phone_number, email, password_hash(password), notes, 1, 0, None)
    session.add(new_client)
    session.commit()
    return f"New client has been added: name: {name}, uuid: {client_id} ", 200

def delete_client(client_id): # Deletes a client from the database
    for client in session.query(Client).all():
        if client.client_id == client_id:
            if client.accounts == None:
                session.delete(client)
                session.commit()
                return f"client_id: {client_id} has been removed.", 200
            else:
                return f"client_id: {client_id} has active accounts and can not be removed.", 400
    return f"client_id: {client_id} is not found.", 404





def login_user(email:str, password:str):
    for client in session.query(Client).all():
        if client.email == email and client.password == password:
            return f"Welcome {client.name}."
    return "Invalid email or password."

def logout_user():
    return "You have been logged out." 



def update_client(client_id, name, birthdate, address, phone_number, email, notes):
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client.name = name
            client.birthdate = birthdate
            client.address = address
            client.phone_number = phone_number
            client.email = email
            client.notes = notes
            session.commit()
            return f"client_id: {client_id} has been updated."
    return f"Client ID: {client_id} is not found."



###############
### Account ###
###############

def get_account(account_id:int): # Returns a specific account in the database
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    if account is not None:
        for account in account:
            return jsonify({"client_id": account.client.id, "description": account.description, "account_type": account.account_type, "balance": account.balance, "enabled": account.enabled, "notes": account.notes}), 200

def add_account(client_id, description:str, account_type, **kwargs): # Adds a new account to the database
    account_id = generate_uuid_short()
    notes = kwargs.get("notes", None)
    client_found = None
     # Find the client
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client_found = client
            break

    # Check if client was found
    if client_found is None:
        return f"client_id: {client_id} is not found.", 422

    # Add the new account
    new_account = Account(account_id, client_id, description, timestamp(), account_type, 0, 1, notes, None)
    session.add(new_account)
    session.commit()
    return f"New account has been added: description: {description}, uuid: {account_id} ", 200
"""
    for client in session.query(Client).all():
        if client.client_id == client_id:
            new_account = Account(account_id, client_id, description, timestamp(), account_type, 0, 1, notes, None)
            session.add(new_account)
            session.commit()
            return f"New account has been added: description: {description}, uuid: {account_id} ", 200
        else:
            return f"client_id: {client_id} is not found.", 422
"""
def delete_account(account_id): # Deletes an account from the database
    for account in session.query(Account).all():
        if account.account_id == account_id:
            if account.balance == 0:
                session.delete(account)
                session.commit()
                return f"account_id: {account_id} has been removed.", 200
            else:
                return f"account_id: {account_id} has a balance and can not be removed.", 400
    return f"account_id: {account_id} is not found.", 404
        



def update_account(account_id:int, update:dict):    
    for account in session.query(Account).all():
        if account.account_id == account_id: 
            account.description = update["description"]
            account.account_type = update["account_type"]
            account.balance = update["balance"]
            account.enabled = update["enabled"]
            account.notes = update["notes"]
            session.commit()
            return f"account_id: {update['account_id']} has been updated."
    return f"account_id: {update['account_id']} is not found."




###################
### Transaction ###
###################

def get_transaction(transaction_id:int): # Returns a specific transaction in the database
    transaction = session.query(Transaction).filter_by(transaction_id=transaction_id).one_or_none()
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    if transaction is not None:
        return jsonify({"transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_number": transaction.account_number, "recipient_account_number": transaction.recipient_account_number}), 200

def transaction_history(account_id:int): # Returns all transactions for a specific account
    result = session.query(Transaction).filter(Transaction.account_id == account_id)
    return jsonify([{"transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_number": transaction.account_number, "recipient_account_number": transaction.recipient_account_number} for transaction in result]), 200

def add_transaction(amount:int, account_id, recipient_account_id, **kwargs): # Adds a new transaction to the database
    transaction_id = generate_uuid()
    for account in session.query(Account).all():
        if account.account_id == account_id:
            account_from = account
        if account.account_id == recipient_account_id:
            account_dest = account

    # Check if account has enough funds
    if account_from.balance < amount:
        return f"Account ID: {account_id} does not have enough funds to transfer {amount}.", 401

    # Perform the transaction
    account_from.balance -= amount
    account_dest.balance += amount
    transaction_type = "transfer"
    session.commit()

    # Create the transaction record
    description = kwargs.get("description", None)
    new_transaction = Transaction(transaction_id, transaction_type, amount, timestamp(), description, account_id, recipient_account_id)
    session.add(new_transaction)
    session.commit()

    return f"New transaction has been added: description: {description}, uuid: {transaction_id} ", 200   
"""
    if account_from is None:
        return f"Account ID: {account_id} is not found.", 404
    if account_dest is None:
        return f"Account ID: {account_to} is not found.", 404
    
    for account in session.query(Account).all():
        if account.account_id == account_id:
            if account.balance < amount:
                return f"Account ID: {account_id} does not have enough funds to transfer {amount}.", 401
            account.balance -= amount
            transaction_type = "withdraw"
            session.commit()
            return
        else:
            return f"Account ID: {account_id} is not found.", 404
    
    for account in session.query(Account).all():
        if account.account_id == account_to:
            account.balance += amount
            transaction_type = "transfer"
            session.commit()
    description = kwargs.get("description", None)
    new_transaction = Transaction(transaction_id, transaction_type, amount, timestamp(), description, account_id, account_to)
    session.add(new_transaction)
    session.commit()
    return f"New transaction has been added: description: {description}, uuid: {transaction_id} ", 200

"""

#####################
### Administrator ###
#####################

def get_all_clients(): # Returns all clients in the database
    clients = session.query(Client).all()
    return jsonify([{"client_id": client.client_id, "name": client.name, "birthdate": client.birthdate, "opening_timestamp": client.opening_timestamp, "address": client.address, "phone_number": client.phone_number, "email": client.email} for client in clients])

def get_all_accounts(): # Returns all accounts in the database
    accounts = session.query(Account).all()
    return jsonify([{"account_id": account.account_id, "client_id": account.client_id, "description": account.description, "open_timestamp": account.open_timestamp, "account_type": account.account_type, "balance": account.balance, "enabled": account.enabled, "notes": account.notes} for account in accounts])

def get_all_transactions(): # Returns all transactions in the database
    transactions = session.query(Transaction).all()
    return jsonify([{"transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_id": transaction.account_id, "recipient_account_id": transaction.recipient_account_id} for transaction in transactions])
        


def update_transaction(transaction_id, transaction_type, amount, description, account_id, recipient_account_id):
    for transaction in session.query(Transaction).all():
        if transaction.transaction_id == transaction_id:
            transaction.transaction_type = transaction_type
            transaction.amount = amount
            transaction.description = description
            transaction.account_id = account_id
            transaction.recipient_account_id = recipient_account_id
            session.commit()
            return f"Transaction ID: {transaction_id} has been updated."
    return f"Transaction ID: {transaction_id} is not found."
    
def apply_interest(account_id:int, interest_rate:float):
    for account in session.query(Account).filter(Account.account_id == account_id):
        if account.account_id == account_id:
            account.balance += account.balance * interest_rate
            session.commit()
            return f"Interest has been applied to Account ID: {account_id}."
    return f"Account ID: {account_id} is not found."

def apply_fee(account_id:int, fee:float):
    for account in session.query(Account).all():
        if account.account_id == account_id:
            account.balance -= fee
            session.commit()
            return f"Fee has been applied to Account ID: {account_id}."
    return f"Account ID: {account_id} is not found."

def delete_transaction(transaction_id:int):
    DELETE_TRANSACTION = "DELETE FROM transaction WHERE transaction_id=?"
    from api import session, Transaction
    for transaction in session.query(Transaction).all():
        if transaction.transaction_id == transaction_id:
            input(f"Are you sure you would like permanenty delete transaction ID: {transaction_id}? WARNING: This action can not be reversed. (Y/N) ") 
            if input == "Y"or input == "y":
                session.execute(DELETE_TRANSACTION, (transaction_id))
                print(f"Transaction ID: {transaction_id} has been removed.")
            else:
                return f"Transaction ID: {transaction_id} has NOT been removed."
            return
    return f"Transaction ID: {transaction_id} is not found."



