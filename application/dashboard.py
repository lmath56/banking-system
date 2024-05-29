# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Dashboard Page

from tkinter import messagebox, ttk
import customtkinter
import json
import os
from config import CONFIG
from connection import logout_client, get_client, update_client, get_accounts, format_balance, generate_otp, change_password


# Global variables
email_entry = None
phone_entry = None
address_entry = None
otp_entry = None
frame = None

fields = [('Name', 'name'), ('Client ID', 'client_id'), ('Email', 'email'), ('Phone', 'phone_number'),
          ('Address', 'address'), ('Account Opened', 'opening_timestamp')]

#################
### Functions ###
#################

def go_to_login():
    """Closes the current window and opens the login page."""
    root.destroy()
    os.system("python application/login.py")

def logout():
    """Logs out the client and redirects to the login page."""
    response = logout_client()
    json_response = response.json()
    if json_response['success']:
        messagebox.showinfo("Logout", "You have been logged out.")
        go_to_login()
    else:
        messagebox.showerror("Logout failed", json_response['message'])

def exit_application():
    """Logs out the client and exits the application."""
    response = logout_client()
    json_response = response.json()
    if json_response['success']:
        messagebox.showinfo("Logout", "You have been logged out.")
        root.quit()
    else:
        messagebox.showerror("Logout failed", json_response['message'])


def display_client_info():
    """Displays the client's information on the dashboard."""
    global frame
    if frame is not None:
        for widget in frame.winfo_children():
            widget.destroy()
    else:
        frame = customtkinter.CTkFrame(root)
        frame.grid(row=1, column=0, padx=20, pady=20)

    try:
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        client_id = session_data['client_id']
        client_info = get_client(client_id)
        if client_info.get('success'):
            client = client_info['data']
            for i, (display_name, key) in enumerate(fields):
                value = client.get(key, 'N/A')
                label_key = customtkinter.CTkLabel(frame, text=f"{display_name}: ", font=("Helvetica", 14))
                label_value = customtkinter.CTkLabel(frame, text=value, font=("Helvetica", 14), anchor='w')
                label_key.grid(row=i, column=0, sticky='e')
                label_value.grid(row=i, column=1, sticky='w')
        else:
            error_label = customtkinter.CTkLabel(root, text="Error: Could not retrieve client information", font=("Helvetica", 14))
            error_label.pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve client information: {e}")

def edit_details():
    """Opens a new window for editing client details."""
    global edit_window, email_entry, phone_entry, address_entry, otp_entry
    edit_window = customtkinter.CTkToplevel(root)
    edit_window.title("Edit Details")
    edit_window.iconbitmap("application/luxbank.ico")
    edit_window.geometry("300x350")
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

    customtkinter.CTkLabel(edit_window, text=" ").pack()  # Add space under the address box

    otp_button = customtkinter.CTkButton(edit_window, text="Get OTP Code", command=generate_otp)
    otp_button.pack()

    otp_label = customtkinter.CTkLabel(edit_window, text="OTP Code: ")
    otp_entry = customtkinter.CTkEntry(edit_window)
    otp_label.pack()
    otp_entry.pack()

    save_button = customtkinter.CTkButton(edit_window, text="Verify OTP and Save", command=change_password_save)
    save_button.pack()
    edit_window.lift()

def save_details():
    """Saves the updated client details."""
    global edit_window, otp_entry, email_entry, phone_entry, address_entry
    new_email = email_entry.get() if email_entry.get() != '' else None
    new_phone = phone_entry.get() if phone_entry.get() != '' else None
    new_address = address_entry.get() if address_entry.get() != '' else None
    otp_code = otp_entry.get()

    if not otp_code:
        messagebox.showerror("Error", "OTP code must be entered.")
        return

    with open('application\\session_data.json', 'r') as f:
        session_data = json.load(f)
    client_id = session_data['client_id']

    if not messagebox.askyesno("Confirmation", "Are you sure you want to update the details?"):
        return

    try:
        result = update_client(client_id, otp_code, new_email, new_phone, new_address)
        if result['success']:
            display_client_info()
            messagebox.showinfo("Success", "Details updated successfully.")
            edit_window.destroy()
        else:
            if result['message'] == "Invalid OTP.":
                messagebox.showerror("Error", "MFA details not correct. Please try again.")
            else:
                messagebox.showerror("Error", f"Could not update client details: {result['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not update client details: {str(e)}")

def populate_table():
    """Populates the accounts table with client accounts."""
    for row in table.get_children(): # Clear the table before populating it
        table.delete(row)
    try: 
        with open('application\\session_data.json', 'r') as f:
            session_data = json.load(f)
        client_id = session_data['client_id']
        response = get_accounts(client_id)
        accounts = response.get('data', [])
        if not isinstance(accounts, list):
            raise ValueError(f"Expected a list of accounts, but got {type(accounts)}")

        for account in accounts:
            formatted_balance = format_balance(account['balance'])
            table.insert('', 'end', values=(account['description'], account['account_id'], formatted_balance, account['account_type']))
    except Exception as e:
        messagebox.showerror("Error", f"Could not populate accounts table: {e}")

def on_account_double_click(event):
    """Handles double-click event on an account in the table."""
    try:
        selected_account = table.item(table.selection())
        session = json.load(open('application\\session_data.json', 'r'))
        account_description = selected_account['values'][0]
        command = f"python application\\account.py {selected_account['values'][1]} {session['client_id']} \"{account_description}\""
        return_code = os.system(command)
        if return_code != 0:
            print(f"Error: The command failed with return code {return_code}")
    except Exception as e:
        print(f"Error: {e}")

def reload_info_and_accounts():
    """Reloads the client information and the accounts table."""
    display_client_info()
    populate_table()

def change_password_box():
    """Opens a new window for changing the client's password."""
    global edit_window,password_entry, old_password_entry, confirm_password_entry, otp_entry
    edit_window = customtkinter.CTkToplevel(root)
    edit_window.title("Change Password")
    edit_window.iconbitmap("application/luxbank.ico")
    edit_window.geometry("300x350")
    edit_window.attributes('-topmost', True)

    old_password_label = customtkinter.CTkLabel(edit_window, text="Old Password: ")
    old_password_entry = customtkinter.CTkEntry(edit_window, show="*")
    old_password_label.pack()
    old_password_entry.pack()

    customtkinter.CTkLabel(edit_window, text=" ").pack()  # Add space under the old password box

    password_label = customtkinter.CTkLabel(edit_window, text="New Password: ")
    password_entry = customtkinter.CTkEntry(edit_window, show="*")
    password_label.pack()
    password_entry.pack()

    confirm_password_label = customtkinter.CTkLabel(edit_window, text="Confirm Password: ")
    confirm_password_entry = customtkinter.CTkEntry(edit_window, show="*")
    confirm_password_label.pack()
    confirm_password_entry.pack()

    customtkinter.CTkLabel(edit_window, text=" ").pack()  # Add space under the confirm password box

    otp_button = customtkinter.CTkButton(edit_window, text="Get OTP Code", command=generate_otp)
    otp_button.pack()

    otp_label = customtkinter.CTkLabel(edit_window, text="OTP Code: ")
    otp_entry = customtkinter.CTkEntry(edit_window)
    otp_label.pack()
    otp_entry.pack()

    save_button = customtkinter.CTkButton(edit_window, text="Verify OTP and Save", command=change_password_save)
    save_button.pack()
    edit_window.lift()

def change_password_save():
    """Saves the updated client password."""
    global edit_window, otp_entry, password_entry, old_password_entry, confirm_password_entry
    old_password = old_password_entry.get()
    new_password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    otp_code = otp_entry.get()

    if not otp_code:
        messagebox.showerror("Error", "OTP code must be entered.")
        return

    if not new_password or not confirm_password:
        messagebox.showerror("Error", "New password and confirm password must be entered.")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "New password and confirm password do not match.")
        return

    with open('application\\session_data.json', 'r') as f:
        session_data = json.load(f)
    client_id = session_data['client_id']

    if not messagebox.askyesno("Confirmation", "Are you sure you want to change the password?"):
        return

    try:
        response = change_password(client_id, old_password, new_password, otp_code)
        if response['success']:
            messagebox.showinfo("Success", "Password changed successfully.")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", f"Could not change password: {response['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not change password: {str(e)}")

##############
### Layout ###
##############

root = customtkinter.CTk()
root.title("Luxbank Dashboard")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x350")

# Set appearance mode based on configuration
customtkinter.set_appearance_mode(CONFIG["preferences"].get("dark_theme", "light"))

# Create a label for the title
welcome_label = customtkinter.CTkLabel(root, text="Welcome to the Luxbank Dashboard!", font=("Helvetica", 24))
welcome_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create a frame for buttons
button_frame = customtkinter.CTkFrame(root)
button_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=15)

# Create the OTP button
otp_button = customtkinter.CTkButton(button_frame, text="Get OTP Code", command=generate_otp)
otp_button.grid(row=0, column=0, padx=5)

# Create the reload button
reload_button = customtkinter.CTkButton(button_frame, text="Reload", command=reload_info_and_accounts)
reload_button.grid(row=0, column=1, padx=5)

# Create reset password button
password_button = customtkinter.CTkButton(button_frame, text="Reset Password", command=change_password_box)
password_button.grid(row=0, column=2, padx=5)

# Create the logout button
logout_button = customtkinter.CTkButton(button_frame, text="Logout", command=logout)
logout_button.grid(row=0, column=3, padx=5)

# Create the exit button
exit_button = customtkinter.CTkButton(button_frame, text="Exit", command=exit_application)
exit_button.grid(row=0, column=4, padx=5)

# Display client info after creating the buttons
frame = customtkinter.CTkFrame(root)
frame.grid(row=2, column=0, padx=20, pady=20, sticky='n')  # Adjusted grid placement
display_client_info()

# Create a frame for the table
table_frame = ttk.Frame(root)
table_frame.grid(row=2, column=1, sticky='nsew')  # Adjusted grid placement

# Configure the grid
root.grid_rowconfigure(2, weight=1)  # Adjusted row index
root.grid_columnconfigure(1, weight=1)


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

table.bind("<Double-1>", on_account_double_click)

root.mainloop()
