# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility Connection File

import requests
from config import CONFIG
import hashlib
import json

##############
### System ###
##############

def format_balance(balance):
    """Formats the balance as a currency string with comma separators."""
    return f"€{balance:,.2f}"

def hash_password(password:str):
    """Hashes a password using the SHA-512 algorithm and returns the hexadecimal representation of the hash."""
    return hashlib.sha512(password.encode()).hexdigest()

#####################
### API Functions ###
#####################

def login(client_id, password):
    """Authenticates a client with the given client_id and client_hash."""
    try:
        client_hash = hash_password(password)
        response = requests.post(CONFIG["server"]["url"] + "/Client/Login", json={'client_id': client_id, 'client_hash': client_hash})
        response.raise_for_status()
        response_content = json.loads(response.content)  # Parse the JSON response
        if response.status_code == 200 and response_content.get('success'):
            return {'success': True, 'message': response_content.get('message')}
        else:
            return {'success': False, 'message': response_content.get('message')}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': str(e)}

def logout():
    url = f"{CONFIG['server']['url']}/logout"
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_content = json.loads(response.content)  # Parse the JSON response
        if response.status_code == 200 and response_content.get('success'):
            return {'success': True, 'message': response_content.get('message')}
        else:
            return {'success': False, 'message': response_content.get('message')}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': str(e)}
