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
                            Username TEXT NOT NULL,
                            AccountType TEXT,
                            Balance REAL,
                            Password TEXT NOT NULL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                            AccountNo INTEGER,
                            Type TEXT,
                            Amount REAL,
                            Date TEXT DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(AccountNo) REFERENCES accounts(AccountNo))''')
        self.conn.commit()

        # Login Frame
        self.login_frame = Frame(self.root, bg="#333333", padx=20, pady=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.login_frame, text="Account No:", fg="#ffffff", bg="#333333", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        Label(self.login_frame, text="Password:", fg="#ffffff", bg="#333333", font=("Arial", 12)).grid(row=1, column=0, pady=10)

        self.login_account_no = Entry(self.login_frame, font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")
        self.login_password = Entry(self.login_frame, show='*', font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")

        self.login_account_no.grid(row=0, column=1, padx=10, pady=5)
        self.login_password.grid(row=1, column=1, padx=10, pady=5)

        Button(self.login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=2, column=0, columnspan=2, pady=10)
        Button(self.login_frame, text="Create New Account", command=self.show_create_account, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        acc_no = self.login_account_no.get()
        pwd = self.login_password.get()

        self.cur.execute("SELECT * FROM accounts WHERE AccountNo = ? AND Password = ?", (acc_no, pwd))
        account = self.cur.fetchone()

        if account:
            self.account_no = acc_no
            self.show_main_menu()
        else:
            tkinter.messagebox.showerror("Login Failed", "Invalid Account Number or Password")

    def show_create_account(self):
        self.login_frame.place_forget()
        self.create_account_frame = Frame(self.root, bg="#282828", padx=20, pady=20)
        self.create_account_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.create_account_frame, text="Account No", fg="#ffffff", bg="#282828", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        Label(self.create_account_frame, text="Username", fg="#ffffff", bg="#282828", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        Label(self.create_account_frame, text="Account Type", fg="#ffffff", bg="#282828", font=("Arial", 12)).grid(row=2, column=0, pady=10)
        Label(self.create_account_frame, text="Initial Balance", fg="#ffffff", bg="#282828", font=("Arial", 12)).grid(row=3, column=0, pady=10)
        Label(self.create_account_frame, text="Password", fg="#ffffff", bg="#282828", font=("Arial", 12)).grid(row=4, column=0, pady=10)

        self.new_account_no = Entry(self.create_account_frame, font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")
        self.new_username = Entry(self.create_account_frame, font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")
        self.new_account_type = Entry(self.create_account_frame, font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")
        self.new_balance = Entry(self.create_account_frame, font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")
        self.new_password = Entry(self.create_account_frame, show='*', font=("Arial", 12), bd=2, relief="flat", bg="#444444", fg="#ffffff")

        self.new_account_no.grid(row=0, column=1, padx=10, pady=5)
        self.new_username.grid(row=1, column=1, padx=10, pady=5)
        self.new_account_type.grid(row=2, column=1, padx=10, pady=5)
        self.new_balance.grid(row=3, column=1, padx=10, pady=5)
        self.new_password.grid(row=4, column=1, padx=10, pady=5)

        Button(self.create_account_frame, text="Create Account", command=self.create_account, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.create_account_frame, text="Back to Login", command=self.back_to_login, bg="#f44336", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=6, column=0, columnspan=2, pady=10)

    def back_to_login(self):
        self.create_account_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def create_account(self):
        try:
            acc_no = int(self.new_account_no.get())
            user = self.new_username.get()
            acc_type = self.new_account_type.get()
            bal = float(self.new_balance.get())
            pwd = self.new_password.get()

            if user and acc_type and pwd:
                self.cur.execute("INSERT INTO accounts (AccountNo, Username, AccountType, Balance, Password) VALUES (?, ?, ?, ?, ?)",
                                 (acc_no, user, acc_type, bal, pwd))
                self.conn.commit()
                tkinter.messagebox.showinfo("Bank", "Account created successfully!")
                self.back_to_login()
            else:
                tkinter.messagebox.showerror("Bank", "Please fill in all details.")
        except ValueError:
            tkinter.messagebox.showerror("Bank", "Please enter valid numbers for Account No and Balance.")
        except sqlite3.IntegrityError:
            tkinter.messagebox.showerror("Bank", "Account number already exists.")

    def show_main_menu(self):
        self.login_frame.place_forget()

        # Adding the background image to the main menu
        self.main_menu_frame = Frame(self.root, bg="#424242", padx=20, pady=20)
        self.main_menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        bg_label = Label(self.main_menu_frame, image=self.bg_image)  # Add background image for this frame
        bg_label.place(relwidth=1, relheight=1)

        Button(self.main_menu_frame, text="Deposit", command=self.deposit, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=0, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Withdraw", command=self.withdraw, bg="#FF5722", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=1, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Check Balance", command=self.check_balance, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=2, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Transaction History", command=self.transaction_history, bg="#FFC107", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=3, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Change Password", command=self.change_password, bg="#8BC34A", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=4, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Delete Account", command=self.delete_account, bg="#F44336", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=5, column=0, pady=10, sticky="ew")
        Button(self.main_menu_frame, text="Logout", command=self.logout, bg="#607D8B", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=6, column=0, pady=10, sticky="ew")

    def deposit(self):
        amount = float(tkinter.simpledialog.askstring("Deposit", "Enter deposit amount:"))
        self.cur.execute("UPDATE accounts SET Balance = Balance + ? WHERE AccountNo = ?", (amount, self.account_no))
        self.cur.execute("INSERT INTO transactions (AccountNo, Type, Amount) VALUES (?, 'Deposit', ?)", (self.account_no, amount))
        self.conn.commit()
        tkinter.messagebox.showinfo("Bank", f"Deposited {amount} successfully!")

    def withdraw(self):
        amount = float(tkinter.simpledialog.askstring("Withdraw", "Enter withdrawal amount:"))
        self.cur.execute("SELECT Balance FROM accounts WHERE AccountNo = ?", (self.account_no,))
        balance = self.cur.fetchone()[0]
        if balance >= amount:
            self.cur.execute("UPDATE accounts SET Balance = Balance - ? WHERE AccountNo = ?", (amount, self.account_no))
            self.cur.execute("INSERT INTO transactions (AccountNo, Type, Amount) VALUES (?, 'Withdrawal', ?)", (self.account_no, amount))
            self.conn.commit()
            tkinter.messagebox.showinfo("Bank", f"Withdrew {amount} successfully!")
        else:
            tkinter.messagebox.showerror("Bank", "Insufficient funds.")

    def check_balance(self):
        self.cur.execute("SELECT Balance FROM accounts WHERE AccountNo = ?", (self.account_no,))
        balance = self.cur.fetchone()[0]
        tkinter.messagebox.showinfo("Bank", f"Current Balance: {balance}")

    def transaction_history(self):
        self.cur.execute("SELECT Type, Amount, Date FROM transactions WHERE AccountNo = ?", (self.account_no,))
        transactions = self.cur.fetchall()
        history = "\n".join([f"{t[0]} of {t[1]} on {t[2]}" for t in transactions])
        tkinter.messagebox.showinfo("Transaction History", history if transactions else "No transactions found.")

    def change_password(self):
        new_password = tkinter.simpledialog.askstring("Change Password", "Enter new password:")
        self.cur.execute("UPDATE accounts SET Password = ? WHERE AccountNo = ?", (new_password, self.account_no))
        self.conn.commit()
        tkinter.messagebox.showinfo("Bank", "Password updated successfully.")

    def delete_account(self):
        confirm = tkinter.messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
        if confirm:
            self.cur.execute("DELETE FROM accounts WHERE AccountNo = ?", (self.account_no,))
            self.conn.commit()
            tkinter.messagebox.showinfo("Bank", "Account deleted successfully.")
            self.logout()

    def logout(self):
        self.main_menu_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Initialize the GUI
root = Tk()
app = BankManagement(root)
root.mainloop()




