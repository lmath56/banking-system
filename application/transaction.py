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

if len(sys.argv) > 3:  # Check if the transaction description is provided as a command line argument
    transaction_id = sys.argv[1]
    transaction_description = sys.argv[3]
else:
    messagebox.showerror("Error", "Transaction ID and description were not provided by the server.")
    sys.exit(1)

def display_transaction_info(transaction_id):
    """Display the transaction information for the given transaction ID."""
    response = get_transaction(transaction_id)  # Fetch the transaction details
    print(response)
    if response is None or 'data' not in response:
        messagebox.showerror("Error", "Transaction details not found.")
        return

    transaction = response.get('data', {})  # Get transaction data or empty dictionary
    if not transaction:
        messagebox.showerror("Error", "Transaction details not found.")
        return
    global transaction_description
    t_id = transaction['transaction_id']
    t_description = transaction['description']
    t_amount = format_balance(transaction['amount'])
    t_timestamp = transaction['timestamp']
    t_sender = transaction['account_id']
    t_recipient = transaction['recipient_account_id']
    t_type = transaction['transaction_type']

    # Create labels for each piece of transaction information and pack them into the transaction_frame
    id_label = customtkinter.CTkLabel(transaction_frame, text=f"Transaction ID: {t_id}")
    id_label.pack()
    description_label = customtkinter.CTkLabel(transaction_frame, text=f"Description: {t_description}")
    description_label.pack()
    amount_label = customtkinter.CTkLabel(transaction_frame, text=f"Amount: {t_amount}")
    amount_label.pack()
    timestamp_label = customtkinter.CTkLabel(transaction_frame, text=f"Timestamp: {t_timestamp}")
    timestamp_label.pack()
    sender_label = customtkinter.CTkLabel(transaction_frame, text=f"Sender: {t_sender}")
    sender_label.pack()
    recipient_label = customtkinter.CTkLabel(transaction_frame, text=f"Recipient: {t_recipient}")
    recipient_label.pack()
    type_label = customtkinter.CTkLabel(transaction_frame, text=f"Transaction Type: {t_type}")
    type_label.pack()


##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title(f"Transactions: {transaction_description}")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x400")

# Create a close button at the top of the window
close_button = customtkinter.CTkButton(root, text="Close", command=root.destroy)
close_button.pack(side="top", anchor="e")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

# Display main window title
welcome_label = customtkinter.CTkLabel(root, text=f"Transactions: {transaction_description}", font=("Helvetica", 24))
welcome_label.pack(pady=10)

# Create a frame for the transaction details
transaction_frame = customtkinter.CTkFrame(root)
transaction_frame.pack(pady=10)
display_transaction_info(transaction_id)


root.mainloop()