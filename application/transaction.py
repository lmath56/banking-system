# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Transaction Page

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
from config import CONFIG
from connection import get_transaction, format_balance
import sys

#################
### Functions ###
#################





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
welcome_label = customtkinter.CTkLabel(root, text=f"Transactions: {transaction_description}", font=("Helvetica", 24))
welcome_label.pack(pady=10)