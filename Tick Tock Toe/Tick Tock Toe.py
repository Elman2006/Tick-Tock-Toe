# ---------------------------------- Madules ----------------------------------------
import customtkinter as ctk # A library like tkinter, but more modern designe
from tkinter import messagebox # For showing the notifications
import os
import sys

# ------------------------------------- Variables -------------------------------------
ctk.set_appearance_mode("System")    # “Light”, “Dark”, or “System”
ctk.set_default_color_theme("green")  # built‑in: “blue”, “green”, “dark-blue”
BTN_WIDTH_HEIGHT = 100
FG_CLR = "#3E5F44"
BTN_HOVER_CLR = "#5E936C"
BTN_CLR = "#93DA97"
RESET_BG   = "#D65A31"
RESET_HOVER= "#BF3E17"
SCORE_FONT = ("Arial", 32, "bold")

# Game state
current_player = "X"
board = [""] * 9


# --------------------------------- Functions ------------------------------------
def on_cell(idx):
    """ To rewrite the text of button """

    global current_player
    if board[idx] != "": # Check if cell is already occupied
        return

    board[idx] = current_player # Mark the cell
    buttons[idx].configure(text=current_player) # Update button display

    if check_win(current_player): # Check if current player won
        messagebox.showinfo("Game Over", f"Player {current_player} wins!")
        disable_all()

    elif "" not in board: # Check for draw
        messagebox.showinfo("Game Over", "It's a draw!")

    else:
        # switch turns
        current_player = "O" if current_player == "X" else "X"


def check_win(player):
    """Check win conditions"""

    wins = [
        (0,1,2), (3,4,5), (6,7,8),    # rows
        (0,3,6), (1,4,7), (2,5,8),    # cols
        (0,4,8), (2,4,6)              # diags
    ]

    for a,b,c in wins:
        if board[a]==board[b]==board[c]==player:
            return True
        
    return False


def disable_all():
    """ This function disables all the 9 game buttons, so the player cannot click them after the game is over."""

    for btn in buttons:
        # This method .configure() updates (changes) properties of the button after it has been created.
        btn.configure(state="disabled")


def reset_game():
    """Reset the game state"""

    global current_player, board
    current_player = "X"
    board = [""] * 9
    for btn in buttons:
        btn.configure(text="", state="normal")


def toggle_mode():
    """Toggle between dark/light mode and update switch text"""

    # read switch state by widget reference
    mode = "Dark" if dark_switch.get() else "Light"
    ctk.set_appearance_mode(mode)


# -------------------------------- Main ----------------------------------
app = ctk.CTk()
app.title("Tic Tac Toe")  # Make a name for game

app.resizable(False, False) # Make the app unchangable

# Create a frame for the game board
game_frame = ctk.CTkFrame(app)
game_frame.pack(pady=20, padx=20)


# Buttons
buttons = []  # We'll store buttons in a list for easier management

for i in range(9):
    btn = ctk.CTkButton(
        master=game_frame, 
        fg_color=BTN_CLR,
        text="",
        text_color="black",
        text_color_disabled="black",  # Disabled state
        font=SCORE_FONT,
        hover_color=BTN_HOVER_CLR,
        width=BTN_WIDTH_HEIGHT,
        height=BTN_WIDTH_HEIGHT,
        corner_radius=10,
        command=lambda i=i: on_cell(i)
    )
    buttons.append(btn)


# Grid layout - using loops for cleaner code
for i, btn in enumerate(buttons):
    row = i // 3 + 1  # Calculate row (0-2 becomes 1-3)
    col = i % 3 + 1   # Calculate column (0,1,2,0,1,2...)
    btn.grid(row=row, column=col, padx=2, pady=2)  # Add some padding between buttons


# Reset button
reset_btn = ctk.CTkButton(
    master=app,
    text="Reset",
    fg_color=RESET_BG,
    hover_color=RESET_HOVER,
    text_color="white",
    command=reset_game
)
reset_btn.pack(pady=10)


# Dark/Light mode switch
dark_switch = ctk.CTkSwitch(
    master=app,
    text="Dark Mode",
    command=toggle_mode
)
dark_switch.pack(pady=10)


# Center window
# Force window to update so we can get its actual size
app.update_idletasks()

window_width = app.winfo_width()
window_height = app.winfo_height()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width//2 - window_width//2)
y = (screen_height//2 - window_height//2)

app.geometry(f"{x}+{y}")

app.mainloop()
