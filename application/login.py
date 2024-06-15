# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Login Page

import tkinter as tk
from tkinter import messagebox
import customtkinter
import os
import json
import requests
from connection import authenticate_client, hash_password
from config import CONFIG
import configparser, sys


#################
### Functions ###
#################

def login():
    """Authenticate the client and open the dashboard if successful."""
    client_id = entry_username.get() if entry_username.get() else CONFIG["client"]["default_id"]
    client_password = entry_password.get() if entry_password.get() else CONFIG["client"]["default_password"]
    client_hash = hash_password(client_password)  # Hash the password on the client-side
    try:
        response = authenticate_client(client_id, client_hash)  # Authenticate the client
        json_response = response.json()  # Convert the response content to JSON
        if response.status_code == 200 and json_response.get("success"):  # If the authentication is successful, open the dashboard
            session_data = {
                'session_cookie': response.cookies.get_dict(),
                'client_id': client_id
            }
            with open('session_data.json', 'w') as f:  # Save the session data to a file
                json.dump(session_data, f)
            root.destroy()
            os.system("python dashboard.py")
        elif response.status_code == 401:
                messagebox.showerror("Login failed", "Invalid client ID or password.")
        else:
                messagebox.showerror("Login failed", json_response.get("message", "Unknown error"))
    except requests.exceptions.HTTPError:
        messagebox.showerror("Login failed", "Invalid client ID or password.")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", f"Could not connect to the server on {CONFIG['server']['url']}")

def change_dark_theme():
    """Change the theme between dark and light."""
    config = configparser.ConfigParser()
    config.read('app.ini')
    if 'preferences' in config:
        current_theme = config.get('preferences', 'dark_theme')
        new_theme = 'light' if current_theme == 'dark' else 'dark'
        config.set('preferences', 'dark_theme', new_theme)
        with open('app.ini', 'w') as configfile:
            config.write(configfile)
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        messagebox.showerror("Error", "Could not change the theme. Please check the configuration file.")

##############
### Layout ###
##############

# Set appearance mode based on configuration
if "preferences" in CONFIG and "dark_theme" in CONFIG["preferences"]:
    if CONFIG["preferences"]["dark_theme"] == "dark":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")
else:
    customtkinter.set_appearance_mode("dark")

# Initialize the main window
root = customtkinter.CTk()
root.title("Luxbank Login")
root.iconbitmap("luxbank.ico")
root.geometry("400x300")

# Create and pack the label for the title
label = customtkinter.CTkLabel(root, text="Luxbank", font=("Helvetica", 24))
label.pack(pady=20)

# Create and pack the username entry
entry_username = customtkinter.CTkEntry(root, placeholder_text="Client ID")
entry_username.pack(pady=20)

# Create and pack the password entry
entry_password = customtkinter.CTkEntry(root, placeholder_text="Password", show="*")
entry_password.pack(pady=10)

# Create and pack the login button
login_button = customtkinter.CTkButton(root, text="Login", command=login)
login_button.pack(pady=15)

# Create and pack the theme change button
theme_button = customtkinter.CTkButton(root, text="Change Theme", command=change_dark_theme)
theme_button.pack(side='bottom', anchor='w')

# Bind the Return key to the login function
root.bind('<Return>', lambda event=None: login())

###########
### Run ###
###########

# Start the main event loop
root.mainloop()
