# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Connection file

import requests
from requests.models import PreparedRequest, Response
from config import CONFIG
import json


def authenticate_client(client_id, client_password):
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
    try:
        with open('application\\session_data.json', 'r') as f: # Open the session_data.json file in read mode
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
    try:
        with open('application\\session_data.json', 'r') as f: # Open the session_data.json file in read mode
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Client", cookies=session_data['session_cookie'], params={'client_id': client_id})
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response.json() 
    
def update_client(client_id, email=None, phone_number=None, address=None):
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        
        # Create a dictionary of parameters to update
        params = {'client_id': client_id}
        if email is not None:
            params['email'] = email
        if phone_number is not None:
            params['phone_number'] = phone_number
        if address is not None:
            params['address'] = address

        response = requests.put(
            CONFIG["server"]["url"] + "/Client",
            cookies=session_data['session_cookie'],
            params=params
        )
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}
    
def get_accounts(client_id):
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)

        response = requests.get(
            CONFIG["server"]["url"] + "/Client/Accounts",
            cookies=session_data['session_cookie'],
            params={'client_id': client_id}
        )
        response.raise_for_status()  # Raise an exception if the request failed
        accounts = response.json()
        if isinstance(accounts, str):  # If the response is a string, convert it to a list of dictionaries
            accounts = json.loads(accounts)
        return accounts
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}
    
def format_balance(balance): # Formats the balance as a currency string with comma seperator
    return f"€{balance:,.2f}"

def get_transactions(account_id):
    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)

        response = requests.get(
            CONFIG["server"]["url"] + "/Account/Transactions",
            cookies=session_data['session_cookie'],
            params={'account_id': account_id}
        )
        response.raise_for_status()  # Raise an exception if the request failed
        transactions = response.json()
        if isinstance(transactions, str):  # If the response is a string, convert it to a list of dictionaries
            transactions = json.loads(transactions)
        return transactions
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}
    
