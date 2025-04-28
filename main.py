import customtkinter as ctk
from screens.home import create_home_page
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Jira Uygulaması")
root.geometry("700x500")

create_home_page(root)

root.mainloop()
