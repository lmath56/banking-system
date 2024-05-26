# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Dashboard Page

import tkinter as tk
from tkinter import messagebox, ttk 
import customtkinter
import json
from config import CONFIG
import os
from connection import logout_client, get_client, update_client, get_accounts, format_balance

email_entry = None
phone_entry = None
address_entry = None
frame = None

#################
### Functions ###
#################

def logout():
    response = logout_client()  # Call the logout_client function
    json_response = response.json()  # Convert the response content to JSON
    if json_response['success'] == True:
        messagebox.showinfo("Logout", "You have been logged out.")
        root.destroy()
    else:
        messagebox.showerror("Logout failed", json_response['message'])

def display_client_info():
    global frame  # Declare frame as global inside the function
    if frame is not None:
        for widget in frame.winfo_children():  # Destroy all widgets in the frame
            widget.destroy()
    else:
        frame = customtkinter.CTkFrame(root)
        frame.pack(anchor='w', side='left', padx=20, pady=20)
    with open('application\\session_data.json', 'r') as f:
        session_data = json.load(f)
    client_id = session_data['client_id']
    client_info = get_client(client_id)
    if 'success' in client_info and client_info['success']:
        client = client_info['data']
        fields = [('Name', 'name'), 
                  ('Client ID', 'client_id'), 
                  ('Email', 'email'), 
                  ('Phone', 'phone_number'), 
                  ('Address', 'address'), 
                  ('Account Opened', 'opening_timestamp')]
        for i, (display_name, key) in enumerate(fields):
            value = client.get(key, 'N/A')  # Use 'N/A' as the default value if the key is not found
            label_key = customtkinter.CTkLabel(frame, text=f"{display_name}: ", font=("Helvetica", 14))
            label_value = customtkinter.CTkLabel(frame, text=value, font=("Helvetica", 14))
            label_key.grid(row=i, column=0, sticky='e')
            label_value.grid(row=i, column=1, sticky='w')
    else:
        error_label = customtkinter.CTkLabel(root, text="Error: Could not retrieve client information", font=("Helvetica", 14))
        error_label.pack(pady=20)
    
    edit_button = customtkinter.CTkButton(frame, text="Edit Details", command=edit_details)
    edit_button.grid(row=len(fields), column=0, columnspan=2)


def edit_details():
    global edit_window, email_entry, phone_entry, address_entry  # Declare the variables as global inside the function
    edit_window = customtkinter.CTkToplevel(root)
    edit_window.title("Edit Details")
    edit_window.geometry("300x200")
    edit_window.attributes('-topmost', True)
    

    email_label = customtkinter.CTkLabel(edit_window, text="Email: ")
    email_entry = customtkinter.CTkEntry(edit_window)
    email_label.pack()
    email_entry.pack()

    phone_label = customtkinter.CTkLabel(edit_window, text="Phone: ")
    phone_entry = customtkinter.CTkEntry(edit_window)
    phone_label.pack()
    phone_entry.pack()

    address_label = customtkinter.CTkLabel(edit_window, text="Address: ")
    address_entry = customtkinter.CTkEntry(edit_window)
    address_label.pack()
    address_entry.pack()

    save_button = customtkinter.CTkButton(edit_window, text="Save", command=save_details)
    save_button.pack()
    edit_window.lift()

def save_details():
    global edit_window, email_entry, phone_entry, address_entry
    new_email = email_entry.get() if email_entry.get() != '' else None
    new_phone = phone_entry.get() if phone_entry.get() != '' else None
    new_address = address_entry.get() if address_entry.get() != '' else None
    with open('application\\session_data.json', 'r') as f:
        session_data = json.load(f)
    client_id = session_data['client_id']
    if not messagebox.askyesno("Confirmation", "Are you sure you want to update the details?"):
        return  # If the user clicked 'No', exit the function
    result = update_client(client_id, new_email, new_phone, new_address)
    if result['success']:
        display_client_info()
    edit_window.destroy() 

def populate_table():
    with open('application\\session_data.json', 'r') as f:  # Get the client_id from the session data
        session_data = json.load(f)
    client_id = session_data['client_id']
    response = get_accounts(client_id) # Get the accounts for the client
    accounts = response['data'] if 'data' in response else []
    if not isinstance(accounts, list): # Check if accounts is a list
        print(f"Error: Expected a list of accounts, but got {type(accounts)}")
        return
    for account in accounts:  # Populate the table with the accounts
        formatted_balance = format_balance(account['balance'])
        table.insert('', 'end', values=(account['description'], account['account_id'], formatted_balance, account['account_type']))

def on_account_double_click(event):
    try:
        selected_account = table.item(table.selection()) # Get the selected account
        session = json.load(open('application\\session_data.json', 'r')) # Get the session data
        account_description = selected_account['values'][0]
        os.system(f"python application\\account.py {selected_account['values'][1]} {session['client_id']} \"{account_description}\"")
    except Exception as e:
        print(f"Error: {e}")


##############
### Layout ###
##############

root = customtkinter.CTk()

root.title("Luxbank Dashboard")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x350")

if CONFIG["preferences"]["dark_theme"] == "dark": # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark") # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light") # Set the style for light mode

# Create a label for the title
welcome_label = customtkinter.CTkLabel(root, text="Welcome to the Luxbank Dashboard!", font=("Helvetica", 24))
welcome_label.pack(pady=20)

display_client_info()

logout_button = customtkinter.CTkButton(root, text="Logout", command=logout)
logout_button.pack(pady=15)

# Create a frame for the table
table_frame = ttk.Frame(root)
table_frame.pack(side='right', fill='both', expand=True)

# Create the table
table = ttk.Treeview(table_frame, columns=('Name', 'Account ID', 'Balance', 'Account Type'), show='headings')
table.heading('Name', text='Name')
table.heading('Account ID', text='Account ID')
table.heading('Balance', text='Balance')
table.heading('Account Type', text='Account Type')

# Set the column widths
table.column('Name', width=200)
table.column('Account ID', width=100)
table.column('Balance', width=100)
table.column('Account Type', width=100)

table.pack(fill='both', expand=True)

populate_table()

# Create a scrollbar for the table
scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
scrollbar.pack(side='right', fill='y')
table.configure(yscrollcommand=scrollbar.set)

table.bind("<Double-1>", on_account_double_click)

root.mainloop()