import customtkinter as ctk
from tkinter import messagebox, Toplevel, Label
import pygame
from PIL import Image, ImageTk
import os

# Ρύθμιση εμφάνισης
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TrivialGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivial")
        self.root.geometry("900x650")

        # Ρυθμίσεις ήχου
        pygame.mixer.init()
        self.sound_enabled = True
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        
        # Φόρτωση μουσικής
        self.load_background_music("444.mid")
        
        self.create_frames()
        self.show_welcome_screen()
    
    def load_background_music(self, music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  
             
    def create_frames(self):
        # Δημιουργία frames
        self.welcome_frame = ctk.CTkFrame(self.root)
        self.main_menu_frame = ctk.CTkFrame(self.root)
        self.settings_frame = ctk.CTkFrame(self.root)
        self.leaderboard_frame = ctk.CTkFrame(self.root)
        self.credits_frame = ctk.CTkFrame(self.root)
        self.game_frame = ctk.CTkFrame(self.root)
        self.game_settings_frame = ctk.CTkFrame(self.root)
        self.top_ten_frame = ctk.CTkFrame(self.root)
        self.player1_frame = ctk.CTkFrame(self.root)
        self.player2_frame = ctk.CTkFrame(self.root)
        self.player3_frame = ctk.CTkFrame(self.root)
        self.player4_frame = ctk.CTkFrame(self.root)
        self.players_frame = ctk.CTkFrame(self.root)

          # Welcome frame     
        try:
            # Φόρτωση εικόνας φόντου
            bg_image = Image.open("555.jpg")
            bg_image = bg_image.resize((900, 650), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.welcome_frame, image=bg_photo)
            bg_label.image = bg_photo 
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            
            welcome_label = ctk.CTkLabel(
                self.welcome_frame,
                text="Welcome stranger, introduce yourself!",
                font=("Arial", 24, "bold"),
                text_color="white",
            )
            welcome_label.place(relx=0.502, rely=0.402, anchor="center") 
            
            # Ετικέτα "Enter your name" 
            name_label = ctk.CTkLabel(
                self.welcome_frame,
                text="Enter your name:",
                text_color="white",
            )
            name_label.place(relx=0.502, rely=0.502, anchor="center")
            
            # Πεδίο εισαγωγής ονόματος
            self.name_entry = ctk.CTkEntry(self.welcome_frame, width=200)
            self.name_entry.place(relx=0.5, rely=0.55, anchor="center")
            
            # Κουμπί "Continue"
            continue_btn = ctk.CTkButton(
                self.welcome_frame,
                text="Continue",
                command=self.show_main_menu
            )
            continue_btn.place(relx=0.5, rely=0.65, anchor="center")
            
        except Exception as e:
            print(f"Σφάλμα φόρτωσης εικόνας: {e}")

        
        # Main menu frame 
        self.menu_title = ctk.CTkLabel(self.main_menu_frame, text="Main Menu", font=("Arial", 18))
        self.menu_title.pack(pady=20)
        
        button_options = {"width": 200, "height": 40, "corner_radius": 10}
        ctk.CTkButton(self.main_menu_frame, text="Play", command=self.show_players_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_menu_frame, text="Leaderboard", command=self.show_leaderboard, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_menu_frame, text="Settings", command=self.show_settings_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_menu_frame, text="Credits", command=self.show_credits_frame, **button_options).pack(pady=10)

        #players frame
        self.players_title = ctk.CTkLabel(self.players_frame, text="How many players will play?", font=("Arial", 22))
        self.players_title.pack(pady=20)
        
        button_options = {"width": 200, "height": 40, "corner_radius": 10}
        ctk.CTkButton(self.players_frame, text="1 Player", command=self.show_player1_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.players_frame, text="2 Players", command=self.show_player2_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.players_frame, text="3 Players", command=self.show_player3_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.players_frame, text="4 Players ", command=self.show_player4_frame, **button_options).pack(pady=10)
        ctk.CTkButton(self.players_frame, text="Back", command=self.show_main_menu).pack(pady=30) 

        #player1 frame
        ctk.CTkLabel(self.player1_frame, text="Player 1 would you like to keep your name, or create a new one?", font=("Arial", 16, "bold")).pack(pady=20)
        ctk.CTkLabel(self.player1_frame, text="Enter new name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player1_frame, width=200)
        self.name_entry.pack(pady=10)

        ctk.CTkButton(self.player1_frame, text="Continue", command=self.show_game_settings_frame).pack(pady=20)
        ctk.CTkButton(self.player1_frame, text="Back", command=self.show_players_frame).pack(pady=20)

        #player2 frame
        ctk.CTkLabel(self.player2_frame, text="2 Players", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.player2_frame, text="Player 1 would you like to keep your name, or enter new name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player2_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player2_frame, text="Player 2 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player2_frame, width=200)
        self.name_entry.pack(pady=10)

        ctk.CTkButton(self.player2_frame, text="Continue", command=self.show_game_settings_frame).pack(pady=20)
        ctk.CTkButton(self.player2_frame, text="Back", command=self.show_players_frame).pack(pady=20)

        #player3 frame
        ctk.CTkLabel(self.player3_frame, text="3 Players", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.player3_frame, text="Player 1 would you like to keep your name, or enter new name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player3_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player3_frame, text="Player 2 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player3_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player3_frame, text="Player 3 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player3_frame, width=200)
        self.name_entry.pack(pady=10)

        ctk.CTkButton(self.player3_frame, text="Continue", command=self.show_game_settings_frame).pack(pady=20)
        ctk.CTkButton(self.player3_frame, text="Back", command=self.show_players_frame).pack(pady=20)

        #player4 frame
        ctk.CTkLabel(self.player4_frame, text="3 Players", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.player4_frame, text="Player 1 would you like to keep your name, or enter new name", font=("Arial", 16, "bold")).pack(pady=15)
        self.name_entry = ctk.CTkEntry(self.player4_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player4_frame, text="Player 2 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player4_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player4_frame, text="Player 3 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player4_frame, width=200)
        self.name_entry.pack(pady=10)
        ctk.CTkLabel(self.player4_frame, text="Player 4 enter your name", font=("Arial", 16, "bold")).pack(pady=20)
        self.name_entry = ctk.CTkEntry(self.player4_frame, width=200)
        self.name_entry.pack(pady=10)

        ctk.CTkButton(self.player4_frame, text="Continue", command=self.show_game_settings_frame).pack(pady=20)
        ctk.CTkButton(self.player4_frame, text="Back", command=self.show_players_frame).pack(pady=10)
       
        # Game Settings frame 
        ctk.CTkLabel(self.game_settings_frame, text="Game Settings", font=("Arial", 18)).pack(pady=20)

        # Difficulty 
        ctk.CTkLabel(self.game_settings_frame, text="Select Difficulty:").pack()
        self.difficulty_var = ctk.StringVar(value="easy")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        for text, mode in difficulties:
            ctk.CTkRadioButton(self.game_settings_frame, text=text, variable=self.difficulty_var, value=mode).pack()

        # Category 
        ctk.CTkLabel(self.game_settings_frame, text="Select Category:").pack(pady=(10, 0))
        self.category_var = ctk.StringVar()
        self.category_dropdown = ctk.CTkComboBox(self.game_settings_frame, variable=self.category_var, 
                                              values=["General Knowledge", "Science", "History"])
        self.category_dropdown.pack()

        # Number of questions 
        ctk.CTkLabel(self.game_settings_frame, text="Number of Questions:", font=("Arial", 12)).pack(pady=(15, 5))
        self.questions_var = ctk.StringVar(value="10")
        questions_frame = ctk.CTkFrame(self.game_settings_frame)
        questions_frame.pack()
        question_options = ["5", "9", "10", "15"]
        for i, num in enumerate(question_options):
            btn = ctk.CTkRadioButton(questions_frame, text=num, variable=self.questions_var, value=num)
            btn.grid(row=0, column=i, padx=5)

        # Time limit 
        ctk.CTkLabel(self.game_settings_frame, text="Time Limit (seconds):", font=("Arial", 12)).pack(pady=(15, 5))
        self.time_var = ctk.StringVar(value="120")
        time_frame = ctk.CTkFrame(self.game_settings_frame)
        time_frame.pack()
        time_options = ["60", "90", "120", "150", "180"]
        for i, time in enumerate(time_options):
            btn = ctk.CTkRadioButton(time_frame, text=time, variable=self.time_var, value=time)
            btn.grid(row=0, column=i, padx=5)

        ctk.CTkButton(self.game_settings_frame, text="Start Game", command=self.show_top_ten_frame).pack(pady=20)
        ctk.CTkButton(self.game_settings_frame, text="Back", command=self.show_players_frame).pack()
        
        # Top Ten frame 
        ctk.CTkLabel(self.top_ten_frame, text="Top Ten", font=("Arial", 24)).pack(pady=20)
        self.top_ten_frame_text = ctk.CTkTextbox(self.top_ten_frame, height=200, width=400)
        self.top_ten_frame_text.insert("1.0", "1. Wonder Woman: 1000\n2. Spiderman: 800\n3. Batman: 600\n4. Spiderman: 500")
        self.top_ten_frame_text.pack(pady=10)

        ctk.CTkButton(self.top_ten_frame, text="Start Game", command=self.show_game_frame).pack(pady=20)
        ctk.CTkButton(self.top_ten_frame, text="Back ", command=self.show_game_settings_frame).pack()
        
        # Credits frame 
        ctk.CTkLabel(self.credits_frame, text="Credits", font=("Arial", 18)).pack(pady=20)
        ctk.CTkLabel(self.credits_frame, text="Trivial Game\n"
        "Διαχείριση API και Ερωτήσεων: Batman\n"
        "Λογική Παιχνιδιού και Χρονόμετρο: Superman\n"
        "Γραφικό Περιβάλλον (Tkinter): Spiderman\n"
        "Διαχείριση Βαθμολογιών & Επιπλέον Λειτουργιών: Wonder Woman\n\n"
        "Έτος: 2025").pack()

        ctk.CTkButton(self.credits_frame, text="Back to Menu", command=self.show_main_menu).pack(pady=20)
        
        # Sound Settings 
        ctk.CTkLabel(self.settings_frame, text="Sound Settings", font=("Arial", 20)).pack(pady=20)
        
        # Sound toggle
        self.sound_toggle = ctk.CTkSwitch(self.settings_frame, 
                                        text="Sound On/Off",
                                        command=self.toggle_sound)
        self.sound_toggle.pack(pady=10)
        self.sound_toggle.select() if self.sound_enabled else self.sound_toggle.deselect()
        
        # Volume slider
        ctk.CTkLabel(self.settings_frame, text="Volume:").pack()
        self.volume_slider = ctk.CTkSlider(self.settings_frame, 
                                         from_=0, to=100,
                                         command=self.update_volume)
        self.volume_slider.set(self.volume * 100)
        self.volume_slider.pack(pady=10)
        
        ctk.CTkButton(self.settings_frame, text="Back", command=self.show_main_menu).pack(pady=20)

        # Leaderboard frame 
        ctk.CTkLabel(self.leaderboard_frame, text="High Scores", font=("Arial", 18)).pack(pady=20)
        self.leaderboard_text = ctk.CTkTextbox(self.leaderboard_frame, height=200, width=400)
        self.leaderboard_text.insert("1.0", "1. Wonder Woman: 1000\n2. Spiderman: 800\n3. Batman: 600\n4. Spiderman: 500")
        self.leaderboard_text.pack(pady=10)
        ctk.CTkButton(self.leaderboard_frame, text="Back to Menu", command=self.show_main_menu).pack()
        
        # Game frame 
        self.time_label = ctk.CTkLabel(self.game_frame, text="Time left: 180", font=("Arial", 12))
        self.time_label.pack(pady=10)
        
        self.question_label = ctk.CTkLabel(self.game_frame, 
                                         text="Τι μπορεί να επηρεάσει αρνητικά το project;", 
                                         font=("Arial", 16, "bold"))
        self.question_label.pack(pady=20, padx=20)
        self.answers_frame = ctk.CTkFrame(self.game_frame)
        self.answers_frame.pack(pady=10)
        self.answer_var = ctk.StringVar()
        answers = ["Ανάδρομος Ερμής", "Πανσέληνος ", "Επίθεση εξωγήινων ", "Καλή επιτυχία από Μητσοτάκη"]
        self.answer_btn1 = ctk.CTkButton(self.answers_frame, text=answers[0], width=200,
                                        command=lambda: self.answer_var.set(answers[0]))
        self.answer_btn1.grid(row=0, column=0, padx=20, pady=10)
        
        self.answer_btn2 = ctk.CTkButton(self.answers_frame, text=answers[1], width=200,
                                        command=lambda: self.answer_var.set(answers[1]))
        self.answer_btn2.grid(row=1, column=0, padx=20, pady=10)
        self.answer_btn3 = ctk.CTkButton(self.answers_frame, text=answers[2], width=200,
                                        command=lambda: self.answer_var.set(answers[2]))
        self.answer_btn3.grid(row=0, column=1, padx=20, pady=10)
        
        self.answer_btn4 = ctk.CTkButton(self.answers_frame, text=answers[3], width=200,
                                        command=lambda: self.answer_var.set(answers[3]))
        self.answer_btn4.grid(row=1, column=1, padx=20, pady=10)
        
        # Buttons First,Previous,Next,Submit
        self.nav_frame = ctk.CTkFrame(self.game_frame)
        self.nav_frame.pack(pady=20)
        self.first_btn = ctk.CTkButton(self.nav_frame, text="First", width=100)
        self.first_btn.grid(row=0, column=0, padx=5)
        
        self.prev_btn = ctk.CTkButton(self.nav_frame, text="Previous", width=100)
        self.prev_btn.grid(row=0, column=1, padx=5)
        
        self.next_btn = ctk.CTkButton(self.nav_frame, text="Next", width=100)
        self.next_btn.grid(row=0, column=2, padx=5)
        
        self.submit_btn = ctk.CTkButton(self.nav_frame, text="Submit Answers", 
                                       command=self.show_leaderboard, width=120)
        self.submit_btn.grid(row=0, column=3, padx=5)
    
    def show_welcome_screen(self):
        self.hide_all_frames()
        self.welcome_frame.pack(fill="both", expand=True)
    
    def show_main_menu(self):
        self.hide_all_frames()
        self.main_menu_frame.pack(fill="both", expand=True)

    def show_settings_frame(self):
        self.hide_all_frames()
        self.settings_frame.pack(fill="both", expand=True)
    
    def show_game_settings_frame(self):
        self.hide_all_frames()
        self.game_settings_frame.pack(fill="both", expand=True)
    
    def show_leaderboard(self):
        self.hide_all_frames()
        self.leaderboard_frame.pack(fill="both", expand=True)
    
    def show_credits_frame(self):
        self.hide_all_frames()
        self.credits_frame.pack(fill="both", expand=True)
        
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        pygame.mixer.music.set_volume(self.volume if self.sound_enabled else 0)
    
    def update_volume(self, value):
        self.volume = float(value) / 100
        pygame.mixer.music.set_volume(self.volume)

    def show_players_frame(self):
        self.hide_all_frames()
        self.players_frame.pack(fill="both", expand=True)       

    def show_player1_frame(self):
        self.hide_all_frames()
        self.player1_frame.pack(fill="both", expand=True)   

    def show_player2_frame(self):
        self.hide_all_frames()
        self.player2_frame.pack(fill="both", expand=True)    

    def show_player3_frame(self):
        self.hide_all_frames()
        self.player3_frame.pack(fill="both", expand=True)     

    def show_player4_frame(self):
        self.hide_all_frames()
        self.player4_frame.pack(fill="both", expand=True) 

    def show_top_ten_frame(self):
        self.hide_all_frames()
        self.top_ten_frame.pack(fill="both", expand=True)    
    
    def show_game_frame(self):
        self.hide_all_frames()
        self.game_frame.pack(fill="both", expand=True)
  
 # αναπαραγωγή gif
        messagebox.showinfo("Emergency Alert", "Γενική Γραμματεία Πολιτικής Προστασίας.")
        self.play_gif("123.gif")

        selected_time = self.time_var.get()
        self.time_label.configure(text=f"Time left: {selected_time}")
    
    def play_gif(self, gif_path):
        gif_window = Toplevel(self.root)
        gif_window.title("Σταμάτα δεν έφτιαξα άλλο")
        gif_window.geometry("500x400")
        gif_window.resizable(False, False)

        frames = []
        gif = Image.open(gif_path)

        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))
        except EOFError:
            pass

        label = Label(gif_window)
        label.pack()

        def update(index=0):
            if index < len(frames):
                label.configure(image=frames[index])
                gif_window.after(100, update, index + 1)
            else:
                gif_window.destroy()

        update()
        
        # Update time 
        selected_time = self.time_var.get()
        self.time_label.configure(text=f"Time left: {selected_time}")
        
    
    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.main_menu_frame, self.settings_frame, self.game_settings_frame, self.players_frame, self.player1_frame, self.player2_frame,
                      self.player3_frame,  self.player4_frame, self.leaderboard_frame, self.credits_frame, self.game_frame, self.top_ten_frame]:
            frame.pack_forget()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TrivialGameUI(root)
    root.mainloop()