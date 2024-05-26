# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Account Page

import tkinter as tk
from tkinter import messagebox, ttk 
import customtkinter
import json
from config import CONFIG
from connection import get_transactions, format_balance, get_account
import sys

#################
### Functions ###
#################

if len(sys.argv) > 3: # Check if the account description is provided as a command line argument
    account_description = sys.argv[3]
else:
    print("Error: Account description not provided.")

def open_account_page(account):
    account_window = tk.Toplevel()

    # Display the account details
    account_label = tk.Label(account_window, text=f"Account ID: {account['account_id']} | Account Type: {account['account_type']} | Balance: {format_balance(account['balance'])}")
    account_label.pack()

    # Create buttons for making a new transaction and editing the account details
    new_transaction_button = tk.Button(account_window, text="New Transaction", command=lambda: new_transaction(account))
    new_transaction_button.pack()

    edit_account_button = tk.Button(account_window, text="Edit Account", command=lambda: edit_account(account))
    edit_account_button.pack()
    
    transactions_frame = tk.Frame(account_window) # Create a frame for the transactions table
    transactions_frame.pack(side='bottom', fill='both', expand=True)

    # Create a table for the transactions
    transactions_table = ttk.Treeview(transactions_frame, columns=("Transaction ID", "Amount", "Date", "Description"), show="headings")
    transactions_table.heading("Transaction ID", text="Transaction ID")
    transactions_table.heading("Amount", text="Amount")
    transactions_table.heading("Date", text="Date")
    transactions_table.heading("Description", text="Description")
    transactions_table.pack(fill='both', expand=True)
    populate_transactions_table(transactions_table, account) # Populate the transactions table


def populate_transactions_table(table, account):
    with open('application\\session_data.json', 'r') as f:
        session_data = json.load(f)
    client_id = session_data['client_id']
    account_id = account['account_id']
    response = get_transactions(account_id)
    if response is None or 'data' not in response:  # Check if the response is valid
        print(f"Error: Unable to fetch transactions for account {account_id}")
        return
    transactions = response['data']
    if not isinstance(transactions, list): # Check if transactions is a list
        print(f"Error: Expected a list of transactions for account {account_id}, but got {type(transactions)}")
        return
    for transaction in transactions: # Populate the table with the transactions
        table.insert('', 'end', values=(transaction['transaction_id'], format_balance(transaction['amount']), transaction['date'], transaction['description']))
    open_account_button = tk.Button(root, text="Open Account", command=lambda: open_account_page(get_selected_account()))
    open_account_button.pack()
    def get_selected_account(): # Implement this function to return the selected account
        selected_item = table.selection()[0]  # Get the selected item
        account_id = table.item(selected_item)["values"][1]  # Get the account ID from the selected item
        return get_account(account_id)  # Fetch the account details and return them

##############
### Layout ###
##############

root = customtkinter.CTk()

root.title(account_description)
root.iconbitmap("application/luxbank.ico")
root.geometry("800x400")

if CONFIG["preferences"]["dark_theme"] == "dark": # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark") # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light") # Set the style for light mode

welcome_label = customtkinter.CTkLabel(root, text=f"Transactions for: {account_description}", font=("Helvetica", 24))
welcome_label.pack(pady=20)

frame = customtkinter.CTkFrame(root)

table = ttk.Treeview(frame, columns=("Description", "Account ID", "Balance", "Account Type"), show="headings")
table.heading("Description", text="Description")
table.heading("Account ID", text="Account ID")
table.heading("Balance", text="Balance")
table.heading("Account Type", text="Account Type")
table.pack()

table.column("Description", width=200)
table.column("Account ID", width=100)
table.column("Balance", width=100)
table.column("Account Type", width=100)

# Bind the double-click event to the table
table.bind("<Double-1>", lambda event: open_account_page(get_selected_account()))


def get_selected_account():
    selected_items = table.selection()  # Get the selected items
    if selected_items:  # Check if any items are selected
        selected_item = selected_items[0]  # Get the first selected item
        account_id = table.item(selected_item)["values"][1]  # Get the account ID from the selected item
        return get_account(account_id)  # Fetch the account details and return them
    else:
        messagebox.showinfo("No selection", "Please select an account first.")
        return None

root.mainloop()