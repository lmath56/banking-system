# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Account Page

import tkinter as tk
import sys
import os
import json
import customtkinter
from tkinter import ttk, messagebox
from config import CONFIG
from connection import get_transactions, format_balance, get_account, generate_otp, update_account

description_entry = None
notes_entry = None
otp_entry = None
notes_text = None

#################
### Functions ###
#################

if len(sys.argv) > 3:  # Check if the account description is provided as a command line argument
    account_id = sys.argv[1]
    account_description = sys.argv[3] # This is passed so that the window can be titled appropriately
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
            transaction['description'], 
            transaction['transaction_type'],
            format_balance(transaction['amount']), 
            transaction['timestamp'], 
            transaction['account_id'], 
            transaction['recipient_account_id'],
            transaction['transaction_id']
        ))

def display_account_info(account_id):
    """Display the account information for the given account ID."""
    account_info = get_account(account_id) 
    if account_info is None or 'data' not in account_info:
        messagebox.showerror("Error", "Could not fetch account details.")
        return
    account = account_info['data']
    if 'description' not in account:
        messagebox.showerror("Error", "Account description not found.")
        return
    global account_description
    account_description = account['description']
    fields = {'Account ID': account_id, 'Description': account_description, 'Balance': format_balance(account['balance']), 'Account Type': account['account_type']}
    for i, (key, value) in enumerate(fields.items()):
        label_key = customtkinter.CTkLabel(info_frame, text=f"{key}:", font=("Helvetica", 14))
        label_value = customtkinter.CTkLabel(info_frame, text=value, font=("Helvetica", 14))
        label_key.grid(row=0, column=i*2, sticky='w', padx=10)
        label_value.grid(row=0, column=i*2+1, sticky='w', padx=10)
    notes = get_account(account_id).get('data', {}).get('notes', '')
    
    print(f"Account: {account}")  # Debugging
    print(f"Account: {notes}")  # Debugging
    
    notes_text.configure(text=account.get('notes', ''))

def on_transaction_double_click(event):
    """Handles double-click event on a transaction in the table."""
    try:
        selected_transaction = transactions_table.item(transactions_table.selection()) 
        transaction_id = selected_transaction['values'][-1]
        command = f"python application\\transaction.py {transaction_id} \"{selected_transaction['values'][4]}\""
        return_code = os.system(command)
        if return_code != 0:
            print(f"Error: The command failed with return code {return_code}")
    except Exception as e:
        print(f"Error: {e}")

def add_transaction():
    """Open the add transaction dialog."""
    command = f"python application\\new_transaction.py {account_id}"
    return_code = os.system(command)
    if return_code != 0:
        print(f"Error: The command failed with return code {return_code}")

def edit_account_details():
    """Opens a new window for editing the account details."""
    global edit_window, otp_entry, description_entry, notes_entry
    edit_window = customtkinter.CTkToplevel(root)
    edit_window.title("Edit Account Details")
    edit_window.iconbitmap("application/luxbank.ico")
    edit_window.geometry("300x350")
    edit_window.attributes('-topmost', True)

    description_label = customtkinter.CTkLabel(edit_window, text="Description: ")
    description_entry = customtkinter.CTkEntry(edit_window)
    description_label.pack()
    description_entry.pack()

    
    notes_label = customtkinter.CTkLabel(edit_window, text="Notes: ")
    notes_entry = customtkinter.CTkEntry(edit_window)
    notes_label.pack()
    notes_entry.pack()

    customtkinter.CTkLabel(edit_window, text=" ").pack()  # Add space under the address box

    # Add the OTP code entry and button
    otp_button = customtkinter.CTkButton(edit_window, text="Get OTP Code", command=generate_otp)
    otp_button.pack()

    otp_label = customtkinter.CTkLabel(edit_window, text="OTP Code: ")
    otp_entry = customtkinter.CTkEntry(edit_window)
    otp_label.pack()
    otp_entry.pack()

    save_button = customtkinter.CTkButton(edit_window, text="Verify OTP and Save", command=save_details)
    save_button.pack()
    edit_window.lift()

def save_details():
    """Saves the edited account details."""
    global edit_window, otp_entry, description_entry, notes_entry, account_description
    description = description_entry.get() if description_entry.get() != '' else None
    notes = notes_entry.get() if notes_entry.get() != '' else None
    otp_code = otp_entry.get() if otp_entry.get() != '' else None

    if not otp_code:
        messagebox.showerror("Error", "OTP code must be entered.")
        return

    if not messagebox.askyesno("Confirmation", "Are you sure you want to save the changes?"):
        return
    
    try:
        result = update_account(account_id, otp_code, description, notes)
        if 'success' in result and result['success']:
            display_account_info(account_id)
            messagebox.showinfo("Success", "Account details have been updated.")
            root.title(f"Transactions for: {account_description}")  # Update the window title
            welcome_label.configure(text=f"Transactions for: {account_description}")
            edit_window.destroy()
        else:
            if result['message'] == "Invalid OTP.":
                messagebox.showerror("Error", "Invalid OTP code. Please try again.")
            else:
                messagebox.showerror("Error", f"Could not update account details: {result['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not update account details: {str(e)}")

def open_transaction_window():
    """Opens a new window for creating a new transaction."""
    try:
        session = json.load(open('application\\session_data.json', 'r'))
        command = f"python application\\new_transaction.py {session['client_id']}"                     
        return_code = os.system(command)
        if return_code != 0:
            print(f"Error: The command failed with return code {return_code}")
    except Exception as e:
        print(f"Error: {e}")

##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title(f"Transactions for: {account_description}")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x450")

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

# Create the notes label and text box
notes_label = customtkinter.CTkLabel(info_frame, text="Notes:", font=("Helvetica", 14))
notes_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
notes_text = customtkinter.CTkLabel(info_frame, height=4, width=50, wraplength=400)  # Use CTkLabel instead of CTkTextbox
notes_text.grid(row=1, column=1, padx=10, pady=5, sticky='ew')  # Add fill and expand options

# Display account information
info_frame = customtkinter.CTkFrame(root)
info_frame.pack(fill=tk.X)
display_account_info(account_id)

# Add buttons for adding a new transaction, requesting the OTP, and editing the account details
button_frame = customtkinter.CTkFrame(root)
button_frame.pack(fill=tk.X, pady=10)

add_transaction_button = customtkinter.CTkButton(button_frame, text="Add Transaction", command=add_transaction)
add_transaction_button.grid(row=0, column=0, padx=10)

request_otp_button = customtkinter.CTkButton(button_frame, text="Request OTP", command=generate_otp)
request_otp_button.grid(row=0, column=1, padx=10)

edit_account_details_button = customtkinter.CTkButton(button_frame, text="Edit Account Details", command=edit_account_details)
edit_account_details_button.grid(row=0, column=2, padx=10)

close_button = customtkinter.CTkButton(button_frame, text="Close", command=root.destroy)
close_button.grid(row=0, column=3, padx=10)

table_frame = customtkinter.CTkFrame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Create the transactions table
transactions_table = ttk.Treeview(table_frame, columns=("Description", "Transaction Type", "Amount", "Timestamp", "Sender", "Recipient"), show="headings")
transactions_table.pack(fill=tk.BOTH, expand=True)
for col in transactions_table["columns"]:
    transactions_table.heading(col, text=col)

transactions_table.column("Description", width=100)
transactions_table.column("Timestamp", width=75)
transactions_table.column("Transaction Type", width=50)
transactions_table.column("Amount", width=20)
transactions_table.column("Timestamp", width=75)
transactions_table.column("Sender", width=20)
transactions_table.column("Recipient", width=20)

populate_transactions_table(transactions_table, account_id)

transactions_table.bind("<Double-1>", on_transaction_double_click)

# Start the main event loop
root.mainloop()
