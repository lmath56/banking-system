# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

from class_client import Client
from class_account import Account
from class_transaction import Transaction
from flask import jsonify, session as flask_session  # Imports the Flask modules
import hashlib # hashlib for password hashing
import datetime # datetime for timestamps
import uuid # uuid for unique identifiers
from functools import wraps # functools for decorators / user login
from database import * # Importing the database connection

##############
### System ###
##############

def timestamp(): # Returns the current timestamp
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def hash_password(password:str): # Converts a string to SHA512 hash
    return hashlib.sha512(password.encode()).hexdigest()

def generate_uuid(): # Generates a unique identifier for transactions
    return str(uuid.uuid4())

def generate_uuid_short(): # Generates a short uuid
    return str(uuid.uuid4())[:8]

#############
### Login ###
#############

def login(client_id:str, password:str): # Logs in a user
    password_hash = hash_password(password)
    for client in session.query(Client).all():
        if client.client_id == client_id and client.hash == password_hash:
            flask_session['client_id'] = client_id
            return jsonify({"message": f"{flask_session['client_id']} logged in succsessfully."}), 200
    return "Invalid client_id or password.", 401
        
def logout():
    if 'client_id' in flask_session:
        flask_session.pop('client_id', None)
        return jsonify({"message": "Logged out"}), 200
    return jsonify({"message": "Not logged in"}), 404

def status():
    if 'client_id' in flask_session:
        return jsonify({"message": f"Logged in as {flask_session['client_id']}"}), 200
    else:
        return jsonify({"message": "Not logged in"}), 400
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'client_id' not in flask_session:
            return jsonify({"error": "Not logged in"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'client_id' not in flask_session:
            return jsonify({"error": "Not logged in"}), 401
        for client in session.query(Client).all():
            if client.client_id == flask_session['client_id']:
                if client.administrator == 1:
                    return f(*args, **kwargs)
        return jsonify({"error": "Not authorised"}), 403
    return decorated_function

def get_current_client():
    client = flask_session['client_id']
    is_admin = session.query(Client).filter_by(client_id=client).one_or_none().administrator
    return client, is_admin
 

##############
### Client ###
##############

@login_required
def get_client(client_id:str): # Returns a specific client in the database
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return jsonify({"error": "You can only view your own client information."}), 403
    for client in session.query(Client).all():
        if client.client_id == client_id:
            return jsonify({"name": client.name, "birthdate": client.birthdate, "opening_timestamp": client.opening_timestamp, "address": client.address, "phone_number": client.phone_number, "email": client.email}), 200 
    return jsonify({"error": "Client not found"}), 404

@login_required
def update_client(client_id:str, **kwargs): # Updates a client in the database
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return jsonify({"error": "You can only update your own client information."}), 403
    for client in session.query(Client).all():
        if client.client_id == client_id:
            name = kwargs.get("name", None)
            birthdate = kwargs.get("birthdate", None)
            address = kwargs.get("address", None)
            phone_number = kwargs.get("phone_number", None)
            email = kwargs.get("email", None)
            notes = kwargs.get("notes", None)
            if name:
                client.name = name
            if birthdate:
                client.birthdate = birthdate
            if address:
                client.address = address
            if phone_number:
                client.phone_number = phone_number
            if email:
                client.email = email
            if notes:
                client.notes = notes
            session.commit()
            return f"client_id: {client_id} has been updated.", 299
    return f"Client ID: {client_id} is not found." , 400

@login_required
def change_password(client_id:str, password:str, new_password:str): # Changes the password of a client
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return jsonify({"error": "You can only update your own password."}), 403    
    old_hash = hash_password(password)
    new_hash = hash_password(new_password)
    for client in session.query(Client).all():
        if client.client_id == client_id:
            if client.hash == old_hash:
                client.hash = new_hash
                session.commit()
                return "Password changed successfully.", 200
            return "Incorrect old password.", 400
    return f"client_id: {client_id} is not found.", 404

###############
### Account ###
###############

@login_required
def get_account(account_id:str): # Returns a specific account in the database
    current_client_id, is_admin = get_current_client()
    account_owner = session.query(Account).filter_by(account_id=account_id).one_or_none().client_id
    if not is_admin and account_owner != current_client_id:
        return jsonify({"error": "You can only view your own account information."}), 403
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    for account in session.query(Account).all():
        if account.account_id == account_id:
            return jsonify({"client_id": account.client_id, "description": account.description, "account_type": account.account_type, "balance": account.balance, "enabled": account.enabled, "notes": account.notes}), 200
    return jsonify({"error": "Account not found"}), 404

@login_required
def add_account(client_id:str, description:str, account_type:str, **kwargs): # Adds a new account to the database
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return jsonify({"error": "You can only add accounts your own client account."}), 403    
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

@login_required       
def update_account(account_id:str, **kwargs): # Updates an account in the database    
    current_client_id, is_admin = get_current_client()
    account_owner = session.query(Account).filter_by(account_id=account_id).one_or_none().client_id
    if not is_admin and account_owner != current_client_id:
        return jsonify({"error": "You can only view your own account information."}), 403    
    for account in session.query(Account).all():
        if account.account_id == account_id: 
            description = kwargs.get("description", None)
            account_type = kwargs.get("account_type", None)
            balance = kwargs.get("balance", None)
            enabled = kwargs.get("enabled", None)
            notes = kwargs.get("notes", None)
            if description:
                account.description = description
            if account_type:
                account.account_type = account_type
            if balance:
                account.balance = balance
            if enabled:
                account.enabled = enabled
            if notes:
                account.notes = notes
            session.commit()
            return f"account_id: {account_id} has been updated.", 200
    return f"account_id: {account_id} is not found.", 400

###################
### Transaction ###
###################

@login_required
def get_transaction(transaction_id:int): # Returns a specific transaction in the database
    current_client_id, is_admin = get_current_client()
    transaction = session.query(Transaction).filter_by(transaction_id=transaction_id).one_or_none()
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    account = session.query(Account).filter_by(account_id=transaction.account_id).one_or_none()
    recipient_account = session.query(Account).filter_by(account_id=transaction.recipient_account_id).one_or_none()
    if not is_admin and (account.client_id != current_client_id and recipient_account.client_id != current_client_id):
        return jsonify({"error": "You can only view your own transaction information."}), 403
    return jsonify({"transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_id": transaction.account_id, "recipient_account_id": transaction.recipient_account_id}), 200

@login_required
def add_transaction(amount:int, account_id, recipient_account_id, **kwargs): # Adds a new transaction to the database
    current_client_id, is_admin = get_current_client()
    if not is_admin and account_id != current_client_id:
        return jsonify({"error": "You can only add transactions to your own account."}), 403
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

@login_required
def transaction_history(account_id:int): # Returns all transactions for a specific account
    current_client_id, is_admin = get_current_client()
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    if not account:
        return jsonify({"error": "Account not found."}), 404
    if not is_admin and account.client_id != current_client_id:
        return jsonify({"error": "You can only view your own transaction history."}), 403
    result = session.query(Transaction).filter(Transaction.account_id == account_id)
    return jsonify([{"transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_number": transaction.account_id, "recipient_account_number": transaction.recipient_account_id} for transaction in result]), 200

#####################
### Administrator ###
#####################

@admin_required
def delete_client(client_id:str): # Deletes a client from the database
    if client_id == flask_session['client_id']:
        return "You can not delete yourself.", 400
    
    for client in session.query(Client).all():
        if client.client_id == client_id:
            if client.accounts == None:
                session.delete(client)
                session.commit()
                return f"client_id: {client_id} has been removed.", 200
            else:
                return f"client_id: {client_id} has active accounts and can not be removed.", 400
    return f"client_id: {client_id} is not found.", 404

@admin_required
def delete_account(account_id:str): # Deletes an account from the database
    for account in session.query(Account).all():
        if account.account_id == account_id:
            if account.balance == 0:
                session.delete(account)
                session.commit()
                return f"account_id: {account_id} has been removed.", 200
            else:
                return f"account_id: {account_id} has a balance and can not be removed.", 400
    return f"account_id: {account_id} is not found.", 404

@admin_required
def get_all_clients(): # Returns all clients in the database
    clients = session.query(Client).all()
    return jsonify([{"client_id": client.client_id, "name": client.name, "birthdate": client.birthdate, "opening_timestamp": client.opening_timestamp, "address": client.address, "phone_number": client.phone_number, "email": client.email} for client in clients])

@admin_required
def get_all_accounts(): # Returns all accounts in the database
    accounts = session.query(Account).all()
    return jsonify([{"account_id": account.account_id, "client_id": account.client_id, "description": account.description, "open_timestamp": account.open_timestamp, "account_type": account.account_type, "balance": account.balance, "enabled": account.enabled, "notes": account.notes} for account in accounts])

@admin_required
def get_all_transactions(): # Returns all transactions in the database
    transactions = session.query(Transaction).all()
    return jsonify([{"transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, "amount": transaction.amount, "timestamp": transaction.timestamp, "description": transaction.description, "account_id": transaction.account_id, "recipient_account_id": transaction.recipient_account_id} for transaction in transactions])
        

@admin_required
def apply_interest(account_id:int, interest_rate:float):
    for account in session.query(Account).filter(Account.account_id == account_id):
        if account.account_id == account_id:
            account.balance += account.balance * interest_rate
            session.commit()
            return f"Interest has been applied to Account ID: {account_id}."
    return f"Account ID: {account_id} is not found."

@admin_required
def apply_fee(account_id:int, fee:float):
    for account in session.query(Account).all():
        if account.account_id == account_id:
            account.balance -= fee
            session.commit()
            return f"Fee has been applied to Account ID: {account_id}."
    return f"Account ID: {account_id} is not found."

@admin_required
def delete_transaction(transaction_id:int):
    DELETE_TRANSACTION = "DELETE FROM transaction WHERE transaction_id=?"
    return

@admin_required
def test_account_balances():
    # Get all transactions from the database
    all_transactions = session.query(Transaction).all()

    # Initialize a dictionary to store the calculated balance for each account
    calculated_balances = {}

    # Go through each transaction
    for transaction in all_transactions:
        # If the account ID of the transaction is not in the dictionary, add it with a balance of 0
        if transaction.account_id not in calculated_balances:
            calculated_balances[transaction.account_id] = 0

        # Update the calculated balance for the account
        if transaction.transaction_type == 'Deposit':
            calculated_balances[transaction.account_id] += transaction.amount
        elif transaction.transaction_type == 'Withdrawal':
            calculated_balances[transaction.account_id] -= transaction.amount

    # Get all accounts from the database
    all_accounts = session.query(Account).all()

    # Initialize a list to store the discrepancies
    discrepancies = []

    # Go through each account
    for account in all_accounts:
        # If the calculated balance doesn't match the stored balance, add the discrepancy to the list
        if calculated_balances.get(account.account_id, 0) != account.balance:
            discrepancies.append({"error": f"Alert: Account {account.account_id} has a balance discrepancy. Stored balance is {account.balance}, but calculated balance is {calculated_balances.get(account.account_id, 0)}."})

    # Return the list of discrepancies
    return jsonify(discrepancies), 200


@admin_required
def add_client(name:str, birthdate:str, address:str, phone_number:str, email:str, password:str, **kwargs): # Adds a new client to the database
    client_id = generate_uuid_short()
    notes = kwargs.get("notes", None)
    new_client = Client(client_id, name, birthdate, timestamp(), address, phone_number, email, hash_password(password), notes, 1, 0, None)
    session.add(new_client)
    session.commit()
    return client_id, 200

def initialise_database(password:str):
    existing_clients = session.query(Client).all() # Check if any clients exist in the database
    if not existing_clients: # If no clients exist, create an administrator client
        add_client('ADMINISTRATOR', 'ADMINISTRATOR', 'ADMINISTRATOR', 'ADMINISTRATOR', 'ADMINISTRATOR', password)  # Add the administrator client
        session.commit()
        admin_client = session.query(Client).filter_by(name='ADMINISTRATOR').one() # Retrieve the administrator client
        admin_client.administrator = 1 # Set the new client as an administrator
        session.commit()
        return jsonify(f"Database initialised with administrator account with client_id {admin_client.client_id}"), 200
    return jsonify("Database not empty, this function cannot be used."), 400

@admin_required
def promote_to_admin(client_id:str):
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client.administrator = 1
            session.commit()
            return f"client_id: {client_id} has been promoted to administrator.", 200
    return f"client_id: {client_id} is not found.", 404

@admin_required
def demote_from_admin(client_id:str):
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client.administrator = 0
            session.commit()
            return f"client_id: {client_id} has been demoted from administrator.", 200
    return f"client_id: {client_id} is not found.", 404