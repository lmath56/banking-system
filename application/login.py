# Lucas Mathews - Fontys Student ID: 5023572
# Banking System App Login Page

from tkinter import *
import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()

root.title("Luxbank Login")
root.iconbitmap("application/luxbank.ico")
root.geometry("400x300")

label = customtkinter.CTkLabel(root, text="Luxbank", font=("Helvetica", 24))
label.pack(pady=20)

username = customtkinter.CTkEntry(root, placeholder_text="Client ID")
username.pack(pady=20)
password = customtkinter.CTkEntry(root, placeholder_text="Password", show="*")
password.pack(pady=10)

login_button= customtkinter.CTkButton(root, text="Login", command=lambda: print("Login"))
login_button.pack(pady=15)

root.mainloop()