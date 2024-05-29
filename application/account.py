import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
from config import CONFIG
from connection import get_transactions, format_balance, get_account
import sys

#################
### Functions ###
#################

if len(sys.argv) > 3:  # Check if the account description is provided as a command line argument
    account_id = sys.argv[1]
    account_description = sys.argv[3]
else:
    messagebox.showerror("Error", "Account ID and description were not provided by the server.")
    sys.exit(1)

def populate_transactions_table(transactions_table, account_id):
    """Populate the transactions table with data for the given account ID."""
    response = get_transactions(account_id)  # Fetch the transactions for the account
    if response is None or 'data' not in response:
        messagebox.showerror("Error", "Could not fetch transactions for the account.")
        return
    transactions = response['data']
    if not isinstance(transactions, list):
        messagebox.showerror("Error", "Data is not formatted as expected.")
        return
    transactions.sort(key=lambda x: x['timestamp'], reverse=True) # Sort transactions by timestamp in descending order
    for transaction in transactions:  # Insert the transactions into the transactions_table
        transactions_table.insert('', 'end', values=(
            transaction['transaction_id'], 
            transaction['transaction_type'], 
            format_balance(transaction['amount']), 
            transaction['timestamp'], 
            transaction['description'], 
            transaction['account_id'], 
            transaction['recipient_account_id']
        ))

def display_account_info(account_id):
    """Display the account information for the given account ID."""
    account_info = get_account(account_id)  # Fetch the account details
    if account_info is None or 'data' not in account_info:
        messagebox.showerror("Error", "Could not fetch account details.")
        return
    account = account_info['data']
    print(account)
    if 'description' not in account:
        messagebox.showerror("Error", "Account description not found.")
        return
    account_description = account['description']
    fields = {'Account ID': account_id, 'Description': account_description, 'Balance': format_balance(account['balance']), 'Account Type': account['account_type']}
    for i, (key, value) in enumerate(fields.items()):
        label_key = customtkinter.CTkLabel(info_frame, text=f"{key}:", font=("Helvetica", 14))
        label_value = customtkinter.CTkLabel(info_frame, text=value, font=("Helvetica", 14))
        label_key.grid(row=0, column=i*2, sticky='w', padx=10)
        label_value.grid(row=0, column=i*2+1, sticky='w', padx=10)

##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title(f"Transactions for: {account_description}")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x400")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

# Display main window title
welcome_label = customtkinter.CTkLabel(root, text=f"Transactions for: {account_description}", font=("Helvetica", 24))
welcome_label.pack(pady=10)

# Display account information
info_frame = customtkinter.CTkFrame(root)
info_frame.pack(fill=tk.X)
display_account_info(account_id)

table_frame = customtkinter.CTkFrame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Add buttons for adding a new transaction, requesting the OTP, and editing the account details
button_frame = customtkinter.CTkFrame(root)
button_frame.pack(fill=tk.X, pady=10)
add_transaction_button = customtkinter.CTkButton(button_frame, text="Add Transaction", command=add_transaction)
add_transaction_button.grid(row=0, column=0, padx=10)
request_otp_button = customtkinter.CTkButton(button_frame, text="Request OTP", command=request_otp)
request_otp_button.grid(row=0, column=1, padx=10)
edit_account_details_button = customtkinter.CTkButton(button_frame, text="Edit Account Details", command=edit_account_details)
edit_account_details_button.grid(row=0, column=2, padx=10)

# Create the transactions table
transactions_table = ttk.Treeview(table_frame, columns=("Transaction ID", "Transaction Type", "Amount", "Timestamp", "Description", "Account ID", "Recipient Account ID"), show="headings")
transactions_table.pack(fill=tk.BOTH, expand=True)
for col in transactions_table["columns"]:
    transactions_table.heading(col, text=col)
populate_transactions_table(transactions_table, account_id)

# Start the main event loop
root.mainloop()
