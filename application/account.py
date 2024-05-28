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

##############
### Layout ###
##############

root = customtkinter.CTk()
root.title(f"Transactions for: {account_description}")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x400")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

welcome_label = customtkinter.CTkLabel(root, text=f"Transactions for: {account_description}", font=("Helvetica", 24))
welcome_label.pack(pady=20)

table_frame = customtkinter.CTkFrame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

transactions_table = ttk.Treeview(table_frame, columns=("Transaction ID", "Transaction Type", "Amount", "Timestamp", "Description", "Account ID", "Recipient Account ID"), show="headings")
transactions_table.pack(fill=tk.BOTH, expand=True)

for col in transactions_table["columns"]:
    transactions_table.heading(col, text=col)

# Directly populate transactions table for the given account
populate_transactions_table(transactions_table, account_id)

root.mainloop()
