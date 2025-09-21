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
        self.root.configure(bg="#f0f0f0")
        
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
        # Title label
        title_label = tk.Label(self.root, text="Login/Signup System", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Frame for input fields
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        # Username
        tk.Label(input_frame, text="Username:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        username_entry = tk.Entry(input_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(input_frame, text="Password:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*", width=25)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        # Login button
        login_button = tk.Button(button_frame, text="Login", command=self.login, 
                                width=10, bg="#8FC1EB", fg="black")
        login_button.grid(row=0, column=0, padx=10)
        
        # Signup button
        signup_button = tk.Button(button_frame, text="Sign Up", command=self.signup, 
                                 width=10, bg="#F4F801", fg="black")
        signup_button.grid(row=0, column=1, padx=10)
        
        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, 
                               width=10, bg="#f44336", fg="black")
        exit_button.pack(pady=10)
    
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
