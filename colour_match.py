#Note: Target colour means the randomly selected colour that the player has to click
#Imports
import tkinter as tk
from tkinter import messagebox
import random
import time

#Constant variables
GRID_SIZE = 5
#Using hexadecimals for bright colours
COLORS = {
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "yellow": "#ffff00"
}
LEVELS = 6
HIGH_SCORE_FILE = "high_scores_colour.txt"


class ColourMatchGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Colour Match Game")
        self.master.resizable(False, False)
        self.level = 1
        self.start_time = None
        self.total_time = None

        #Create the top frame for instructions and target colour
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady = 10)

        #Create the instruction label
        self.instruction_label = tk.Label(self.top_frame, text = "Click the boxes with the target colour")
        self.instruction_label.pack()

        #Create the target colour label
        self.target_colour_label = tk.Label(self.top_frame, text = "")
        self.target_colour_label.pack()

        #Create the timer label
        self.timer_label = tk.Label(self.top_frame, text = "Time: 0.00 seconds")
        self.timer_label.pack()

        #Create the grid frame for the boxes
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()

        #Create the level label
        self.level_label = tk.Label(self.master, text = "Level 1")
        self.level_label.pack()

        #Create the buttons frame
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(fill = tk.X, padx = 10, pady = 10)

        #Create the check button
        self.check_button = tk.Button(self.buttons_frame, text = "Check", command = self.check_boxes)
        self.check_button.pack(side = tk.LEFT, padx = (0, 10))

        #Create the restart button
        self.restart_button = tk.Button(self.buttons_frame, text = "Restart", command = self.start_game)
        self.restart_button.pack(side = tk.LEFT)

        #Create the menu button
        self.menu_button = tk.Button(self.buttons_frame, text = "Menu", command = self.show_menu)
        self.menu_button.pack(side = tk.RIGHT)

        #Create the warning label
        self.warning_label = tk.Label(self.master, text = "", fg = "red")
        self.warning_label.pack()

        #Initialize the grid
        self.grid_checkbuttons = []
        self.initialize_grid()

        #Bind spacebar key press to the check action
        self.master.bind("<space>", lambda event: self.check_boxes())

        #Start the game
        self.start_game()

    def initialize_grid(self):
        #Create the grid of checkboxes
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self.grid_frame, width = 10, height = 5, variable = var, anchor = tk.CENTER)
                checkbutton.grid(row = row, column = col, padx = 5, pady = 5)
                self.grid_checkbuttons.append((checkbutton, var))

    def start_game(self):
        #Start a new game
        self.level = 1
        self.start_time = time.time()
        self.update_level_label()
        self.randomize_grid_colours()
        self.update_timer()

    def update_level_label(self):
        #Update the level label with the current level
        self.level_label.config(text = "Level {}".format(self.level))

    def randomize_grid_colours(self):
        #Randomize the colours of the grid checkboxes
        target_colour = random.choice(list(COLORS.keys()))
        self.target_colour_label.config(text = "Target Colour: {}".format(target_colour.capitalize()))

        for checkbutton, var in self.grid_checkbuttons:
            var.set(False)
            colour_name = random.choice(list(COLORS.keys()))
            if colour_name == target_colour:
                checkbutton.target_colour = True
            else:
                checkbutton.target_colour = False
            checkbutton.config(bg = COLORS[colour_name], activebackground = COLORS[colour_name], state = tk.NORMAL)

    def check_boxes(self):
        #Check if the selected checkboxes are correct
        correct_count = 0
        incorrect_count = 0
        for checkbutton, var in self.grid_checkbuttons:
            if var.get() and checkbutton.target_colour:
                correct_count += 1
            elif not var.get() and checkbutton.target_colour:
                incorrect_count += 1

        if correct_count == sum([var.get() for _, var in self.grid_checkbuttons]) and incorrect_count == 0:
            #If all correct checkboxes are selected, move to the next level or end the game
            self.level += 1
            if self.level <= LEVELS:
                self.update_level_label()
                self.randomize_grid_colours()
                self.reset_checkbuttons()
            else:
                self.end_game()
        else:
            #Show a warning message for incorrect or missing checkboxes
            self.warning_label.config(text = "Not all correct checkboxes are selected or there are incorrect checkboxes.")
            self.master.after(3000, lambda: self.warning_label.config(text = ""))

    def reset_checkbuttons(self):
        #Reset all checkboxes to unchecked state
        for checkbutton, var in self.grid_checkbuttons:
            var.set(False)

    def end_game(self):
        #End the game and check for high scores
        self.total_time = round(time.time() - self.start_time, 2)
        self.start_time = None

        #Check if the current time is a high score
        high_scores = self.load_high_scores()
        if self.is_high_score(high_scores):
            self.ask_player_name(high_scores)
        else:
            self.show_end_screen()

    def show_end_screen(self):
        #Show the end game screen
        self.end_screen = tk.Toplevel(self.master)
        self.end_screen.title("Game Over")
        self.end_screen.resizable(False, False)

        #Create the result label
        result_label = tk.Label(self.end_screen, text = "Game Over! You completed all levels.")
        result_label.pack(pady = 10)

        #Create the time label
        time_label = tk.Label(self.end_screen, text = "Total Time: {:.2f} seconds".format(self.total_time))
        time_label.pack()

        #Create the replay button
        replay_button = tk.Button(self.end_screen, text = "Replay", command = self.replay_game)
        replay_button.pack(side = tk.LEFT)

        #Create the menu button
        menu_button = tk.Button(self.end_screen, text = "Menu", command = self.show_menu)
        menu_button.pack(side = tk.LEFT)

        #Create the quit button
        quit_button = tk.Button(self.end_screen, text = "Quit", command = self.end_screen.quit)
        quit_button.pack(side = tk.RIGHT)

        self.master.withdraw()  #Hide the game window
        self.end_screen.mainloop()

    def show_menu(self):
        #Placeholder for the menu functionality
        print("Menu button clicked.")

    def replay_game(self):
        #Restart the game by creating a new game window
        self.end_screen.destroy()  #Destroy the end screen window
        self.master.destroy()  #Destroy the current game window
        root = tk.Tk()  #Create a new game window
        game = ColourMatchGame(root)
        root.mainloop()

    def update_timer(self):
        #Update the timer label with the elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text = "Time: {:.2f} seconds".format(elapsed_time))
            self.master.after(100, self.update_timer)

    def load_high_scores(self):
        #Load the high scores from the file
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                high_scores = [line.strip().split(",") for line in file]
            return high_scores
        except FileNotFoundError:
            return []

    def save_high_scores(self, high_scores):
        #Save the high scores to the file
        with open(HIGH_SCORE_FILE, "w") as file:
            for score in high_scores:
                file.write(",".join(score) + "\n")

    def is_high_score(self, high_scores):
        #Check if the current time is a high score
        return len(high_scores) < 5 or self.total_time < float(high_scores[-1][0])

    def ask_player_name(self, high_scores):
        #Ask the player to enter their name for the high score
        dialog = tk.Toplevel(self.master)
        dialog.title("New High Score")
        dialog.geometry("300x200")

        score_label = tk.Label(dialog, text = "Your score: {:.2f} seconds".format(self.total_time))
        score_label.pack(pady = 10)

        high_score_label = tk.Label(dialog, text = "Congratulations! You achieved a new high score.")
        high_score_label.pack()

        name_label = tk.Label(dialog, text =  "Enter your name:")
        name_label.pack()

        name_entry = tk.Entry(dialog)
        name_entry.pack()

        submit_button = tk.Button(dialog, text =  "Submit", command =  lambda: self.add_high_score(dialog, high_scores, name_entry.get()))
        submit_button.pack()

    def add_high_score(self, dialog, high_scores, player_name):
        #Add the player's high score to the list and save it
        high_scores.append([str(self.total_time), player_name])
        high_scores.sort(key =  lambda x: float(x[0]))
        if len(high_scores) > 5:
            high_scores = high_scores[:5]
        self.save_high_scores(high_scores)
        messagebox.showinfo("High Score Saved", "Congratulations! Your high score has been saved.")
        dialog.destroy()
        self.show_end_screen()


root = tk.Tk()
game = ColourMatchGame(root)
root.mainloop()
