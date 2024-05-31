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
    global account_id, recipient_id
    account_id = account_combobox.get()
    recipient_id = recipient_text.get()
    amount = amount_text.get() if amount_text.get() != "" else None
    description = description_text.get() if description_text.get() != "" else None
    if not description or not amount or not recipient_id or not account_id:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    account_verification = verify_accounts(account_id, recipient_id)
    if account_verification is False:
        messagebox.showerror("Error", "Could not verify account IDs.")
        return
    response = new_transaction(account_id, description, amount, recipient_id)
    if response is None or "data" not in response:
        messagebox.showerror("Error", "Could not submit transaction.")
        return
    transaction_id = response["data"]
    otp = generate_otp(account_id, transaction_id)
    if otp is None or "data" not in otp:
        messagebox.showerror("Error", "Could not generate OTP.")
        return
    messagebox.showinfo("Success", f"Transaction submitted successfully. OTP: {otp['data']}")

def verify_accounts():
    """Verify that the account IDs are valid."""
    try:
        account = get_account(account_id)
        recipient_account = get_account(recipient_id)
        print(account)
        print(recipient_account)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to get account details: {e}")
        return False

    if account is None or recipient_account is None or "data" not in account or "data" not in recipient_account:
        messagebox.showerror("Error", "Server did not return the expected response.")
        return False
    if "account_id" not in account["data"]:
        messagebox.showerror("Error", "Account ID not found.")
        return False
    if "account_id" not in recipient_account["data"]:
        messagebox.showerror("Error", "Recipient Account ID not found.")
        return False
    #check balance
    if account["data"]["balance"] < float(amount_text.get("1.0", "end-1c")):
        messagebox.showerror("Error", "Insufficient funds.")
        return False
    submit_button.configure(state=tk.NORMAL)  # Enable the submit button if the accounts are valid
    messagebox.showinfo("Success", "Accounts verified successfully.")
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

# Create the account ID label and combobox
account_label = customtkinter.CTkLabel(root, text="Account ID:", font=("Helvetica", 14))
account_label.pack(pady=5)
account_combobox = ttk.Combobox(root, height=1, width=250)
account_combobox.pack(pady=5)

# Create the recipient ID label and text box
recipient_label = customtkinter.CTkLabel(root, text="Recipient ID:", font=("Helvetica", 14))
recipient_label.pack(pady=5)
recipient_text = customtkinter.CTkTextbox(root, height=2, width=250)
recipient_text.pack(pady=5)

# Create the verify buttons
verify_button = customtkinter.CTkButton(root, text="Verify Accounts", command=verify_accounts)
verify_button.pack(pady=10)

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
submit_button = customtkinter.CTkButton(root, text="Submit", command=submit_transaction, state=tk.DISABLED)
submit_button.pack(pady=5)

# Populate accounts combobox with the given client_id
populate_accounts(client_id)

# Display the main window
root.mainloop()
