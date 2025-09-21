import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
from explore import show_explore
from consultation import run_consultation
import webbrowser
import sys
from profile import show_profile

# Load & resize helper
def load_image(path, width, height):
    try:
        img = Image.open(path)
        img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        # Return a blank image as fallback
        return tk.PhotoImage(width=width, height=height)

# Function to run the career test
def run_career_test():
    import sys
    import subprocess
    subprocess.Popen([sys.executable, "careertest.py"])

def style_button(btn, bg, fg, hover_bg):
    btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                  relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

def run(root=None):
    """Main function to run the application"""
    # If no root is provided, create one
    if root is None:
        root = tk.Tk()

    root.title("Career Recruiter")
    root.geometry("440x720")  # Increased size for better layout
    root.configure(bg="#e9ecef")
    root.resizable(False, False)

    # Top navigation bar
    topnav = tk.Frame(root, bg="#e9ecef", height=60)
    topnav.pack(side=tk.TOP, fill=tk.X)

    logo_label = tk.Label(topnav, text="🔎", font=("Segoe UI Emoji", 28), bg="#e9ecef")
    logo_label.pack(side=tk.LEFT, padx=(18, 5), pady=10)
    app_name = tk.Label(topnav, text="Career Recruiter", font=("Segoe UI", 18, "bold"), bg="#e9ecef", fg="#22223b")
    app_name.pack(side=tk.LEFT, padx=5, pady=10)

    try:
        profile_icon_top = load_image("images/profileicon.png", 32, 32)
        profile_label = tk.Label(topnav, image=profile_icon_top, bg="#e9ecef")
        profile_label.image = profile_icon_top
        profile_label.pack(side=tk.RIGHT, padx=18, pady=10)
    except Exception as e:
        print(f"Error loading profile icon: {e}")

    # Card-like main content area
    card = tk.Frame(root, bg="#fff", bd=0, highlightthickness=0)
    card.pack(pady=20, padx=30, fill="both", expand=True)
    card.pack_propagate(False)
    card.configure(width=340, height=470)

    # Search bar inside card
    search_frame = tk.Frame(card, bg="#fff")
    search_frame.pack(pady=(18, 10), padx=10, anchor="n")
    search_label = tk.Label(search_frame, text="Search:", bg="#fff", fg="#22223b", font=("Segoe UI", 10, "bold"))
    search_label.pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, width=28, font=("Segoe UI", 11), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
    search_entry.pack(side=tk.LEFT, padx=7, ipady=6)

    def do_search(event=None):
        query = search_entry.get().strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")

    search_entry.bind("<Return>", do_search)
    search_btn = tk.Button(search_frame, text="Go", command=do_search, width=4)
    style_button(search_btn, "#43aa8b", "#fff", "#27736b")
    search_btn.pack(side=tk.LEFT, padx=5)

    # Main label
    label = tk.Label(card, text="Welcome!", font=("Segoe UI", 18, "bold"), bg="#fff", fg="#22223b")
    label.pack(pady=(10, 6))

    # Button frame
    button_frame = tk.Frame(card, bg="#fff")
    button_frame.pack(pady=10)

    # Replace with actual username from login system if available
    username = "User"

    def open_consultation():
        root.destroy()
        run_consultation()

    def open_explore():
        root.destroy()
        show_explore()

    def open_career_test():
        root.destroy()
        run_career_test()

    def open_profile():
        root.destroy()
        show_profile(username)

    btn_consultation = tk.Button(button_frame, text="Consultation", width=13, height=2, command=open_consultation)
    style_button(btn_consultation, "#4361ee", "#fff", "#274690")
    btn_consultation.grid(row=0, column=0, padx=8, pady=8)

    btn_career = tk.Button(button_frame, text="Career Test", width=13, height=2, command=open_career_test)
    style_button(btn_career, "#f9c74f", "#22223b", "#f9844a")
    btn_career.grid(row=0, column=1, padx=8, pady=8)

    btn_explore = tk.Button(button_frame, text="Explore", width=13, height=2, command=open_explore)
    style_button(btn_explore, "#43aa8b", "#fff", "#27736b")
    btn_explore.grid(row=1, column=0, padx=8, pady=8)

    btn_settings = tk.Button(button_frame, text="Settings", width=13, height=2, command=open_profile)
    style_button(btn_settings, "#adb5bd", "#22223b", "#6c757d")
    btn_settings.grid(row=1, column=1, padx=8, pady=8)

    # Top Careers section
    label1 = tk.Label(card, text="Top Careers", font=("Segoe UI", 14, "bold"), bg="#fff", fg="#22223b")
    label1.pack(pady=(18, 6))
    top_career1 = tk.Label(card, text="Data Scientist", font=("Segoe UI", 11), bg="#fff", fg="#22223b")
    top_career1.pack(pady=3)
    top_career2 = tk.Label(card, text="Software Engineer", font=("Segoe UI", 11), bg="#fff", fg="#22223b")
    top_career2.pack(pady=3)

    # Bottom navigation bar with centered icons
    bottomnav = tk.Frame(root, bg="#e9ecef", height=70)
    bottomnav.pack(side=tk.BOTTOM, fill=tk.X)

    icon_frame = tk.Frame(bottomnav, bg="#e9ecef")
    icon_frame.pack(pady=10)

    try:
        home_icon = load_image("images/homeicon.png", 30, 30)
        label_home = tk.Label(icon_frame, image=home_icon, bg="#e9ecef")
        label_home.image = home_icon
        label_home.pack(side=tk.LEFT, padx=30)
        def go_home(event=None):
            root.destroy()
            import subprocess
            subprocess.Popen([sys.executable, "main.py"])
        label_home.bind("<Button-1>", go_home)

        profile_icon_bottom = load_image("images/profileicon.png", 30, 30)
        label_profile = tk.Label(icon_frame, image=profile_icon_bottom, bg="#e9ecef")
        label_profile.image = profile_icon_bottom
        label_profile.pack(side=tk.LEFT, padx=30)
        # Open profile page on click
        label_profile.bind("<Button-1>", lambda e: open_profile())
    except Exception as e:
        print(f"Error loading bottom icons: {e}")

    return root

if __name__ == "__main__":
    root = run()
    root.mainloop()
