# api_client.py
import requests
from config import CONFIG

def login(username, password):
    url = f"{CONFIG['server']['url']}/login"
    payload = {'username': username, 'password': password}
    response = requests.get(url, params=payload)
    return response

def logout():
    url = f"{CONFIG['server']['url']}/logout"
    response = requests.get(url)
    return response
