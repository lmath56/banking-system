# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Connection file

import requests
from requests.models import PreparedRequest, Response
from config import CONFIG
import json


def authenticate_client(client_id, client_password):
    try:
        # Send a POST request to the /Client/Login endpoint with the client_id and password
        response = requests.post(CONFIG["server"]["url"] + "/Client/Login", params={'client_id': client_id, 'password': client_password})

        # Return the response from the API
        return response
    except requests.exceptions.RequestException as e:
        # If a RequestException is raised, print the exception message
        print(f"RequestException: {e}")
        
        # Create a new Response object with a status code of 500 and the error message in the JSON body
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response
    
def logout_client():
    try:
        # Load the session cookie from the file
        with open('application\\session_cookie.json', 'r') as f:
            cookies = json.load(f)

        # Send a POST request to the /Client/Logout endpoint
        response = requests.post(CONFIG["server"]["url"] + "/Client/Logout", cookies=cookies)

        # Return the response from the API
        return response
    except requests.exceptions.RequestException as e:
        # If a RequestException is raised, print the exception message
        print(f"RequestException: {e}")
        
        # Create a new Response object with a status code of 500 and the error message in the JSON body
        response = Response()
        response.status_code = 500
        response._content = b'{"success": false, "message": "Could not connect to the server. Please try again later."}'
        return response