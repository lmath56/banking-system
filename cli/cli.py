# Lucas Mathews - Fontys Student ID: 5023572
# Banking System CLI Utility

import json
import argparse
import sys
from config import CONFIG
from getpass import getpass
from connection import login, logout, get_client, add_client
from test_database_generator import generate_test_database 


def show_menu():
    print("\nAvailable options:")
    print("1. Logout and exit")
    print("2. New client")
    print("3. Add test data to database (50 clients, 2 accounts each, 40 transactions each)")
    print("4. Initialise Database")
    #print("5. Promote to Admin")
    #print("6. Demote from Admin")
    #print("7. Delete user")S
    print("\n")

def main():
    parser = argparse.ArgumentParser(description='Banking System CLI Utility')
    parser.add_argument('-u', '--username', type=str, default=CONFIG["client"]["default_id"], help='Username for login')
    parser.add_argument('-p', '--password', type=str, default=CONFIG["client"]["default_password"], help='Password for login')

    subparsers = parser.add_subparsers(dest='command')

    login_parser = subparsers.add_parser('login', help='Login to the system')
    logout_parser = subparsers.add_parser('logout', help='Logout from the system')

    args = parser.parse_args()

    if not args.command:
        while True:
            if not args.username:
                args.username = input("Enter username: ")
            if not args.password:
                args.password = getpass("Enter password: ")

            response = login(args.username, args.password)
            if response['success']: 
                print(f"Login successful: {response['message']}")  
                try:
                    with open('session_data.json', 'r') as f:
                        session_data = json.load(f)
                    client_id = session_data['client_id']
                    client_info = get_client(client_id)
                    if client_info.get('success'):
                        client = client_info['data']
                        name = client['name']
                    print(f"Welcome, {name}!")
                except Exception as e:
                    print(f"Error loading client data: {str(e)}")

                while True:
                    show_menu()
                    option = input("Choose an option: ")
                    if option == "1": # Menu option 1 - Logout and exit
                        response = logout()
                        json_response = response.json()
                        if json_response['success']:  
                            print(f"Logout successful: {json_response['message']}")  
                        else:
                            print(f"Logout failed: {json_response['message']}")
                        args.username = None
                        args.password = None

                    elif option == "2": # Menu option 2 - New client
                        print("New user option selected.")
                        name = input("Enter name: ")
                        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
                        address = input("Enter address: ")
                        phone_number = input("Enter phone number: ")
                        email = input("Enter email: ")
                        password = input("Enter password: ")
                        notes = input("Enter notes: ")
                        response = add_client(name, birthdate, address, phone_number, email, password, notes)

                    elif option == "3": # Menu option 3 - Add test data to database
                        print("Add test users option selected.")
                        generate_test_database(args.username, args.password)
                        
                    elif option == "4": # Menu option 4 - Initialise Database
                        print("Not implemented yet, exiting...")
                        break
                    elif option == "5": # Menu option 5 - Promote to Admin
                        print("Not implemented yet, exiting...")
                        break
                    elif option == "6": # Menu option 6 - Demote from Admin
                        print("Not implemented yet, exiting...")
                        break
                    elif option == "7": # Menu option 7 - Delete user
                        print("Not implemented yet, exiting...")
                        break
                    else:
                        print("Invalid option. Please try again.")
                break
            else:
                print(f"Login failed: {response['message']}. Please try again.")
                args.username = None
                args.password = None
    elif args.command == 'login':
        if not args.username or not args.password:
            print("Username and password are required for login.")
            sys.exit(1)
        response = login(args.username, args.password)
        if response['success']:
            print(f"Login successful: {response['message']}")
        else:
            print(f"Login failed: {response['message']}. Please try again.")
    elif args.command == 'logout':
        response = logout()
        if response['success']:
            print(f"Logout successful: {response['message']}")
        else:
            print(f"Logout failed: {response['message']}")
    else:
        print("Invalid command. Use 'login' or 'logout'.")

if __name__ == "__main__":
    main()