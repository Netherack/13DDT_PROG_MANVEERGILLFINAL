import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
from profile import show_profile

# Load & resize helper
def load_image(path, width, height):
    try:
        img = Image.open(path)
        img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return tk.PhotoImage(width=width, height=height)

def style_button(btn, bg, fg, hover_bg):
    btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                  relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

def run_consultation():
    root = tk.Tk()

    root.title("Consultation - Q&A Forum")
    root.geometry("440x720")
    root.configure(bg="#e9ecef")
    root.resizable(False, False)

    username = "User"  # Replace with actual username if available

    # --- Top Navigation Bar ---
    topnav = tk.Frame(root, bg="#e9ecef", height=60)
    topnav.pack(side=tk.TOP, fill=tk.X)

    logo_label = tk.Label(topnav, text="💬", font=("Segoe UI Emoji", 28), bg="#e9ecef")
    logo_label.pack(side=tk.LEFT, padx=(18, 5), pady=10)
    app_name = tk.Label(topnav, text="Consultation", font=("Segoe UI", 18, "bold"), bg="#e9ecef", fg="#22223b")
    app_name.pack(side=tk.LEFT, padx=5, pady=10)

    try:
        profile_icon_top = load_image("images/profileicon.png", 32, 32)
        profile_label = tk.Label(topnav, image=profile_icon_top, bg="#e9ecef")
        profile_label.image = profile_icon_top
        profile_label.pack(side=tk.RIGHT, padx=18, pady=10)
    except Exception as e:
        print(f"Error loading profile icon: {e}")

    # --- Card-like Main Content Area ---
    card = tk.Frame(root, bg="#fff", bd=0, highlightthickness=0)
    card.pack(pady=20, padx=30, fill="both", expand=True)
    card.pack_propagate(False)
    card.configure(width=340, height=470)

    # Add search bar
    search_frame = tk.Frame(card, bg="#fff")
    search_frame.pack(pady=(10, 5), padx=10, anchor="n")
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

    # --- Q&A Logic ---
    questions = []

    # Frame for adding a new question
    add_frame = tk.Frame(card, bg="#fff")
    add_frame.pack(pady=(18, 10), fill=tk.X, padx=10)

    question_entry = tk.Entry(add_frame, width=28, font=("Segoe UI", 11), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
    question_entry.pack(side=tk.LEFT, padx=5, ipady=6)

    def post_question():
        text = question_entry.get().strip()
        if text:
            q_frame = tk.LabelFrame(card, text=text, padx=10, pady=5, bg="#f8f9fa", font=("Segoe UI", 10, "bold"), fg="#22223b", relief="groove", bd=1)
            q_frame.pack(fill="x", pady=5, padx=10)

            answer_entry = tk.Entry(q_frame, width=20, font=("Segoe UI", 10), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
            answer_entry.pack(side=tk.LEFT, padx=5, ipady=4)

            answers_box = tk.Listbox(q_frame, height=2, width=18, font=("Segoe UI", 10), bg="#fff")
            answers_box.pack(side=tk.LEFT, padx=5)

            def add_answer():
                ans = answer_entry.get().strip()
                if ans:
                    answers_box.insert(tk.END, ans)
                    answer_entry.delete(0, tk.END)

            answer_btn = tk.Button(q_frame, text="Answer", width=8, height=1, command=add_answer)
            style_button(answer_btn, "#43aa8b", "#fff", "#27736b")
            answer_btn.pack(side=tk.LEFT, padx=5)

            questions.append(q_frame)
            question_entry.delete(0, tk.END)

    post_btn = tk.Button(add_frame, text="Post", width=8, height=1, command=post_question)
    style_button(post_btn, "#4361ee", "#fff", "#274690")
    post_btn.pack(side=tk.LEFT, padx=5)

    # --- Bottom Navigation Bar ---
    bottomnav = tk.Frame(root, bg="#e9ecef", height=70)
    bottomnav.pack(side=tk.BOTTOM, fill=tk.X)

    icon_frame = tk.Frame(bottomnav, bg="#e9ecef")
    icon_frame.pack(pady=10)

    try:
        home_icon = load_image("images/homeicon.png", 30, 30)
        label_home = tk.Label(icon_frame, image=home_icon, bg="#e9ecef")
        label_home.image = home_icon
        label_home.pack(side=tk.LEFT, padx=30)
        # Home button click event
        def go_home(event=None):
            root.destroy()
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "main.py"])
        label_home.bind("<Button-1>", go_home)

        profile_icon_bottom = load_image("images/profileicon.png", 30, 30)
        label_profile = tk.Label(icon_frame, image=profile_icon_bottom, bg="#e9ecef")
        label_profile.image = profile_icon_bottom
        label_profile.pack(side=tk.LEFT, padx=30)
        # Open profile page on click
        label_profile.bind("<Button-1>", lambda e: [root.destroy(), show_profile(username)])
    except Exception as e:
        print(f"Error loading bottom icons: {e}")

    return root

if __name__ == "__main__":
    root = run_consultation()
    root.mainloop()
