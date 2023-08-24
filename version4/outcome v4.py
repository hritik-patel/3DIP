#All the imports
import tkinter as tk #Required for GUI
from tkinter import ttk as ttk #For combobox
import random #Randomise the colours
import time #Time the player, how long they take
import json #For getting data from the external files
import os #For macos users, getting data from external files is a hassle and this makes it easier

current_directory = os.path.dirname(os.path.abspath(__file__)) #Using OS import to locate files within the same folder, issue on macOS sometimes it doesn't recognise the file in the same folder
celebrities_file_path = os.path.join(current_directory, 'celebrities.json') #Using current directory will work as long as the JSON files are both in the same folder as the .py file
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
#Number of levels in the game
LEVELS = 6

class MainMenu: #Create the MainMenu class
    def __init__(self, master): #Contruct the main menu window
        self.master = master
        self.master.title("Main Menu") #Name of the window
        self.master.geometry("300x200") #Size of the menu window
        self.master.resizable(False, False) #Player cannot resize the window and mess up the placement of widgets
        self.master.config(bg="white") #White background

        label = tk.Label(self.master, text="Select a Game", bg="white", fg="black", font=("Arial", 16, "bold")) #Label asking the player to selected a game
        label.pack(pady=10) 

        self.game_combobox = ttk.Combobox(self.master, values=["Colour Match Game", "Higher Lower Game"], state="readonly") #Create a combobox with 2 options and readonly state so the player cannot type in it
        self.game_combobox.pack(pady=10)

        play_button = tk.Button(self.master, text="Play", command=self.start_game) #Start the game depending on the selected game in the combobox
        play_button.pack(pady=5)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Quit the program, destroy everything
        quit_button.pack(pady=5)

    def start_game(self):
        selected_game = self.game_combobox.get() #Get the value in the combobox, either 'Colour Match Game' or 'Higher Lower Game'
        if selected_game == "Colour Match Game": #If Colour Match Game is selected in the combobox
            self.master.destroy() #Destroy the main menu window
            root = tk.Tk() 
            ColourMatchGame(root)
            root.mainloop()
        elif selected_game == "Higher Lower Game": #If Higher Lower Game is selected
            self.master.withdraw() #Essentially iconffying the game, minimising it or moving it to the background out of focus
            self.game_window = tk.Toplevel(self.master)  #Create a Toplevel window for the game so it is in focus
            HigherLowerGame(self.game_window, self) 
            self.game_window.mainloop()


class ColourMatchGame: #Create the ColourMatchGame class
    #Setting up the main window
    def __init__(self, master): #Construct the parts that make up ColourMatchGame class
        self.master = master
        self.master.title("Colour Match Game") #Name of the window
        self.master.geometry("550x775") #Size of the game window
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
        MainMenu(root)  #Start the main menu
        root.mainloop()

    def replay_game(self):
        #Restart the game by creating a new game window
        self.end_screen.destroy() #Destroy the end game screen window
        self.master.destroy() #Destroy the current game window
        root = tk.Tk() #Create a new game window
        ColourMatchGame(root) #Start the game
        root.mainloop()

    def update_timer(self):
        #Update the timer label with the elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text="Time: {:.2f} seconds".format(elapsed_time))
            self.master.after(10, self.update_timer) #Every 0.01 seconds update the timer label (0.01s looks much better than 0.1s, and since the game is very small it doesn't make a difference on performance)

class HigherLowerGame: #Create the higher lower game class
    def __init__(self, master, main_menu): #Construct the HigherLowerGame class
        self.master = master  #The Tkinter root window for the game
        self.master.title("Higher or Lower Game")  #Set the window title to Higher or Lower game
        self.master.geometry("500x300")  #Set the window size
        self.master.resizable(False, False)  #Disable window resizing so the game doesnt break
        self.main_menu = main_menu  #The MainMenu instance to go back to the main menu if needed

        self.current_topic = None  #The selected topic for the game (Celebrities or Companies) set to None for now
        self.score = 0  #Player's score set to 0

        self.create_topic_selection_screen()  #Call the method to create the topic selection screen, where the player selects which topic to play

    def create_topic_selection_screen(self):
        #Create the topic selection screen
        self.clear_window() #Clear the current window

        labeltopic = tk.Label(self.master, text="Pick the topic:", font=("Arial", 16)) #Label for the top of the window
        labeltopic.pack(pady=20)

        self.topic_combobox = ttk.Combobox(self.master, values=["Celebrities", "Companies"], state="readonly") #Create the combobox for selecting topic, readonly state so the player ccannot write in it
        self.topic_combobox.pack(pady=10)

        play_button = tk.Button(self.master, text="Play", command=self.start_game) #Button to start the game depending on the topic selected
        play_button.pack(pady=5)

        main_menu_button = tk.Button(self.master, text="Main Menu", command=self.show_main_menu) #Button to take the player back to the main menu to switch games or to switch topics
        main_menu_button.pack(pady=5)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Quits the entire program, ends the game
        quit_button.pack(pady=5)

    def show_main_menu(self): #Show the main menu and close the game window
        self.master.destroy() #Destroy the window
        self.main_menu.master.deiconify() #Restores the main menu that has been iconified earlier

    def start_game(self): #Start the game by setting the current topic and creating the game screen
        self.current_topic = self.topic_combobox.get() #Get the topic the player selected in the combobox
        self.create_game_screen() #Call the create_game_screen method which creates the main game window

    def create_game_screen(self): #Create the game screen
        self.clear_window()  #Clear the current window
        topic_word = "celebrity" if self.current_topic == "Celebrities" else "company" #For the labels to use the correct wording and proper grammar later
        label = tk.Label(self.master, text=f"Guess which {topic_word} has the higher {self.get_attribute()}?", font=("Arial", 16)) #For example here it would originally say 'Guess which Celebrities ...' but with the topic word it does 'Guess which celebrity ...'
        label.pack(pady=5) 

        data = self.load_data() # Load data from external files (companies.json or celebrities.json)
        choices = random.sample(data, 2) #Uses the random.sample() function to pick 2 random data from the external data files
        choice1, choice2 = choices # Assign the two randomly selected choices to variables choice1 and choice2

        button1 = tk.Button(self.master, text=choice1['name'], command=lambda: self.check_answer(choice1, choice2)) #Create a button for the first option (choice1) with its name as the button text and set its command to check_answer with choice1 and choice2
        button1.pack(pady=10)

        button2 = tk.Button(self.master, text=choice2['name'], command=lambda: self.check_answer(choice2, choice1)) #Create another button for the second option (choice2) with its name as the button text and set its command to check_answer with choice2 and choice1
        button2.pack(pady=10)

    def get_attribute(self): #Get the attribute based on the selected topic
        if self.current_topic == "Celebrities":
            return "million followers"
        elif self.current_topic == "Companies":
            return "networth in billions"
        else:   
            return None

    def get_value(self, choice): #Get the value of the attribute for a given choice (million followers for celebrities, billion net worth for companies)
        attribute = self.get_attribute()
        if attribute in choice:
            return choice[attribute]
        else:
            return 0

    def check_answer(self, selected_choice, other_choice): #Check the player's answer and display the correct or the incorrect screen
        self.first_choice = selected_choice #Store the selected choice for later use
        self.second_choice = other_choice #Store the other choice for later use

        selected_value = self.get_value(selected_choice) #Get the value of the selected choice from the file
        other_value = self.get_value(other_choice) #Get the value of the other choice from the file

        if selected_value > other_value: #Compare the values see if the player chose the right answer, if so:
            self.score += 1 #Increment the score if the answer is correct
            self.create_correct_screen(selected_value, other_value, selected_value - other_value) #Show the correct screen
        else:
            self.create_incorrect_screen(selected_value, other_value, selected_value - other_value) #Show the incorrect screen

    def create_correct_screen(self, higher_value, lower_value, difference_value):
        self.clear_window() #Clear the window to for the correct screen

        label = tk.Label(self.master, text="Correct!", font=("Arial", 16, "bold"), fg="green") #Show "Correct!" label
        label.pack(pady=20)

        score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 14)) #Show the current score
        score_label.pack(pady=10)

        attribute_label = "million followers on instagram" if self.current_topic == "Celebrities" else "billion net worth in usd" #Choose the correct label based on the selected topic

        choice1_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {higher_value:,} {attribute_label}", font=("Arial", 12)) #Show the name and value of the selected choice
        choice1_label.pack(pady=5)

        choice2_label = tk.Label(self.master, text=f"{self.get_name(self.second_choice)} has {lower_value:,} {attribute_label}", font=("Arial", 12)) #Show the name and value of the other choice
        choice2_label.pack(pady=5)

        if difference_value >= 0: #Check if the difference between values is positive
            difference_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {difference_value:.1f} {attribute_label} more than {self.get_name(self.second_choice)}!", font=("Arial", 12)) #Show the difference between values when it's positive, using .1f for 1dp
        else:
            difference_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {abs(difference_value):.1f,} {attribute_label} less than {self.get_name(self.second_choice)}!", font=("Arial", 12)) #Show the difference between values when it's negative (use abs to get the positive value by removing the negative sign), using .1f for 1dp
        difference_label.pack(pady=5)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Create a button to quit the game
        quit_button.pack(side=tk.RIGHT, padx=10, pady=10) 

        next_round_button = tk.Button(self.master, text="Next Round", command=self.next_round) #Create a button to go to the next round
        next_round_button.pack(pady=10)  # Add padding to the button

    def create_incorrect_screen(self, higher_value, lower_value, difference_value):
        self.clear_window() #Clear the current window for the incorrect screen

        label = tk.Label(self.master, text="Incorrect!", font=("Arial", 16, "bold"), fg="red") #Show "Incorrect!" label
        label.pack(pady=20)

        score_label = tk.Label(self.master, text=f"Final Score: {self.score}", font=("Arial", 14)) #Show the final score
        score_label.pack(pady=10)

        attribute_label = "million followers" if self.current_topic == "Celebrities" else "billion net worth" #Use the correct label based on the selected topic

        choice1_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {higher_value:,} {attribute_label}", font=("Arial", 12)) #Show the name and value of the selected choice
        choice1_label.pack(pady=5)
        choice2_label = tk.Label(self.master, text=f"{self.get_name(self.second_choice)} has {lower_value:,} {attribute_label}", font=("Arial", 12)) #Show the name and value of the other choice
        choice2_label.pack(pady=5)

        if difference_value >= 0: #Check if the difference between values is positive
            difference_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {(difference_value):.1f} {attribute_label} less than {self.get_name(self.second_choice)}!", font=("Arial", 12)) #Show the difference between values when it's positive, using .1f for 1dp
        else:
            difference_label = tk.Label(self.master, text=f"{self.get_name(self.first_choice)} has {abs(difference_value):.1f} {attribute_label} less than {self.get_name(self.second_choice)}!", font=("Arial", 12)) #Show the difference between values when it's negative (use abs to get the positive value by removing negative sign), using .1f for 1dp
        difference_label.pack(pady=5) 

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit) #Create a button to quit the game
        quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        play_again_button = tk.Button(self.master, text="Play Again", command=self.play_again) #Create a button to play the game again
        play_again_button.pack(pady=10)

        main_menu_button = tk.Button(self.master, text="Main Menu", command=self.show_main_menu) #Create a button to go back to the main menu
        main_menu_button.pack(pady=10)

    def next_round(self): #Get new data and choices for the next round
        self.clear_window() #Clear the current window
        self.create_game_screen() #Create the game screen again for the next round
        self.create_game_screen() #Create the game screen with the new data and choices for the next round

    def get_name(self, choice): #Get the name of a choice (celebrity or company) from the data file
        return choice['name']

    def play_again(self): #Start the game again by resetting the score and creating the game screen
        self.score = 0
        self.create_game_screen()

    def show_main_menu(self): #Show the main menu and destroy the game window
        self.master.destroy()
        self.main_menu.master.deiconify() #Deiconify as we simply withdrew the main menu at the start

    def load_data(self): #Load the data (celebrities or companies) from the external file
        file_path = celebrities_file_path if self.current_topic == "Celebrities" else companies_file_path #If not Celebrities, use the other option
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    def clear_window(self): #Clear the current window by destroying all widgets
        for widget in self.master.winfo_children(): #Check if there are widgets in the window
            widget.destroy() #If there are any widgets, destroy them

if __name__ == "__main__": #This creates a new Tkinter window using the MainMenu class and starts the main event loop
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
