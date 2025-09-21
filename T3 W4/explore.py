import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
from profile import show_profile

def load_image(path, w, h):
    img = Image.open(path).resize((w, h), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def style_button(btn, bg, fg, hover_bg):
    btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                  relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

def show_explore(card_width=340, card_height=470, parent=None):
    # Only use Toplevel if parent is a Toplevel/Tk, otherwise use Tk
    if parent is not None:
        parent.destroy()
        win = tk.Tk()
    else:
        win = tk.Tk()
    win.title("Explore Careers")
    win.geometry("440x720")  # Increased size for better layout
    win.configure(bg="#e9ecef")
    win.resizable(False, False)

    # --- Top Navigation Bar ---
    topnav = tk.Frame(win, bg="#e9ecef", height=60)
    topnav.pack(side=tk.TOP, fill=tk.X)

    logo_label = tk.Label(topnav, text="🌐", font=("Segoe UI Emoji", 28), bg="#e9ecef")
    logo_label.pack(side=tk.LEFT, padx=(18, 5), pady=10)
    tk.Label(topnav, text="Explore", font=("Segoe UI", 18, "bold"),
             bg="#e9ecef", fg="#22223b").pack(side=tk.LEFT, padx=5, pady=10)

    import logging
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

    try:
        profile_icon_top = load_image("images/profileicon.png", 32, 32)
        lbl_profile = tk.Label(topnav, image=profile_icon_top, bg="#e9ecef")
        lbl_profile.image = profile_icon_top
        lbl_profile.pack(side=tk.RIGHT, padx=18, pady=10)
    except Exception as e:
        logging.error(f"Failed to load top navigation profile icon from 'images/profileicon.png': {e}")

    # --- Card-like Main Content Area ---
    card = tk.Frame(win, bg="#fff", bd=0, highlightthickness=0)
    card.pack(pady=20, padx=30, fill="both", expand=True)
    card.pack_propagate(False)
    card.configure(width=card_width, height=card_height)

    # --- Scrollable job list using Canvas ---
    canvas = tk.Canvas(card, bg="#fff", highlightthickness=0, width=card_width, height=card_height-60)
    scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#fff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add search bar (not inside scrollable area)
    search_frame = tk.Frame(card, bg="#fff")
    search_frame.place(x=0, y=0, relwidth=1)
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

    # Add title and jobs to scrollable_frame
    tk.Label(scrollable_frame, text="Explore Jobs",
             font=("Segoe UI", 16, "bold"), bg="#fff", fg="#22223b").pack(pady=10)

    jobs = [
        {"title": "Data Scientist",    "company": "Acme Corp",  "location": "New York, NY"},
        {"title": "Software Engineer", "company": "Globex Inc", "location": "San Francisco, CA"},
        {"title": "Product Manager",   "company": "Initech",    "location": "Austin, TX"},
        {"title": "UX Designer",      "company": "Soylent Corp", "location": "Seattle, WA"},
        {"title": "Data Analyst",     "company": "Wayne Enterprises", "location": "Gotham City, NY"},
        {"title": "DevOps Engineer",  "company": "LexCorp", "location": "Metropolis, IL"},
        {"title": "AI Researcher", "company": "Stark Industries", "location": "Malibu, CA"},
        {"title": "Cybersecurity Analyst", "company": "Oscorp", "location": "New York, NY"},
        {"title": "Cloud Architect", "company": "Umbrella Corp", "location": "Raccoon City"},
        {"title": "Mobile Developer", "company": "Pied Piper", "location": "Silicon Valley"},
    ]

    for job in jobs:
        frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="flat", padx=8, pady=6, highlightbackground='#adb5bd', highlightthickness=1)
        frame.pack(fill="x", pady=6, padx=10)
        tk.Label(frame, text=job["title"],
                 font=("Segoe UI", 13, "bold"), bg="#f8f9fa", fg="#22223b").pack(anchor="w")
        tk.Label(frame, text=f"{job['company']} – {job['location']}", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w")

    # --- Bottom Navigation Bar ---
    bottom_nav = tk.Frame(win, bg="#e9ecef", height=70)
    bottom_nav.pack(side=tk.BOTTOM, fill=tk.X)

    icon_frame = tk.Frame(bottom_nav, bg="#e9ecef")
    icon_frame.pack(pady=10)

    try:
        home_icon = load_image("images/homeicon.png", 30, 30)
        label_home = tk.Label(icon_frame, image=home_icon, bg="#e9ecef")
        label_home.image = home_icon
        label_home.pack(side=tk.LEFT, padx=30)
        # Home button click event
        def go_home(event=None):
            win.destroy()
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "main.py"])
        label_home.bind("<Button-1>", go_home)

        profile_icon = load_image("images/profileicon.png", 30, 30)
        label_profile = tk.Label(icon_frame, image=profile_icon, bg="#e9ecef")
        label_profile.image = profile_icon
        label_profile.pack(side=tk.LEFT, padx=30)
        # Open profile page on click
        username = "User"  # Replace with actual username if available
        label_profile.bind("<Button-1>", lambda e: [win.destroy(), show_profile(username)])
    except Exception as e:
        logging.error(f"Failed to load bottom navigation icons from 'images/homeicon.png' or 'images/profileicon.png': {e}")
