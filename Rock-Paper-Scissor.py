import tkinter as tk
from PIL import Image, ImageTk
import random

class RockPaperScissorsGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Rock-Paper-Scissors Game")
        self.window.geometry("600x400")
        self.window.configure(bg="pink")
        self.window.resizable(False, False)

        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0

        # Title label
        self.title_label = tk.Label(window, text="Rock Paper Scissors Game", font=("Forte", 20), fg="Dark blue",
                                    bg="pink")
        self.title_label.pack(pady=10)

        # Button frame
        self.button_frame = tk.Frame(window, bg="pink")  
        self.button_frame.pack(pady=5)

        # Load images
        self.rock_image = Image.open("rock.png").resize((100, 100), resample=Image.BICUBIC)
        self.rock_photo = ImageTk.PhotoImage(self.rock_image)

        self.paper_image = Image.open("paper.png").resize((100, 100), resample=Image.BICUBIC)
        self.paper_photo = ImageTk.PhotoImage(self.paper_image)

        self.scissors_image = Image.open("scissor.png").resize((100, 100), resample=Image.BICUBIC)
        self.scissors_photo = ImageTk.PhotoImage(self.scissors_image)

        
        self.buttons = []
        for image, label_text in [(self.rock_photo, "Rock"), (self.paper_photo, "Paper"), (self.scissors_photo, "Scissors")]:
                button = tk.Button(self.button_frame, image=image, bg="pink", bd=0, fg="pink", command=lambda img=image: self.determine_winner(img))
                button.image = image
                button.pack(side=tk.LEFT, padx=10)

                label = tk.Label(self.button_frame, text=label_text, font=("Arial", 10), bg="pink", fg="#8b4513")
                label.pack(side=tk.LEFT, pady=10) 


        self.buttons.append(button)

        
        self.result_label = tk.Label(window, text="", font=("Arial", 14), bg="pink", fg="#8b4513")
        self.result_label.pack(pady=10)

        
        self.score_label = tk.Label(window, text="", font=("Arial", 12), bg="pink", fg="#8b4513")
        self.score_label.pack()

        
        self.play_again_button = tk.Button(window, text="Play Again", font=("Arial", 12), bg="#8b4513", fg="pink",
                                           command=self.reset_game)
        self.play_again_button.pack(pady=10)

    def determine_winner(self, user_choice):
        choices = {self.rock_photo: "Rock", self.paper_photo: "Paper", self.scissors_photo: "Scissors"}
        user_choice_name = choices[user_choice]

        computer_choice = random.choice(["Rock", "Paper", "Scissors"])

        if user_choice_name == computer_choice:
            result = "It's a tie!"
        elif (user_choice_name == "Rock" and computer_choice == "Scissors") or \
             (user_choice_name == "Paper" and computer_choice == "Rock") or \
             (user_choice_name == "Scissors" and computer_choice == "Paper"):
            result = "You win!"
            self.user_score += 1
        else:
            result = "Computer wins!"
            self.computer_score += 1

        self.rounds_played += 1
        self.update_result_label(f"Computer chose {computer_choice}. {result}")
        self.update_score_label()

    def update_result_label(self, text):
        self.result_label.config(text=text)

    def update_score_label(self):
        score_text = (f"Your Score: {self.user_score} | Computer Score: {self.computer_score} | Rounds Played: "
                      f"{self.rounds_played}")
        self.score_label.config(text=score_text)

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.update_result_label("")
        self.update_score_label()


window = tk.Tk()
window.configure(bg="pink")  
game = RockPaperScissorsGame(window)


window.mainloop()



