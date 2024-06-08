# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

from class_client import Client
from class_account import Account
from class_transaction import Transaction
from emailer import EmailSendingError # Import the EmailSendingError class to handle email sending errors
from flask import jsonify, session as flask_session  # Imports the Flask modules
from functools import wraps # For decorators / user login
from database import * # Importing the database connection
from emailer import send_email # Importing the emailer function
from flask import session as flask_session
from flask import request
from database import session
import hashlib # For password hashing
import datetime # For timestamps
import uuid # For unique identifiers
import random # For OTP generation
import time # For OTP generation
import re # For password hash validation

otps = {} # Temporary dictionary to store OTPs and their creation time

##############
### System ###
##############

def timestamp():
    """Returns the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'."""
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def hash_password(password:str):
    """Hashes a password using the SHA-512 algorithm and returns the hexadecimal representation of the hash."""
    return hashlib.sha512(password.encode()).hexdigest()

def generate_uuid():
    """Generates a unique identifier using the UUID4 algorithm and returns it as a string."""
    return str(uuid.uuid4())

def generate_uuid_short():
    """Generates a short unique identifier using the UUID4 algorithm and returns the first 8 characters as a string."""
    return str(uuid.uuid4())[:8]

def get_email(client_id:str):
    """Returns the email of a client given their client_id. If the client is not found, returns None."""
    client = session.query(Client).filter_by(client_id=client_id).one_or_none()
    return client.email if client else None

def format_response(success: bool, message: str = '', data: dict = None):
    """Formats the response for the API so that it is standardised across all functions."""
    response = {
        'success': success,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)

def get_current_client():
    """Returns the client_id and administrator status of the currently logged in client. If no client is logged in, returns None, None."""
    if 'client_id' not in flask_session:
        return None, None
    client = flask_session['client_id']
    client_obj = session.query(Client).filter_by(client_id=client).one_or_none()
    if client_obj is None:
        return None, None
    return client_obj.client_id, client_obj.administrator

def verify_otp(client_id:str, otp:int):
    """Verifies a one time password for a client. Returns True if the OTP is correct and False otherwise."""
    if CONFIG["smtp"]["true"] == "False":
        return True
    if client_id in otps:
        stored_otp, creation_time = otps[client_id]
        if stored_otp == otp and time.time() - creation_time <= 300:  # Check if OTP is within 5 minutes
            return True
    return False
    
def delete_otp(client_id:str):
    """Deletes the OTP for a client."""
    if client_id in otps:
        del otps[client_id]

def clean_expired_otps():
    """Checks for expired OTPs and deletes them. An OTP is considered expired if it is older than 5 minutes."""
    current_time = time.time()
    expired_otps = [client_id for client_id, (otp, creation_time) in otps.items() if current_time - creation_time > 300]  # Find OTPs older than 5 minutes
    otps_removed = 0
    for client_id in expired_otps:
        delete_otp(client_id)
        otps_removed += 1
    log_event(f"Cleaned {otps_removed} expired OTPs.")

def log_event(data_to_log:str):
    """Logs an event to the log file."""
    with open("log.txt", "a") as log_file:
        log_file.write(f"{timestamp()} - {data_to_log}\n")


######################
### Authentication ###
######################

def login():
    """Logs in a client using their client_id and password hash. Returns a success message if the login is successful and an error message otherwise."""
    data = request.get_json()
    client_id = data.get('client_id')
    client_hash = data.get('client_hash')
    client = session.query(Client).filter_by(client_id=client_id).first()
    if client and client.hash == client_hash:
        flask_session['client_id'] = client_id
        log_event(f"{client_id} logged in successfully.")
        return format_response(True, f"{flask_session['client_id']} logged in successfully."), 200
    return format_response(False, "Invalid client_id or password."), 401

def logout():
    """Logs out a client. Returns a success message if the logout is successful and an error message otherwise."""
    if 'client_id' in flask_session:
        flask_session.pop('client_id', None)
        return format_response(True, "Logged out successfully."), 200
    return format_response(False, "Not logged in."), 400

def status():
    """Returns the current status of the client."""
    if 'client_id' in flask_session:
        return format_response(True, f"Logged in as {flask_session['client_id']}"), 200
    else:
        return format_response(False, "Not logged in."), 400
    
def login_required(f):
    """Decorator function to check if a client is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'client_id' not in flask_session:
            return format_response(False, "Not logged in."), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator function to check if a client is an administrator before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'client_id' not in flask_session:
            return format_response(False, "Not logged in."), 401
        for client in session.query(Client).all():
            if client.client_id == flask_session['client_id']:
                if client.administrator == 1:
                    return f(*args, **kwargs)
        return format_response(False, "Not authorised."), 403
    return decorated_function

@login_required
def generate_otp(client_id: str):
    """Generates a one-time password for a client and sends it to their email address. Returns a success message if the OTP is generated and an error message otherwise."""
    if CONFIG["smtp"]["true"] == "False":
        return format_response(True, "OTP generation disabled as SMTP is not enabled."), 200
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return format_response(False, "You can only generate OTPs for your own client account."), 403
    email = get_email(client_id)
    if email:
        password = int(random.randint(100000, 999999))  # Generate a 6-digit OTP
        try:
            send_email(email, "Luxbank One Time Password", f"Your one-time password is: {password}")
            otps[client_id] = (password, time.time())  # Store the OTP and the current time
            log_event(f"OTP Code {password} emailed to {email}")
            print(f"OTP Code {password} emailed to {email}")
            return format_response(True, "OTP generated and sent successfully."), 200
        except EmailSendingError as e:
            log_event(f"Error sending email: {str(e)}")
            error_message = "Error sending email. Please try again later."
            if e.original_error:
                error_message += f" Original error: {str(e.original_error)}"
            return format_response(False, error_message), 500
    else:
        return format_response(False, "Email address not found for the client."), 404

##############
### Client ###
##############

@login_required
def get_client(client_id: str):
    """Returns a specific client in the database. If the client is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403

    client = session.query(Client).filter_by(client_id=client_id).one_or_none()
    if client:
        return format_response(True, "", client.to_dict()), 200

    return format_response(False, "Client not found."), 404

@login_required
def update_client(client_id:str, otp_code:int, **kwargs):
    """Updates a client in the database. If the client is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    if not verify_otp(current_client_id, otp_code):
        return format_response(False, "Invalid OTP."), 400  # Changed to 400 Bad Request
    if not is_admin and client_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    client = session.query(Client).filter_by(client_id=client_id).first()
    if client:
        for field in ['name', 'birthdate', 'address', 'phone_number', 'email', 'notes']:
            if field in kwargs and kwargs[field] is not None:
                setattr(client, field, kwargs[field])
        session.commit()
        return format_response(True, f"Client ID: {client_id} has been updated."), 200
    return format_response(False, "Client not found."), 404


def change_password():
    """Changes the password for a client in the database. If the client is not found, returns an error message."""
    data = request.get_json()
    client_id = data.get('client_id')
    hash_old_password = data.get('hash_old_password')
    hash_new_password = data.get('hash_new_password')
    otp_code = data.get('otp_code')
    current_client_id, is_admin = get_current_client()
    otp_verified = verify_otp(client_id, otp_code) # Verify if the OTP is correct
    if not is_admin and client_id != current_client_id: # Check if the client is authorized to change the password
        return format_response(False, "You can only update your own client information."), 401
    if not otp_verified: # Recheck OTP verification after authorisation check
        return format_response(False, "Invalid OTP."), 400
    hash_format = r'^[0-9a-f]{128}$' # Validate new password format
    if not re.match(hash_format, hash_new_password):
        return format_response(False, "Invalid new password format (must be provided as a hash)."), 400
    client = session.query(Client).filter_by(client_id=client_id).first() # Check if the old password hash matches and update to the new password hash
    if client:
        if client.hash == hash_old_password:
            client.hash = hash_new_password
            session.commit()
            delete_otp(current_client_id)
            log_event(f"Password for client_id {client_id} has been updated by {current_client_id}.")
            return format_response(True, f"Password for client_id {client_id} has been updated."), 200
        else:
            return format_response(False, "Invalid old password."), 400
    else:
        return format_response(False, "Client not found."), 404

@login_required
def get_accounts(client_id: str):
    """Returns all accounts for a specific client in the database. If the client is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    if current_client_id is None:
        raise Exception("No current client found")
    if not is_admin and client_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    accounts = session.query(Account).filter(Account.client_id == client_id)
    return format_response(True, "", [account.to_dict() for account in accounts]), 200

###############
### Account ###
###############

@login_required
def get_account(account_id: str):
    """Returns a specific account in the database. If the account is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    if account is None:
        return format_response(False, "Account not found."), 404
    account_owner = account.client_id
    if not is_admin and account_owner != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    return format_response(True, "", account.to_dict()), 200


@login_required
def add_account(client_id:str, description:str, account_type:str, **kwargs):
    """Adds a new account to the database. If the client is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    if not is_admin and client_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    account_id = generate_uuid_short()
    notes = kwargs.get("notes", None)
    client_found = None
    for client in session.query(Client).all(): # Find the client
        if client.client_id == client_id:
            client_found = client
            break
    if client_found is None: # If the client is not found, return an error
        return format_response(False, "Client not found."), 404
    new_account = Account(account_id, client_id, description, timestamp(), account_type, 0, 1, notes, None) # Create the new account
    session.add(new_account)
    session.commit()
    return format_response(True, f"New account has been added: account_id: {account_id}"), 200

@login_required       
def update_account(account_id: str, otp_code: str, **kwargs):
    """Updates an account in the database. If the account is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()

    # Verify OTP
    if not verify_otp(current_client_id, otp_code):
        return format_response(False, "Invalid OTP."), 400

    # Query the account once
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    if account is None:
        return format_response(False, "Account not found."), 404

    account_owner = account.client_id

    # Check permissions
    if not is_admin and account_owner != current_client_id:
        return format_response(False, "You can only update your own account information."), 403    

    # Update the account with provided kwargs
    description = kwargs.get("description")
    account_type = kwargs.get("account_type")
    balance = kwargs.get("balance")
    enabled = kwargs.get("enabled")
    notes = kwargs.get("notes")

    if description is not None:
        account.description = description
    if account_type is not None:
        account.account_type = account_type
    if balance is not None:
        account.balance = balance
    if enabled is not None:
        account.enabled = enabled
    if notes is not None:
        account.notes = notes

    # Commit the changes
    session.commit()
    return format_response(True, f"account_id: {account_id} has been updated."), 200


###################
### Transaction ###
###################

@login_required
def get_transaction(transaction_id:int):
    """Returns a specific transaction in the database. If the transaction is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    transaction = session.query(Transaction).filter_by(transaction_id=transaction_id).one_or_none()
    if not transaction:
        return format_response(False, "Transaction not found."), 404
    account = session.query(Account).filter_by(account_id=transaction.account_id).one_or_none()
    recipient_account = session.query(Account).filter_by(account_id=transaction.recipient_account_id).one_or_none()
    if not is_admin and (account.client_id != current_client_id and recipient_account.client_id != current_client_id):
        return format_response(False, "You can only view your own client information."), 403
    return format_response(True, "", transaction.to_dict()), 200

@login_required
def add_transaction(amount: float, account_id: str, recipient_account_id: str, otp_code: int, description: str):
    """Adds a new transaction to the database. If the account is not found, returns an error message."""
    print(f"Adding transaction: amount: {amount}, account_id: {account_id}, recipient_account_id: {recipient_account_id}, otp_code: {otp_code}, description: {description}")
    current_client_id, is_admin = get_current_client()
    if not is_admin and account_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    otp_verified = verify_otp(current_client_id, otp_code)
    if not otp_verified:
        return format_response(False, "Invalid OTP."), 400
    
    transaction_id = generate_uuid()
    account_from = session.query(Account).filter_by(account_id=account_id).one_or_none()
    account_dest = session.query(Account).filter_by(account_id=recipient_account_id).one_or_none()


    if account_from is None or account_dest is None:
        return format_response(False, "Account not found."), 404
    if account_from.balance < amount:
        return format_response(False, "Insufficient funds."), 400
    delete_otp(current_client_id)
    # Perform the transaction
    account_from.balance -= amount
    account_dest.balance += amount
    transaction_type = "transfer"
    session.commit()
    # Create the transaction record
    new_transaction = Transaction(transaction_id, transaction_type, amount, timestamp(), description, account_id, recipient_account_id)
    session.add(new_transaction)
    session.commit()
    
    return format_response(True, f"New transaction has been added: transaction_id: {transaction_id}"), 200

@login_required
def transaction_history(account_id:int):
    """Returns all transactions for a specific account in the database. If the account is not found, returns an error message."""
    current_client_id, is_admin = get_current_client()
    account = session.query(Account).filter_by(account_id=account_id).one_or_none()
    if not account:
        return format_response(False, "Account not found."), 404
    if not is_admin and account.client_id != current_client_id:
        return format_response(False, "You can only view your own client information."), 403
    result = session.query(Transaction).filter(Transaction.account_id == account_id)
    return format_response(True, "", [transaction.to_dict() for transaction in result]), 200

#####################
### Administrator ###
#####################

@admin_required
def delete_client(client_id:str):
    """Deletes a client from the database. If the client is not found, returns an error message."""
    if client_id == flask_session['client_id']:
        return format_response(False, "You cannot delete your own account."), 400
    for client in session.query(Client).all():
        if client.client_id == client_id:
            if client.accounts == None:
                session.delete(client)
                session.commit()
                log_event(f"Client ID: {client_id} has been removed by {flask_session['client_id']}.")
                return format_response(True, f"client_id: {client_id} has been removed."), 200
            else:
                return format_response(False, "Client has accounts and can not be removed."), 400
    return format_response(False, "Client not found."), 404

@admin_required
def delete_account(account_id:str):
    """Deletes an account from the database. If the account is not found, returns an error message."""
    for account in session.query(Account).all():
        if account.account_id == account_id:
            if account.balance == 0:
                session.delete(account)
                session.commit()
                log_event(f"Account ID: {account_id} has been removed by {flask_session['client_id']}.")
                return format_response(True, f"account_id: {account_id} has been removed."), 200
            else:
                return format_response(False, "Account has a balance and can not be removed."), 400
    return format_response(False, "Account not found."), 404

@admin_required
def get_all_clients():
    """Returns all clients in the database."""
    clients = session.query(Client).all()
    log_event(f"All clients have been retrieved by {flask_session['client_id']}.")
    return format_response(True, "", [client.to_dict() for client in clients]), 200

@admin_required
def get_all_accounts():
    """Returns all accounts in the database."""
    accounts = session.query(Account).all()
    log_event(f"All accounts have been retrieved by {flask_session['client_id']}.")
    return format_response(True, "", [account.to_dict() for account in accounts]), 200

@admin_required
def get_all_transactions():
    """Returns all transactions in the database."""
    transactions = session.query(Transaction).all()
    log_event(f"All transactions have been retrieved by {flask_session['client_id']}.")
    return format_response(True, "", [transaction.to_dict() for transaction in transactions]), 200

@admin_required
def apply_interest(account_id:int, interest_rate:float):
    """Applies interest to an account based on the interest rate. If the account is not found, returns an error message."""
    for account in session.query(Account).filter(Account.account_id == account_id):
        if account.account_id == account_id:
            interest = account.balance * interest_rate
            account.balance += interest
            session.commit()
            log_event(f"Interest of €{interest} has been applied to Account ID: {account_id} by {flask_session['client_id']}.")
            return format_response(True, f"€{interest} in interest has been applied to Account ID: {account_id}."), 200
    return format_response(False, "Account not found."), 404

@admin_required
def apply_fee(account_id:int, fee:float):
    """Applies a fee to an account based on the fee amount. If the account is not found, returns an error message."""
    for account in session.query(Account).all():
        if account.account_id == account_id:
            account.balance -= fee
            session.commit()
            log_event(f"Fee of €{fee} has been applied to Account ID: {account_id} by {flask_session['client_id']}.")
            return format_response(True, f"€{fee} in fees has been applied to Account ID: {account_id}."), 200
    return format_response(False, "Account not found."), 404

@admin_required
def delete_transaction(transaction_id:int):
    """Deletes a transaction from the database. If the transaction is not found, returns an error message."""
    for transaction in session.query(Transaction).all():
        if transaction.transaction_id == transaction_id:
            session.delete(transaction)
            session.commit()
            log_event(f"Transaction ID: {transaction_id} has been removed by {flask_session['client_id']}.")
            return format_response(True, f"Transaction ID: {transaction_id} has been removed."), 200
    return format_response(False, "Transaction not found."), 404

@admin_required
def modify_balance(transaction_id:int, amount:int):
    """Modifies the amount of a transaction in the database. If the transaction is not found, returns an error message."""
    for transaction in session.query(Transaction).all():
        if transaction.transaction_id == transaction_id:
            transaction.amount = amount
            session.commit()
            log_event(f"Transaction ID: {transaction_id} has been modified by {flask_session['client_id']}.")
            return format_response(True, f"Transaction ID: {transaction_id} has been modified."), 200
    return format_response(False, "Transaction not found."), 404

@admin_required
def test_account_balances():
    """Checks all account balances in the database and returns a list of discrepancies."""
    log_event(f"Account balances have been checked by {flask_session['client_id']}.")
    all_transactions = session.query(Transaction).all()# Get all transactions from the database
    calculated_balances = {} # Initialize a dictionary to store the calculated balance for each account
    for transaction in all_transactions: # Go through each transaction
        if transaction.account_id not in calculated_balances: # If the account ID of the transaction is not in the dictionary, add it with a balance of 0
            calculated_balances[transaction.account_id] = 0
        if transaction.transaction_type == 'Deposit': # Update the calculated balance for the account
            calculated_balances[transaction.account_id] += transaction.amount
        elif transaction.transaction_type == 'Withdrawal':
            calculated_balances[transaction.account_id] -= transaction.amount
    all_accounts = session.query(Account).all() # Get all accounts from the database
    discrepancies = [] # Initialize a list to store the discrepancies
    for account in all_accounts:  # Go through each account
        if calculated_balances.get(account.account_id, 0) != account.balance: # If the calculated balance doesn't match the stored balance, add the discrepancy to the list
            discrepancies.append({"error": f"Alert: Account {account.account_id} has a balance discrepancy. Stored balance is {account.balance}, but calculated balance is {calculated_balances.get(account.account_id, 0)}."})
    return format_response(True, "", discrepancies), 200 # Return the list of discrepancies

@admin_required
def add_client(name:str, birthdate:str, address:str, phone_number:str, email:str, password:str, **kwargs):
    """Adds a new client to the database."""
    client_id = generate_uuid_short()
    notes = kwargs.get("notes", None)
    new_client = Client(client_id, name, birthdate, timestamp(), address, phone_number, email, hash_password(password), notes, 1, 0, None)
    session.add(new_client)
    session.commit()
    log_event(f"New client has been added: client_id: {client_id} by {flask_session['client_id']}.")
    return format_response(True, f"New client has been added: client_id: {client_id}"), 200

def initialise_database(password:str, email:str):
    """Initialises the database with an administrator client if no clients exist."""
    existing_clients = session.query(Client).all() # Check if any clients exist in the database
    if not existing_clients: # If no clients exist, create an administrator client
        new_client = Client(generate_uuid_short(), "ADMIN", "ADMIN", timestamp(), "ADMIN", "ADMIN", email, hash_password(password), None, 1, 0, None)
        session.add(new_client)
        session.commit()
        admin_client = session.query(Client).filter_by(name='ADMIN').one() # Retrieve the administrator client
        admin_client.administrator = 1 # Set the new client as an administrator
        session.commit()
        log_event(f"Database initialised with administrator account with client_id {admin_client.client_id}.")
        return format_response(True, f"Database initialised with administrator account with client_id {admin_client.client_id}"), 200
    return format_response(False, "Database not empty."), 400

@admin_required
def promote_to_admin(client_id:str):
    """Promotes a client to administrator status. If the client is not found, returns an error message."""
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client.administrator = 1
            session.commit()
            log_event(f"Client ID: {client_id} has been promoted to administrator by {flask_session['client_id']}.")
            return format_response(True, f"client_id: {client_id} has been promoted to administrator."), 200
    return format_response(False, f"client_id: {client_id} is not found."), 404

@admin_required
def demote_from_admin(client_id:str):
    """Demotes a client from administrator status. If the client is not found, returns an error message."""
    for client in session.query(Client).all():
        if client.client_id == client_id:
            client.administrator = 0
            session.commit()
            log_event(f"Client ID: {client_id} has been demoted from administrator by {flask_session['client_id']}.")
            return format_response(True, f"client_id: {client_id} has been demoted from administrator."), 200
    return format_response(False, f"client_id: {client_id} is not found."), 404

