# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility

import argparse
import sys
from connection import login, logout

def main():
    parser = argparse.ArgumentParser(description='Banking System CLI Utility')
    parser.add_argument('-u', '--username', type=str, help='Username for login')
    parser.add_argument('-p', '--password', type=str, help='Password for login')

    subparsers = parser.add_subparsers(dest='command')

    login_parser = subparsers.add_parser('login', help='Login to the system')
    logout_parser = subparsers.add_parser('logout', help='Logout from the system')

    args = parser.parse_args()

    if args.command == 'login':
        if not args.username or not args.password:
            print("Username and password are required for login.")
            sys.exit(1)
        response = login(args.username, args.password)
        print(f"{response.status_code}: {response.content}")
    elif args.command == 'logout':
        response = logout()
        print(f"{response.status_code}: {response.content}")
    else:
        print("Invalid command. Use 'login' or 'logout'.")

if __name__ == "__main__":
    main()