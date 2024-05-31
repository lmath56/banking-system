# Lucas Mathews - Fontys Student ID: 5023572
# Banking System New Transaction Page

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
from config import CONFIG
from connection import format_balance, get_account, new_transaction, generate_otp
import sys

#################
### Functions ###
#################

if len(sys.argv) > 3:  # Check if the account description is provided as a command line argument
    account_id = sys.argv[1]
    account_description = sys.argv[3] # This is passed so that the window can be titled appopriately
else:
    messagebox.showerror("Error", "Account ID and description were not provided by the server.")
    sys.exit(1)



##############
### Layout ###
##############

# Initialise the main window
root = customtkinter.CTk()
root.title(f"Transactions: {transaction_description}")
root.iconbitmap("application/luxbank.ico")
root.geometry("800x400")

if CONFIG["preferences"]["dark_theme"] == "dark":  # Check if dark mode is enabled
    customtkinter.set_appearance_mode("dark")  # Set the style for dark mode
else:
    customtkinter.set_appearance_mode("light")  # Set the style for light mode

# Display main window title
welcome_label = customtkinter.CTkLabel(root, text=f"Transactions for: {account_description}", font=("Helvetica", 24))
welcome_label.pack(pady=10)

root.mainloop()
