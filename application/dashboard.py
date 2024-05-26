# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Dashboard Page

import tkinter as tk
from tkinter import messagebox
import customtkinter


from connection import logout_client

def logout():
    response = logout_client()  # Call the logout_client function
    json_response = response.json()  # Convert the response content to JSON
    if json_response['success'] == True:
        messagebox.showinfo("Logout", "You have been logged out.")
        root.destroy()
    else:
        messagebox.showerror("Logout failed", json_response['message'])

# Create the main window
root = customtkinter.CTk()

# Set the window title, icon, and size
root.title("Luxbank Dashboard")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x600")

# Create a label with a welcome message
welcome_label = customtkinter.CTkLabel(root, text="Welcome to the Luxbank Dashboard!", font=("Helvetica", 24))
welcome_label.pack(pady=20)

# Create a Logout button
logout_button = customtkinter.CTkButton(root, text="Logout", command=logout)
logout_button.pack(pady=15)

# Start the main loop
root.mainloop()