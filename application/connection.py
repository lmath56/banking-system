# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Connection file

import requests
from config import CONFIG

def get_connection():
    return requests.get(CONFIG["api"]["url"]) # Returns the connection to the API