import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

# Load & resize helper
def load_image(path, width, height):
    img = Image.open(path)
    img = img.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def style_button(btn, bg, fg, hover_bg):
    btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                  relief="flat", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

class CareerQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Pathway Quiz")
        self.root.geometry("440x720")  # Increased size for better layout
        self.root.configure(bg="#e9ecef")
        self.root.resizable(False, False)

        # Top navigation bar
        self.topnav = tk.Frame(root, bg="#e9ecef", height=60)
        self.topnav.pack(side=tk.TOP, fill=tk.X)

        logo_label = tk.Label(self.topnav, text="📝", font=("Segoe UI Emoji", 28), bg="#e9ecef")
        logo_label.pack(side=tk.LEFT, padx=(18, 5), pady=10)
        self.app_name = tk.Label(self.topnav, text="Career Quiz", font=("Segoe UI", 18, "bold"), bg="#e9ecef", fg="#22223b")
        self.app_name.pack(side=tk.LEFT, padx=5, pady=10)

        try:
            self.profile_icon_top = load_image("images/profileicon.png", 32, 32)
            self.profile_label = tk.Label(self.topnav, image=self.profile_icon_top, bg="#e9ecef")
            self.profile_label.image = self.profile_icon_top
            self.profile_label.pack(side=tk.RIGHT, padx=18, pady=10)
        except Exception as e:
            print(f"Error loading profile icon: {e}")

        # Card-like main content area
        card = tk.Frame(root, bg="#fff", bd=0, highlightthickness=0)
        card.pack(pady=20, padx=30, fill="both", expand=True)
        card.pack_propagate(False)
        card.configure(width=340, height=470)

        # Content frame inside card
        self.content_frame = tk.Frame(card, bg="#fff")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add search bar
        search_frame = tk.Frame(self.content_frame, bg="#fff")
        search_frame.pack(pady=(5, 5), padx=10, anchor="n")
        search_label = tk.Label(search_frame, text="Search:", bg="#fff", fg="#22223b", font=("Segoe UI", 10, "bold"))
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=28, font=("Segoe UI", 11), relief="flat", bg="#f5f6fa", fg="#22223b", highlightthickness=1, highlightbackground="#adb5bd", highlightcolor="#4361ee")
        self.search_entry.pack(side=tk.LEFT, padx=7, ipady=6)

        def do_search(event=None):
            query = self.search_entry.get().strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")

        self.search_entry.bind("<Return>", do_search)
        search_btn = tk.Button(search_frame, text="Go", command=do_search, width=4)
        style_button(search_btn, "#43aa8b", "#fff", "#27736b")
        search_btn.pack(side=tk.LEFT, padx=5)

        # Title
        tk.Label(self.content_frame, text="Career Pathway Quiz", 
                 font=("Segoe UI", 16, "bold"), bg="#fff", fg="#22223b").pack(pady=10)

        # Welcome message
        welcome_text = "This quiz will help suggest potential career paths based on your\nacademic interests and personal hobbies.\nFor each question, select your chosen option."
        tk.Label(self.content_frame, text=welcome_text, 
                 font=("Segoe UI", 11), bg="#fff", fg="#495057").pack(pady=6)

        # Initialize questions and options
        self.questions = [
            "Which subject do you enjoy the most?",
            "What activity do you prefer in your free time?",
            "In which environment would you prefer to work?"
        ]

        self.options = [
            ["Mathematics/Physics", "Art/Design", "Business/Economics", "Biology/Chemistry"],
            ["Solving puzzles or coding", "Creating art or music", "Leading groups or organizing events", "Experimenting or researching"],
            ["Tech company with cutting-edge technology", "Design studio or creative space", "Corporate office or business setting", "Laboratory or research facility"]
        ]

        self.answers = []
        self.current_question = 0

        # Frame for questions and options
        self.question_frame = tk.Frame(self.content_frame, bg="#fff")
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Start button
        self.start_button = tk.Button(self.content_frame, text="Start Quiz", 
                                     font=("Segoe UI", 11, "bold"), width=16)
        style_button(self.start_button, "#4361ee", "#fff", "#274690")
        self.start_button.config(command=self.show_question)
        self.start_button.pack(pady=10)

        # Result frame (initially hidden)
        self.result_frame = tk.Frame(self.content_frame, bg="#fff")

        # Bottom navigation bar with centered icons
        self.bottomnav = tk.Frame(root, bg="#e9ecef", height=70)
        self.bottomnav.pack(side=tk.BOTTOM, fill=tk.X)

        self.icon_frame = tk.Frame(self.bottomnav, bg="#e9ecef")
        self.icon_frame.pack(pady=10)

        try:
            self.home_icon = load_image("images/homeicon.png", 30, 30)
            self.label_home = tk.Label(self.icon_frame, image=self.home_icon, bg="#e9ecef")
            self.label_home.image = self.home_icon
            self.label_home.pack(side=tk.LEFT, padx=30)
            # Home button click event
            def go_home(event=None):
                self.root.destroy()
                import subprocess
                import sys
                subprocess.Popen([sys.executable, "main.py"])
            self.label_home.bind("<Button-1>", go_home)

            self.profile_icon_bottom = load_image("images/profileicon.png", 30, 30)
            self.label_profile = tk.Label(self.icon_frame, image=self.profile_icon_bottom, bg="#e9ecef")
            self.label_profile.image = self.profile_icon_bottom
            self.label_profile.pack(side=tk.LEFT, padx=30)
        except Exception as e:
            print(f"Error loading bottom icons: {e}")

    def show_question(self):
        # Clear previous content
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        if hasattr(self, 'start_button') and self.start_button.winfo_exists():
            self.start_button.destroy()

        if self.current_question < len(self.questions):
            # Display question
            question_label = tk.Label(self.question_frame, 
                                     text=self.questions[self.current_question],
                                     font=("Segoe UI", 13, "bold"), bg="#fff", fg="#22223b")
            question_label.pack(pady=10)

            # Radio buttons for options
            self.selected_option = tk.IntVar()
            self.selected_option.set(0)  # Default selection

            for i, option in enumerate(self.options[self.current_question], 1):
                rb = tk.Radiobutton(self.question_frame, text=option, 
                                   variable=self.selected_option, value=i,
                                   font=("Segoe UI", 11), bg="#fff", fg="#22223b", selectcolor="#f5f6fa", activebackground="#f5f6fa")
                rb.pack(anchor=tk.W, pady=5)

            # Next button
            next_button = tk.Button(self.question_frame, text="Next", width=12)
            style_button(next_button, "#43aa8b", "#fff", "#27736b")
            next_button.config(command=self.next_question)
            next_button.pack(pady=16)
        else:
            # Show results
            self.show_results()

    def next_question(self):
        # Validate selection
        if self.selected_option.get() == 0:
            messagebox.showwarning("Selection Required", "Please select an option before continuing.")
            return
        
        # Save answer
        self.answers.append(self.selected_option.get())
        
        # Move to next question
        self.current_question += 1
        self.show_question()
    
    def determine_career(self):
        """Determines career based on answers"""
        # Simple scoring system
        tech_score = 0
        creative_score = 0
        business_score = 0
        science_score = 0
        
        # Question 1 - Subject preference
        if self.answers[0] == 1:  # Math/Physics
            tech_score += 2
            science_score += 1
        elif self.answers[0] == 2:  # Art/Design
            creative_score += 2
        elif self.answers[0] == 3:  # Business/Economics
            business_score += 2
        elif self.answers[0] == 4:  # Biology/Chemistry
            science_score += 2
        
        # Question 2 - Activity preference
        if self.answers[1] == 1:  # Solving puzzles
            tech_score += 1
            science_score += 1
        elif self.answers[1] == 2:  # Creating art
            creative_score += 2
        elif self.answers[1] == 3:  # Leading groups
            business_score += 2
        elif self.answers[1] == 4:  # Experimenting
            science_score += 2
            tech_score += 1
        
        # Question 3 - Work environment
        if self.answers[2] == 1:  # Tech company
            tech_score += 2
        elif self.answers[2] == 2:  # Design studio
            creative_score += 2
        elif self.answers[2] == 3:  # Corporate office
            business_score += 2
        elif self.answers[2] == 4:  # Laboratory
            science_score += 2
        
        # Determine highest score
        scores = {
            "tech": tech_score,
            "creative": creative_score,
            "business": business_score,
            "science": science_score
        }
        
        career_path = max(scores, key=scores.get)
        
        # Career suggestions based on highest score
        careers = {
            "tech": ["Software Developer", "Data Scientist", "IT Specialist", "Web Developer"],
            "creative": ["Graphic Designer", "UX/UI Designer", "Content Creator", "Digital Artist"],
            "business": ["Business Analyst", "Marketing Manager", "Entrepreneur", "Financial Advisor"],
            "science": ["Research Scientist", "Medical Professional", "Environmental Scientist", "Pharmacist"]
        }
        
        return career_path, careers[career_path]
    
    def show_results(self):
        # Clear question frame
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        # Get career path and suggestions
        career_path, suggested_careers = self.determine_career()

        # Display results
        result_title = tk.Label(self.question_frame, 
                              text=f"Your Result: {career_path.upper()} FIELD",
                              font=("Segoe UI", 14, "bold"), bg="#fff", fg="#22223b")
        result_title.pack(pady=14)

        result_text = tk.Label(self.question_frame, 
                             text="Based on your responses, you might be suited for the following careers:",
                             font=("Segoe UI", 11), bg="#fff", fg="#495057")
        result_text.pack(pady=6)

        # List suggested careers
        careers_frame = tk.Frame(self.question_frame, bg="#fff")
        careers_frame.pack(pady=6)

        for i, career in enumerate(suggested_careers, 1):
            career_label = tk.Label(careers_frame, 
                                  text=f"{i}. {career}",
                                  font=("Segoe UI", 11), bg="#fff", fg="#22223b")
            career_label.pack(anchor=tk.W, pady=3)

        # Note
        note_label = tk.Label(self.question_frame, 
                            text="Remember, this is just a simple suggestion.\nFurther research and exploration is recommended!",
                            font=("Segoe UI", 10, "italic"), bg="#fff", fg="#495057")
        note_label.pack(pady=12)

        # Restart button
        restart_button = tk.Button(self.question_frame, text="Take Quiz Again", width=16)
        style_button(restart_button, "#4361ee", "#fff", "#274690")
        restart_button.config(command=self.restart_quiz)
        restart_button.pack(pady=8)

    def restart_quiz(self):
        # Reset quiz state
        self.answers = []
        self.current_question = 0
        
        # Show first question
        self.show_question()

def main():
    root = tk.Tk()
    app = CareerQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
