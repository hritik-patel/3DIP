#All the imports
import tkinter as tk #Required for GUI
from tkinter import ttk as ttk #For combobox
import random #Randomise the colours
import time #Time the player, how long they take
import json #For getting data from the external files
import os #For macos users, getting access to the data from external files is a hassle and this makes it easier

current_directory = os.path.dirname(os.path.abspath(__file__))
celebrities_file_path = os.path.join(current_directory, 'celebrities.json')
companies_file_path = os.path.join(current_directory, 'companies.json')

#Constant variables
GRID_SIZE = 5
#Using hexadecimals for bright colours
COLOURS = {
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#00D8FF",
    "yellow": "#ffff00"
}
LEVELS = 6

class MainMenu: #Create the main menu class
    def __init__(self, master): #Contruct the main menu window
        self.master = master
        self.master.title("Main Menu") #Name of window
        self.master.geometry("300x200") #Size of the window
        self.master.resizable(False, False) #Unresizable winddow
        self.master.config(bg="white") 

        #Create and display widgets for the main menu
        label = tk.Label(self.master, text="Select a Game", bg="white", fg="black", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        self.game_combobox = ttk.Combobox(self.master, values=["Colour Match Game", "Higher Lower Game"], state="readonly") #Combobox for the main menu, where the player selects the game, set to readonly so the playre cant write in the box
        self.game_combobox.pack(pady=10)

        play_button = tk.Button(self.master, text="Play", command=self.start_game) #Start the game depending on the selected option in the combobox
        play_button.pack(pady=5)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Quit the program
        quit_button.pack(pady=5)

    def start_game(self): #Start the selected game based on what the user picks
        selected_game = self.game_combobox.get() #Get what the user has selected
        if selected_game == "Colour Match Game": #If colour match game
            self.master.destroy() #Destroy main menu
            root = tk.Tk()
            game = ColourMatchGame(root)
            root.mainloop()
        elif selected_game == "Higher Lower Game": #If higher lower game
            self.master.withdraw() #Withdraw main menu, similar to iconify(), where it pulls it out of focus
            self.game_window = tk.Toplevel(self.master)  #Create a Toplevel window for the game to put it into focus
            game = HigherLowerGame(self.game_window, self)  
            self.game_window.mainloop()


class ColourMatchGame: #Create the ColourMatchGame class
    #Setting up the main window
    def __init__(self, master): #Constructor used to create the attributes of the ColourMatchGame class
        self.master = master
        self.master.title("Colour Match Game") #Name of the window
        self.master.geometry("550x750") #Size of the game window
        self.master.resizable(False, False) #Game window cannot be resized so things inside don't move around
        self.level = 1 #Set the starting level to 1
        self.start_time = None #Set time to None
        self.total_time = None #Set total time to None
        self.master.config(bg="black") #Set the game window background to black

        #Create the top frame for instructions and target colour
        self.top_frame = tk.Frame(self.master, bg="black")
        self.top_frame.pack(pady=10)

        #Create the instruction label
        self.instruction_label = tk.Label(self.top_frame, text="Click the boxes with the target colour", bg="black", fg="white")
        self.instruction_label.pack()

        #Create the target colour label
        self.target_colour_label = tk.Label(self.top_frame, text="", bg="black", fg="yellow", font=("Arial", 16, "bold"))
        self.target_colour_label.pack()

        #Create the timer label
        self.timer_label = tk.Label(self.top_frame, text="Time: 0.00 seconds", bg="black", fg="white")
        self.timer_label.pack()

        #Create the grid frame for the boxes
        self.grid_frame = tk.Frame(self.master, bg="black")
        self.grid_frame.pack()

        #Create the level label
        self.level_label = tk.Label(self.master, text="Level 1", bg="black", fg="white")
        self.level_label.pack()

        #Create the buttons frame
        self.buttons_frame = tk.Frame(self.master, bg="black")
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        #Create the check button
        self.check_button = tk.Button(self.buttons_frame, text="Check (Spacebar)", command=self.check_boxes)
        self.check_button.pack(pady=10)

        #Create the restart button
        self.restart_button = tk.Button(self.buttons_frame, text="Restart (R)", command=self.start_game)
        self.restart_button.pack(side=tk.LEFT, padx=5)

        #Create the menu button
        self.menu_button = tk.Button(self.buttons_frame, text="Menu", command=self.show_menu)
        self.menu_button.pack(side=tk.RIGHT, padx=5)

        #Create the warning label
        self.warning_label = tk.Label(self.master, text="", fg="red", bg="black")
        self.warning_label.pack()

        #Create the exit button
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(side=tk.BOTTOM, pady=10)

        #Initialize the grid
        self.grid_checkbuttons = []
        self.initialize_grid()

        #Bind spacebar key press to the check action
        self.master.bind("<space>", lambda event: self.check_boxes())

        #Bind 'r' key press to the restart action
        self.master.bind("r", lambda event: self.start_game())
        
        #Start the game
        self.start_game()

    def initialize_grid(self): 
        #Create the grid of checkboxes
        for row in range(GRID_SIZE): #Repeat 5 times as the GRID_SIZE constant = 5
            for col in range(GRID_SIZE): #Used to create columns for the grid of checkboxes in the game
                var = tk.BooleanVar() #Create a BooleanVar for each checkbox to track its state (checked or unchecked)
                checkbutton = tk.Checkbutton(self.grid_frame, width=10, height=5, variable=var, anchor=tk.CENTER, bg="white", activebackground="white") #Create a checkbutton widget
                checkbutton.grid(row=row, column=col, padx=5, pady=5) #Place the checkbutton in the grid at the specified row and column with padding
                self.grid_checkbuttons.append((checkbutton, var)) #Store the checkbutton and its variables in the list for later use

    def start_game(self):
        #Start a new game
        self.level = 1 #Set the starting level to 1
        self.start_time = time.time() #Make the current time as the start time
        self.update_level_label() #Update the level label to show the current level
        self.randomize_grid_colours() #Randomize the colours of the grid checkboxes
        self.update_timer() #Start updating the timer label with the elapsed time

    def update_level_label(self):
        #Update the level label with the current level
        self.level_label.config(text="Level {}".format(self.level))

    def randomize_grid_colours(self):
        #Randomize the colours of the grid checkboxes
        target_colour = random.choice(list(COLOURS.keys())) #Choose a random colour as the target colour
        self.target_colour_label.config(text="Target Colour: {}".format(target_colour.capitalize()), fg=COLOURS[target_colour]) #Update the target colour label with the chosen colour and colour the text with the target colour

        for checkbutton, var in self.grid_checkbuttons: #Loop through the grid checkboxes and their variables
            var.set(False) #Set each variable to False (meaning all the checkbuttons are unchecked)
            colour_name = random.choice(list(COLOURS.keys())) #Choose a random colour for the current checkbox
            if colour_name == target_colour: #Check if the colour matches the target colour
                checkbutton.target_colour = True #If colour matches with target colour, then set a the attribute 'target_colour' for the checkbutton to True
            else:
                checkbutton.target_colour = False #If the colour does not match then set attribute 'target_colour' for the checkbutton to False
            checkbutton.config(bg=COLOURS[colour_name], activebackground=COLOURS[colour_name], state=tk.NORMAL) #Set the background colour and active background colour for the checkbutton

    def check_boxes(self):
        #Check if the selected checkboxes are correct
        correct_count = 0 #Counter for correctly selected checkboxes
        incorrect_count = 0 #Counter for incorrectly selected checkboxes

        for checkbutton, var in self.grid_checkbuttons: #Loop through the grid checkboxes and their associated variables
            if var.get() and checkbutton.target_colour: #Check if the checkbox is checked (var.get() == True) and it matches the target colour (checkbutton.target_colour == True)
                correct_count += 1 #Add one to the correct count
            elif not var.get() and checkbutton.target_colour: #Check if the checkbox is unchecked (var.get() == False) and it matches the target colour (checkbutton.target_colour == True)
                incorrect_count += 1 #Add one to the incorrect count

        if correct_count == sum([var.get() for _, var in self.grid_checkbuttons]) and incorrect_count == 0: #Check if all correct checkboxes are selected and no incorrect checkboxes are selected
            self.level += 1 #If so, increase the level by one
            if self.level <= LEVELS: #Check if the current level is less than or equal to the total number of levels which is 6
                self.update_level_label() #Update the level label to show the new level
                self.randomize_grid_colours() #Randomize the colours of the grid checkboxes for the next level
                self.reset_checkbuttons() #Reset all checkboxes to unchecked state for the next level
            else:
                self.end_game() #If all levels are completed, meaning the player has played all 6 levels, end the game
        else:
            #Show a warning message for incorrect or missing checkboxes
            self.warning_label.config(text="Not all correct checkboxes are selected or there are incorrect checkboxes.")
            self.master.after(3000, lambda: self.warning_label.config(text="")) #Warning disappears after 3 seconds

    def reset_checkbuttons(self):
        #Reset all checkboxes to unchecked state
        for checkbutton, var in self.grid_checkbuttons: #Loop through the grid checkboxes and their associated variables
            var.set(False) #Set each variable to False (unchecked)

    def end_game(self):
        #End the game
        self.total_time = round(time.time() - self.start_time, 2) #Calculate the total time taken to complete the game and round to 2dp
        self.start_time = None #Reset the start time
        self.show_end_screen() #Display the end game screen

    def show_end_screen(self):
        #Show the end game screen
        self.end_screen = tk.Toplevel(self.master) #Create a new Toplevel window as the end game screen
        self.end_screen.title("Game Over") #Set the title of the end game screen
        self.end_screen.resizable(False, False) #Disable window resizing for the end game screen
        self.end_screen.config(bg="black") #Set the background of the end game screen to black

        #Create the result label
        result_label = tk.Label(self.end_screen, text="Game Over! You completed all levels", bg="black", fg="white") #Create a label to display the result message
        result_label.pack(pady=10) #Place the label in the end game screen with padding

        #Create the time label
        time_label = tk.Label(self.end_screen, text="Total Time: {:.2f} seconds".format(self.total_time), bg="black", fg="white") #Create a label to display the total time taken
        time_label.pack() #Place the label in the end game screen

        # Create the replay button
        replay_button = tk.Button(self.end_screen, text="Replay", command=self.replay_game) #Create a button to replay the game
        replay_button.pack(side=tk.LEFT, padx=5) #Place the button on the left side with padding

        # Create the menu button
        menu_button = tk.Button(self.end_screen, text="Menu", command=self.show_menu) #Create a button to go back to the main menu
        menu_button.pack(side=tk.LEFT, padx=5) #Place the button on the left side with padding

        # Create the quit button
        quit_button = tk.Button(self.end_screen, text="Quit", command=self.end_screen.quit) #Create a button to quit the game
        quit_button.pack(side=tk.RIGHT, padx=5) #Place the button on the right side with padding

        self.master.withdraw() #Hide the game window
        self.end_screen.lift() #Bring the end game screen to the front and give it focus

        self.end_screen.mainloop() #Start the loop for the end game screen

    def show_menu(self):
        #Show the main menu and close the game window
        self.master.destroy()  #Destroy the current game window
        root = tk.Tk()  #Create a new main menu window
        main_menu = MainMenu(root)  #Start the main menu
        root.mainloop()

    def replay_game(self):
        #Restart the game by creating a new game window
        self.end_screen.destroy() #Destroy the end game screen window
        self.master.destroy() #Destroy the current game window
        root = tk.Tk() #Create a new game window
        game = ColourMatchGame(root) #Start the game
        root.mainloop()

    def update_timer(self):
        #Update the timer label with the elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text="Time: {:.2f} seconds".format(elapsed_time))
            self.master.after(10, self.update_timer) #Every 0.01 seconds update the timer label (0.01s looks much better than 0.1s, and since the game is very small it doesn't make a difference on performance)

class HigherLowerGame:
    def __init__(self, master, main_menu): #Construct the main menu
        #Initialize the Higher Lower Guessing Game window
        self.master = master
        self.master.title("Higher or Lower Guessing Game") #Name of window
        self.master.geometry("450x300") #Size of window
        self.master.resizable(False, False) #Resizability of the window is disabled so the widgets inside dont get moved around
        self.main_menu = main_menu

        #Variables to track the game,
        self.current_topic = None
        self.score = 0

        #Create the topic selection screen
        self.create_topic_selection_screen()

    def clear_window(self):
        for widget in self.master.winfo_children(): #Loop through all widgets that are in the wiindow
            widget.destroy() #Destroy each widget to clear the window

    def create_topic_selection_screen(self):
        self.clear_window() #Clear the current window by destroying all other widgets
        label = tk.Label(self.master, text="Pick the topic:", font=("Arial", 16)) #Create a label widget for topic selection
        label.pack(pady=20) #Place the label widget in the window

        self.topic_combobox = ttk.Combobox(self.master, values=["Celebrities", "Companies"], state="readonly") #Create a combobox widget for selecting topics
        self.topic_combobox.pack(pady=10) #Place the combobox in the window

        play_button = tk.Button(self.master, text="Play", command=self.start_game) #Create a button widget for starting the game
        play_button.pack(pady=5) #Place the button in the window

        main_menu_button = tk.Button(self.master, text="Main Menu", command=self.show_main_menu) #Create a button widget for going back to the main menu
        main_menu_button.pack(pady=5) #Place the button in the window

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Create a button widget for quitting the game
        quit_button.pack(pady=5) #Place the button in the window

    def show_main_menu(self):
        self.master.destroy() #Close the current game window
        self.main_menu.master.deiconify() #Display the main menu window

    def start_game(self):
        self.current_topic = self.topic_combobox.get() #Get the selected topic from the combobox
        self.create_game_screen() #Create the game screen for the selected topic

    def create_game_screen(self):
        self.clear_window() #Clear the current window by destroying all widgets
        topic_word = "celebrity" if self.current_topic == "Celebrities" else "company" #Decide the word 'celebrity' or 'company' based on the selected topic
        label = tk.Label(self.master, text=f"Guess which {topic_word} has the higher {self.get_attribute()}?", font=("Arial", 16)) #Create a label widget with the instructions depending on the topic
        label.pack(pady=5) #Place the label in the window

        data = self.load_data() #Load the data (celebrities or companies) from the external file
        choices = random.sample(data, 2) #Randomly select 2 (celebrities or companies) from the external data files
        choice1, choice2 = choices #Give the selected choices variable names choice1 and choice2

        button1 = tk.Button(self.master, text=choice1['name'], command=lambda: self.check_answer(choice1, choice2)) #Create a button widget for the first choice
        button1.pack(pady=10) #Place the button in the window

        button2 = tk.Button(self.master, text=choice2['name'], command=lambda: self.check_answer(choice2, choice1)) #Create a button widget for the second choice
        button2.pack(pady=10) #Place the button in the window
    def get_attribute(self):
        return "instagram followers" if self.current_topic == "Celebrities" else "net worth" #Return the attribute based on the selected topic

    def get_value(self, choice):
        return choice['instagram followers'] if self.current_topic == "Celebrities" else choice['net_worth'] #Return the value of the attribute for the given choice

    def check_answer(self, selected_choice, other_choice):
        if self.get_value(selected_choice) > self.get_value(other_choice): #Compare the values of the selected choices
            self.score += 1 #Increment the score if the selected choice has a higher value
            self.create_correct_screen() #Display the correct screen
        else:
            self.create_incorrect_screen() #Display the incorrect screen

    def create_correct_screen(self):
        self.clear_window() #Clear the current window by destroying all widgets

        label = tk.Label(self.master, text="Correct!", font=("Arial", 16)) #Create a label widget to show "Correct!"
        label.pack(pady=20) #Place the label in the window

        score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 14)) #Create a label widget to show the current score
        score_label.pack(pady=10) #Place the label in the window
        next_round_button = tk.Button(self.master, text="Next Round", command=self.create_game_screen) #Create a button widget for starting the next round
        next_round_button.pack(pady=10) #Place the button in the window

    def create_incorrect_screen(self):
        self.clear_window() #Clear the current window by destroying all widgets

        label = tk.Label(self.master, text="Incorrect!", font=("Arial", 16)) #Create a label widget to show "Incorrect!"
        label.pack(pady=20) #Place the label in the window
        score_label = tk.Label(self.master, text=f"Final Score: {self.score}", font=("Arial", 14)) #Create a label widget to show the final score
        score_label.pack(pady=10) #Place the label in the window

        play_again_button = tk.Button(self.master, text="Play Again", command=self.play_again) #Create a button widget for playing the game again
        play_again_button.pack(pady=10) #Place the button in the window

        main_menu_button = tk.Button(self.master, text="Main Menu", command=self.show_main_menu) #Create a button widget for going back to the main menu
        main_menu_button.pack(pady=10) #Place the button in the window

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Create a button widget for quitting the game
        quit_button.pack(pady=10) #Place the button in the window

    def play_again(self):
        self.score = 0 #Reset the score to zero
        self.create_game_screen() #Create the game screen for the next round

    def show_main_menu(self):
        self.master.destroy() #Close the current game window
        self.main_menu.master.deiconify() #Display the main menu window

    def load_data(self):
        file_path = celebrities_file_path if self.current_topic == "Celebrities" else companies_file_path #Choose the file path based on the topic
        with open(file_path, "r") as file:
            data = json.load(file) #Load data from the external file (celebrities.jsn or companies.json)
        return data #Return the loaded data

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()


