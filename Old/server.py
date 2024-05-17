# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Classes - Version 2

###############
### Modules ###
###############

import sqlite3
import os.path
import datetime
import connexion
from config import CONFIG

#################
### Functions ###
#################




###############
### Classes ###
###############

class Manager:
    def __init__():
        pass



class Client:
    def __init__(self, client_id, name, opening_timestamp, birthdate, address, phone_number, email:str, password, accounts, notes):
        self.client_id = client_id
        self.name = name
        self.birthdate = birthdate
        self.opening_timestamp = opening_timestamp
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.accounts = accounts
        self.notes = notes

    #If you call a print function on the object, it will return the following string (does not include password for security reasons)
    def __str__(self):
        return f"Client ID: {self.client_id}, Name: {self.name}, Birthdate: {self.birthdate}, Address: {self.address}, Phone Number: {self.phone_number}, Email: {self.email}"

    #This function will return the account list
    def get_accounts(self)->str:
        return f"Accounts: {self.accounts}"	

    #Change details (name, birthdate, address, phone number, email, password)
    #Change password
    
class Account:
    def __init__(self, account_id, description, open_timestamp, account_type, balance, enabled, notes, transactions):
        self.account_id = account_id
        self.description = description
        self.open_timestamp = open_timestamp
        self.account_type = account_type
        self.balance = balance
        self.enabled = enabled
        self.notes = notes
        self.transactions = transactions

    #If you call a print function on the object, it will return the following string
    def __str__(self):
        return f"Account ID: {self.account_id}, Description: {self.description}, Open Timestamp: {self.open_timestamp}, Account Type: {self.account_type}, Balance: {self.balance}, Enabled: {self.enabled}, Notes: {self.notes}, Transactions: {self.transactions}"

    # This function will return the transaction history of an account
    def transaction_history(self, account_id:int):
        return self.transactions
    
    #This function will remove the account
    def remove_account(self, account_id:int):
        REMOVE_ACCOUNT = "DELETE FROM account WHERE account_id=?"
        for account in self.accounts:
            if account.balance != 0: #If the account has a balance, it can not be removed
                return f"Account ID: {account_id} has a balance of {account.balance} and can not be removed."
            if account.account_id == account_id: #Check if account exists
                input(f"Are you sure you would like permanenty delete account ID: {account_id}? WARNING: This action can not be reversed. (Y/N) ") 
                if input == "Y"or input == "y": #If the user inputs Y or y, the account will be removed
                    db_conn = get_db_connection()
                    cursor = db_conn.cursor()
                    cursor.execute(REMOVE_ACCOUNT, (account_id, ) )
                    db_conn.commit()
                    print(f"Account ID: {account_id} has been removed.")
                else:
                    return f"Account ID: {account_id} has NOT been removed."
                return
        return f"Account ID: {account_id} is not found."
    
    #This function will return the account balance
    def account_balance(account_id:int):
        GET_ACCOUNT = "SELECT balance FROM account WHERE account_id = ?"

        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        cursor.execute(GET_ACCOUNT, (account_id) )
        resultset = cursor.fetchall()
        db_conn.close()

        if len(resultset) < 1:
            return "Not found", 404
        elif len(resultset) > 2:
            return "Too many results found.", 500

class Transaction:
    def __init__(self, transaction_id, transaction_type, amount, timestamp, description, account_number, recipient_account_number = None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp
        self.description = description
        self.account_number = account_number
        self.recipient_account_number = recipient_account_number

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Transaction Type: {self.transaction_type}, Amount: {self.amount}, Timestamp: {self.timestamp}, Description: {self.description} From Account Number: {self.account_number}, Recipient Account Number: {self.recipient_account_number}"
    
################
### Database ###
################

def Database():
    CLIENT_TABLE_CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS client (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birthdate DATE NOT NULL,
        opening_timestamp TIMESTAMP NOT NULL,
        address TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        notes TEXT NOT NULL
    )
    """
    ACCOUNT_TABLE_CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        open_timestamp TIMESTAMP NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL,
        enabled BOOLEAN NOT NULL,
        notes TEXT NOT NULL,
        client_id INTEGER NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    )
    """
    TRANSACT_TABLE_CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS transact (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        description TEXT NOT NULL,
        account_id INTEGER NOT NULL,
        recipient_account_id INTEGER, 
        FOREIGN KEY (account_id) REFERENCES account(account_id)
    )
    """
    # Check if the database exists
    if os.path.exists('bank.db'):
        print("Database already exists.")
    else:
        print("Database does not exist. Creating database.")   
    
    # Create the database and the tables if they do not exist, or connect to the database if it does exist
    db_connection = sqlite3.connect('bank.db') 
    db_cursor = db_connection.cursor()
    db_cursor.execute(CLIENT_TABLE_CREATION_QUERY)
    db_cursor.execute(ACCOUNT_TABLE_CREATION_QUERY)
    db_cursor.execute(TRANSACT_TABLE_CREATION_QUERY)
    db_connection.commit()


#################
### Connexion ###
#################

def API():
    app = connexion.App(__name__)
    app.add_api('api.yml')
    app.run(host=CONFIG["server"]["listen_address"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"])



################
### Run Code ###
################

if __name__ == "__main__":
    Database()
    API()