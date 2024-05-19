# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility

import requests
import argparse
import sys
from config import CONFIG

SERVER_URL = "http://127.0.0.1:81"

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

if __name__ == "__main__":
    sys.exit( main() )