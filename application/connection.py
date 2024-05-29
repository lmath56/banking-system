import requests
from requests.models import Response
from config import CONFIG
import json
from tkinter import messagebox

##############
### System ###
##############

def format_balance(balance):
    """Formats the balance as a currency string with comma separators."""
    return f"€{balance:,.2f}"

#####################
### API Functions ###
#####################

def authenticate_client(client_id, client_password):
    """Authenticates a client with the given client_id and client_password."""
    try:
        response = requests.post(CONFIG["server"]["url"] + "/Client/Login", params={'client_id': client_id, 'password': client_password})
        return response
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response
    
def logout_client():
    """Logs out the current client."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.post(CONFIG["server"]["url"] + "/Client/Logout", cookies=session_data['session_cookie'])
        return response
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response

def get_client(client_id):
    """Retrieves the client details for the given client_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Client", cookies=session_data['session_cookie'], params={'client_id': client_id})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def update_client(client_id, otp_code, email=None, phone_number=None, address=None):
    """Updates the client details for the given client_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        params = {'client_id': client_id, 'otp_code': otp_code}
        if email is not None:
            params['email'] = email
        if phone_number is not None:
            params['phone_number'] = phone_number
        if address is not None:
            params['address'] = address
        response = requests.post(CONFIG["server"]["url"] + "/Client", cookies=session_data['session_cookie'], params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            return {'success': False, 'message': "Invalid OTP."}
        print(f"HTTPError: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def get_accounts(client_id):
    """Retrieves the accounts associated with the given client_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Client/Accounts", cookies=session_data['session_cookie'], params={'client_id': client_id})
        response.raise_for_status()
        accounts = response.json()
        if isinstance(accounts, str):
            accounts = json.loads(accounts)
        return accounts
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def get_transactions(account_id):
    """Retrieves the transactions for the given account_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Transaction/History", cookies=session_data['session_cookie'], params={'account_id': account_id})
        response.raise_for_status()
        transactions = response.json()
        if isinstance(transactions, str):
            transactions = json.loads(transactions)
        return transactions
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def get_account(account_id):
    """Retrieves the account details for the given account_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Account", cookies=session_data['session_cookie'], params={'account_id': account_id})
        response.raise_for_status()
        account = response.json()
        if 'data' not in account or 'balance' not in account['data']:
            print(f"Error: The account dictionary does not have a 'balance' key. Account: {account}")
            return None
        return account
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def update_account(account_id, description=None, notes=None):
    """Updates the account details for the given account_id."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        params = {'account_id': account_id}
        if description is not None:
            params['description'] = description
        if notes is not None:
            params['notes'] = notes
        response = requests.put(CONFIG["server"]["url"] + "/Account", cookies=session_data['session_cookie'], params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def new_transaction(account):
    """Creates a new transaction for the given account."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        params = {'account_id': account['account_id']}
        response = requests.post(CONFIG["server"]["url"] + "/Transaction/History", cookies=session_data['session_cookie'], params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def generate_otp():
    """Generates a new OTP for the current client, which is sent by Email."""
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        client_id = session_data['client_id']
        response = requests.post(f"{CONFIG['server']['url']}/OTP/Generate", cookies=session_data['session_cookie'], params={'client_id': client_id})
        if response.status_code == 200:
            messagebox.showinfo("OTP", "OTP has been sent to your email.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        messagebox.showerror("Error", f"Could not generate OTP: {e}")