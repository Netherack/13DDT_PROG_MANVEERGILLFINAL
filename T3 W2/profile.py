import tkinter as tk
from PIL import Image, ImageTk
import sys
import subprocess

def load_image(path, w, h):
    img = Image.open(path).resize((w, h), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def style_button(btn, bg, fg, hover_bg):
    btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                  relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

def show_profile(username):
    root = tk.Tk()
    root.title("Profile")
    root.geometry("440x720")
    root.configure(bg="#e9ecef")
    root.resizable(False, False)

    # Top Navigation Bar
    topnav = tk.Frame(root, bg="#e9ecef", height=60)
    topnav.pack(side=tk.TOP, fill=tk.X)

    logo_label = tk.Label(topnav, text="👤", font=("Segoe UI Emoji", 28), bg="#e9ecef")
    logo_label.pack(side=tk.LEFT, padx=(18, 5), pady=10)
    tk.Label(topnav, text="Profile", font=("Segoe UI", 18, "bold"),
             bg="#e9ecef", fg="#22223b").pack(side=tk.LEFT, padx=5, pady=10)

    try:
        profile_icon_top = load_image("images/profileicon.png", 32, 32)
        lbl_profile = tk.Label(topnav, image=profile_icon_top, bg="#e9ecef")
        lbl_profile.image = profile_icon_top
        lbl_profile.pack(side=tk.RIGHT, padx=18, pady=10)
    except Exception as e:
        print(f"Error loading profile icon: {e}")

    # Card-like Main Content Area
    card = tk.Frame(root, bg="#fff", bd=0, highlightthickness=0)
    card.pack(pady=20, padx=30, fill="both", expand=True)
    card.pack_propagate(False)
    card.configure(width=340, height=470)

    # User info
    tk.Label(card, text="User Profile", font=("Segoe UI", 16, "bold"), bg="#fff", fg="#22223b").pack(pady=(30, 10))
    tk.Label(card, text=f"Username:", font=("Segoe UI", 12, "bold"), bg="#fff", fg="#22223b").pack(pady=(10, 2))
    tk.Label(card, text=username, font=("Segoe UI", 12), bg="#fff", fg="#495057").pack(pady=(0, 20))

    # Skill chart image
    try:
        skill_img = load_image("images/skillchart.png", 260, 180)
        lbl_skill = tk.Label(card, image=skill_img, bg="#fff")
        lbl_skill.image = skill_img
        lbl_skill.pack(pady=(10, 0))
    except Exception as e:
        tk.Label(card, text="Skill chart not available.", bg="#fff", fg="#e63946").pack(pady=(10, 0))

    # Bottom Navigation Bar
    bottom_nav = tk.Frame(root, bg="#e9ecef", height=70)
    bottom_nav.pack(side=tk.BOTTOM, fill=tk.X)

    icon_frame = tk.Frame(bottom_nav, bg="#e9ecef")
    icon_frame.pack(pady=10)

    try:
        home_icon = load_image("images/homeicon.png", 30, 30)
        label_home = tk.Label(icon_frame, image=home_icon, bg="#e9ecef")
        label_home.image = home_icon
        label_home.pack(side=tk.LEFT, padx=30)
        def go_home(event=None):
            root.destroy()
            subprocess.Popen([sys.executable, "main.py"])
        label_home.bind("<Button-1>", go_home)

        profile_icon = load_image("images/profileicon.png", 30, 30)
        label_profile = tk.Label(icon_frame, image=profile_icon, bg="#e9ecef")
        label_profile.image = profile_icon
        label_profile.pack(side=tk.LEFT, padx=30)
    except Exception as e:
        print(f"Error loading bottom icons: {e}")

    root.mainloop()
