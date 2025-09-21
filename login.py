import tkinter as tk
from tkinter import messagebox
import os
import sys
import sqlite3

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Register")
        self.root.geometry("400x600")
        self.root.configure(bg="#e9ecef")
        self.root.resizable(False, False)

        # Variables for input fields
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Database file name
        self.db_name = "users.db"

        # Create UI elements
        self.create_widgets()

        # Initialize database
        self.initialize_database()

    def create_widgets(self):
        # Logo/Title area
        logo_frame = tk.Frame(self.root, bg="#e9ecef")
        logo_frame.pack(pady=(40, 10))
        # You can add an image here if you want
        logo_label = tk.Label(logo_frame, text="🔒", font=("Segoe UI Emoji", 40), bg="#e9ecef")
        logo_label.pack()
        title_label = tk.Label(logo_frame, text="Welcome", font=("Segoe UI", 22, "bold"), bg="#e9ecef", fg="#22223b")
        title_label.pack()

        # Card-like frame for login/signup
        card = tk.Frame(self.root, bg="#fff", bd=0, highlightthickness=0)
        card.pack(pady=10, padx=30, fill="x")
        card.pack_propagate(False)
        card.configure(width=340, height=320)

        # Frame for input fields inside card
        input_frame = tk.Frame(card, bg="#fff")
        input_frame.pack(pady=(30, 10), padx=30, fill="x")

        # Username
        tk.Label(input_frame, text="Username", bg="#fff", fg="#22223b", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 2))
        username_entry = tk.Entry(input_frame, textvariable=self.username_var, width=28, font=("Segoe UI", 11), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
        username_entry.grid(row=1, column=0, pady=(0, 15), ipady=7, sticky="ew")

        # Password
        tk.Label(input_frame, text="Password", bg="#fff", fg="#22223b", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 2))
        password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*", width=28, font=("Segoe UI", 11), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
        password_entry.grid(row=3, column=0, pady=(0, 10), ipady=7, sticky="ew")

        # Buttons frame inside card
        button_frame = tk.Frame(card, bg="#fff")
        button_frame.pack(pady=(10, 0))

        # Modern button style
        def style_button(btn, bg, fg, hover_bg):
            btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg, relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg))

        # Login button
        login_button = tk.Button(button_frame, text="Login", command=self.login, width=13)
        style_button(login_button, "#4361ee", "#fff", "#274690")
        login_button.grid(row=0, column=0, padx=5, pady=5)

        # Signup button
        signup_button = tk.Button(button_frame, text="Sign Up", command=self.signup, width=13)
        style_button(signup_button, "#f9c74f", "#22223b", "#f9844a")
        signup_button.grid(row=0, column=1, padx=5, pady=5)

        # Exit button (outside card)
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, width=13)
        style_button(exit_button, "#e63946", "#fff", "#b5171e")
        exit_button.pack(pady=(30, 0))

    def initialize_database(self):
        """Initialize SQLite database and create users table if it doesn't exist"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Create users table with correct column name
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {str(e)}")

    def user_exists(self, username):
        """Check if username already exists in database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            conn.close()
            return result is not None

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to check user: {str(e)}")
            return False

    def create_user(self, username, password):
        """Create new user in database with plain text password"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Store the plain text password directly
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                           (username, password))  # Change here

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create user: {str(e)}")
            return False

    def authenticate_user(self, username, password):
        """Authenticate user credentials with plain text password"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            conn.close()

            if result and result[0] == password:  # Change here
                return True
            return False

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to authenticate user: {str(e)}")
            return False

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        if self.authenticate_user(username, password):
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.open_main_application()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            # Clear password field for security
            self.password_var.set("")

    def signup(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Validate username
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return

        if self.user_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return

        if self.create_user(username, password):
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            # Clear fields after successful signup
            self.username_var.set("")
            self.password_var.set("")

    def open_main_application(self):
        # Close the login window
        self.root.destroy()

        # Try to run main.py
        try:
            if os.path.exists("main.py"):
                # Use subprocess to run main.py as a separate process
                import subprocess
                subprocess.Popen([sys.executable, "main.py"])
            else:
                messagebox.showerror("Error", "main.py not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open main application: {str(e)}")

def main():
    root = tk.Tk()
    app = LoginSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
