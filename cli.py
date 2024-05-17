# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility

import requests

SERVER_URL = "http://127.0.0.1:5000"

def main():
    username = "john"
    password = "doe"
    print(f"Login with {username} and {password}:")
    response = requests.get( f"{SERVER_URL}/login?username={username}&password={password}")
    print(f"{response}, {response.content}")

    print(f"Logout:")
    response = requests.get( f"{SERVER_URL}/logout")
    print(f"{response}, {response.content}")
    print(f"Closing")
main()