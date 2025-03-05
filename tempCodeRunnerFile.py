from tkinter import *
import tkinter.messagebox
import sqlite3

class BankManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")  # Dark background for the whole window

        # Add background image for the root window (login and main menu)
        self.bg_image = PhotoImage(file="bank_PNG22.png")  # Update with your image file path
        self.bg_label = Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Database connection
        self.conn = sqlite3.connect("bank_management.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            AccountNo INTEGER PRIMARY KEY,