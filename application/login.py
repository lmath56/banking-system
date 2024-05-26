# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Login Page

from tkinter import messagebox
import customtkinter
import os
import json
from connection import *

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
                # Save the session cookie to a file
            with open('application\\session_cookie.json', 'w') as f:
                json.dump(response.cookies.get_dict(), f)
            root.destroy()
            os.system("python application\\dashboard.py")
        else:
            messagebox.showerror("Login failed", json_response["message"]) # If the authentication fails, show an error message
    except requests.exceptions.RequestException as e:
        # If a RequestException is raised, show an error message that includes the exception message
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

###########
### Run ###
###########

root.mainloop()