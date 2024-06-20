# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility Connection File

import hashlib
import json
import requests
from requests.models import Response
from config import CONFIG

##############
### System ###
##############

def format_balance(balance):
    """Formats the balance as a currency string with comma separators."""
    return f"€{balance:,.2f}"

def hash_password(password: str):
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
            session_data = {
                'session_cookie': response.cookies.get_dict(),
                'client_id': client_id
            }
            with open('session_data.json', 'w') as f:
                json.dump(session_data, f)
            return {'success': True, 'message': response_content.get('message')}
        else:
            return {'success': False, 'message': response_content.get('message')}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': str(e)}

def logout():
    """Logs out the current client by deleting the session data."""
    try:
        with open('session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.post(CONFIG["server"]["url"] + "/Client/Logout", cookies=session_data['session_cookie'])
        return response
    except requests.exceptions.RequestException as e:
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response

def get_client(client_id):
    """Retrieves the client details for the given client_id."""
    try:
        with open('session_data.json', 'r') as f:
            session_data = json.load(f)
        response = requests.get(CONFIG["server"]["url"] + "/Client", cookies=session_data['session_cookie'], params={'client_id': client_id})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}

def add_client(name, birthdate, address, phone_number, email, password, notes):
    data = {
        "name": name,
        "birthdate": birthdate,
        "address": address,
        "phone_number": phone_number,
        "email": email,
        "password": password,
        "notes": notes
    }
    try:   
        with open('session_data.json', 'r') as f:
            session_data = json.load(f)
            response = requests.get(CONFIG["server"]["url"] + "/Client", cookies=session_data['session_cookie'], params=data)  
            response.raise_for_status()
        if response.status_code == 200:
            print("Client retrieved successfully.")
        else:   
            print(f"Failed to retrieve client. Status code: {response.status_code}, message: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return {'success': False, 'message': "Could not connect to the server. Please try again later."}
            