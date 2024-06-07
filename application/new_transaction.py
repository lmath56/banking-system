# Lucas Mathews - Fontys Student ID: 5023572
# Banking System New Transaction Page

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
from config import CONFIG
from connection import new_transaction, generate_otp, get_account, get_accounts
import sys
import requests

account_id = None
recipient_id = None

#################
### Functions ###
#################

if len(sys.argv) > 1:  # Check if the account description is provided as a command line argument
    client_id = sys.argv[1]
else:
    messagebox.showerror("Error", "Account ID and description were not provided by the server.")
    sys.exit(1)

def submit_transaction():
    """Submit a new transaction to the server."""
    amount = amount_text.get("1.0", "end").strip()
    account_id = account_combobox.get().strip()
    recipient_id = recipient_text.get("1.0", "end").strip()
    description = description_text.get("1.0", "end").strip()
    otp_code:int = otp_text.get("1.0", "end").strip()
    if not amount or not recipient_id or not account_id or not otp_code: 
        messagebox.showerror("Error", "Please fill in manditory fields.")
        return
    if verify_accounts(account_id, recipient_id, amount) is False:
        return
    if not otp_code.isdigit() or len(otp_code) != 6:
        messagebox.showerror("Error", "Please enter a valid 6-digit OTP code.")
        return    
    try: # Convert amount to float
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
        return
    try: # Convert otp code to int
        otp_code = int(otp_code)
    except ValueError:
        messagebox.showerror("Error", "Invalid OTP code entered.")
        return

    response = new_transaction(account_id, description, amount, recipient_id, otp_code)
    if response is None or "success" not in response:
        messagebox.showerror("Error", "Could not submit transaction.")
        return

    if not response['success']:  # Check if the transaction was unsuccessful
        messagebox.showerror("Error", response['message'])  # Show the error message in a popup
        return

    if response['success']:  # Check if the transaction was successful
        messagebox.showinfo("Success", "Transaction submitted successfully.")
        root.destroy()  # Close the window
        return


def verify_accounts(account_id, recipient_id, amount):
    """Verify that both account IDs are valid, and the from account has enough balance to make the transaction."""
    account = get_account(account_id)
    if account is None or "data" not in account or "balance" not in account["data"]:
        messagebox.showerror("Error", "Invalid account ID.")
        return False
    recipient = get_account(recipient_id)
    if recipient is None or "data" not in recipient:
        messagebox.showerror("Error", "Invalid recipient ID.")
        return False
    try: # Convert amount to float
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
        return False
    account_balance = account["data"]["balance"]
    if account_balance < amount:
        messagebox.showerror("Error", "Insufficient balance.")
        return False 
    return True

def populate_accounts(client_id):
    """Populate the account combobox with accounts for the given client ID."""
    accounts = get_accounts(client_id)
    if accounts is None or "data" not in accounts:
        messagebox.showerror("Error", "Could not retrieve accounts.")
        return
    account_ids = [account["account_id"] for account in accounts["data"]]
    account_combobox['values'] = account_ids

##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title("New Transaction")
root.iconbitmap("application/luxbank.ico")
root.geometry("400x600")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

# Display main window title
welcome_label = customtkinter.CTkLabel(root, text="New Transaction", font=("Helvetica", 24))
welcome_label.pack(pady=20)

# Create a close button at the top of the window
close_button = customtkinter.CTkButton(root, text="Cancel and Close", command=root.destroy)
close_button.pack(side="top", anchor="e", padx=10, pady=10)

# Create a frame for the account ID combobox
account_label = customtkinter.CTkLabel(root, text="From Account ID:", font=("Helvetica", 14))
account_label.pack(pady=5)
account_frame = ttk.Frame(root, width=200, height=25)
account_frame.pack_propagate(0)  # Don't shrink
account_frame.pack(pady=5)

# Create the account ID combobox inside the frame
account_combobox = ttk.Combobox(account_frame, height=1)
account_combobox.pack(fill='both', expand=True)

# Create the recipient ID label and text box
recipient_label = customtkinter.CTkLabel(root, text="To Recipient ID:", font=("Helvetica", 14))
recipient_label.pack(pady=5)
recipient_text = customtkinter.CTkTextbox(root, height=2, width=250)
recipient_text.pack(pady=5)

# Create the transaction description label and text box
description_label = customtkinter.CTkLabel(root, text="Description:", font=("Helvetica", 14))
description_label.pack(pady=5)
description_text = customtkinter.CTkTextbox(root, height=4, width=250)
description_text.pack(pady=5)

# Create the transaction amount label and text box
amount_label = customtkinter.CTkLabel(root, text="Amount:", font=("Helvetica", 14))
amount_label.pack(pady=5)
amount_text = customtkinter.CTkTextbox(root, height=2, width=250)
amount_text.pack(pady=5)

# Create the OTP button
otp_button = customtkinter.CTkButton(root, text="Request OTP", command=generate_otp)
otp_button.pack(pady=10)

# Create the OTP label and text box
otp_label = customtkinter.CTkLabel(root, text="OTP:", font=("Helvetica", 14))
otp_label.pack(pady=5)
otp_text = customtkinter.CTkTextbox(root, height=2, width=250)
otp_text.pack(pady=5)

# Create the submit button
submit_button = customtkinter.CTkButton(root, text="Verify & Submit", command=submit_transaction)
submit_button.pack(pady=5)

# Populate accounts combobox with the given client_id
populate_accounts(client_id)

# Display the main window
root.mainloop()
