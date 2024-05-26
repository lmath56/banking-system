# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Login Page

from tkinter import messagebox
import customtkinter
import os
import json
import requests
from connection import authenticate_client
from config import CONFIG

#################
### Functions ###
#################

def login():
    client_id = entry_username.get()
    client_password = entry_password.get()
    try:
        response = authenticate_client(client_id, client_password) # Authenticate the client
        json_response = response.json() # Convert the response content to JSON
        if json_response["success"] == True: # If the authentication is successful, open the dashboard
            session_data = {
                'session_cookie': response.cookies.get_dict(),
                'client_id': client_id
            }
            with open('application\\session_data.json', 'w') as f: # Save the session data to a file
                json.dump(session_data, f)
            root.destroy()
            os.system("python application\\dashboard.py")
        else:
            messagebox.showerror("Login failed", json_response["message"]) 
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Login failed", "Could not connect to the server. Please try again later. Error: " + str(e))

##############
### Layout ###
##############

customtkinter.set_appearance_mode((CONFIG["preferences"]["dark_theme"]))  # Modes: system (default), light, dark
customtkinter.set_default_color_theme((CONFIG["preferences"]["theme"]))  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()

root.title("Luxbank Login")
root.iconbitmap("application/luxbank.ico")
root.geometry("400x300")

label = customtkinter.CTkLabel(root, text="Luxbank", font=("Helvetica", 24))
label.pack(pady=20)

entry_username = customtkinter.CTkEntry(root, placeholder_text="Client ID")
entry_username.pack(pady=20)
entry_password = customtkinter.CTkEntry(root, placeholder_text="Password", show="*")
entry_password.pack(pady=10)

login_button= customtkinter.CTkButton(root, text="Login", command=login)
login_button.pack(pady=15)

root.bind('<Return>', lambda event=None: login())

###########
### Run ###
###########

root.mainloop()