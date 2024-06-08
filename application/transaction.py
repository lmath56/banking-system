# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Transaction Page

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
from config import CONFIG
from connection import get_transaction, format_balance
import sys

#################
### Functions ###
#################

if len(sys.argv) > 2:  # Check if the transaction ID and client ID are provided as command line arguments
    transaction_id = sys.argv[1]
    client_id = sys.argv[2]
else:
    messagebox.showerror("Error", "Transaction ID and Client ID were not provided by the server.")
    sys.exit(1)

def display_transaction_info(transaction_id):
    """Display the transaction information for the given transaction ID."""
    response = get_transaction(transaction_id)
    if response is None or 'data' not in response:
        messagebox.showerror("Error", "Could not fetch account details.")
        return
    transaction = response.get('data',)
    if "description" not in transaction:
        messagebox.showerror("Error", "Transaction descroption not found.")
        return
    fields = {'Description': transaction['description'], 'Transaction Type  ': transaction['transaction_type'], 'Amount': format_balance(transaction['amount']), 'Timestamp': transaction['timestamp'], 'Account ID': transaction['account_id'], 'Recipient ID': transaction['recipient_account_id'], "Transaction ID": transaction['transaction_id']}
    for i, (key, value) in enumerate(fields.items()):
        label = customtkinter.CTkLabel(transaction_frame, text=f"{key}:")
        label.grid(row=i, column=0, sticky="w")
        value_label = customtkinter.CTkLabel(transaction_frame, text=value)
        value_label.grid(row=i, column=1, sticky="w")


##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title("Banking System Transaction Page")
root.iconbitmap("luxbank.ico")
root.geometry("370x300")

# Create a close button at the top of the window
close_button = customtkinter.CTkButton(root, text="Close", command=root.destroy)
close_button.pack(side="top", anchor="e")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

# Display main window title
welcome_label = customtkinter.CTkLabel(root, text="Transaction Details", font=("Helvetica", 24))
welcome_label.pack(pady=10)

# Create a frame for the transaction details
transaction_frame = customtkinter.CTkFrame(root)
transaction_frame.pack(pady=10)

display_transaction_info(transaction_id)

root.mainloop()
