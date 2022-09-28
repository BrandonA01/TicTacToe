import tkinter as tk
from itertools import cycle
from tkinter import font
from Move import Move
from Player import Player

# Constants
BOARD_SIZE = 3  # define board size here

DEFAULT_PLAYERS = (  # define all players here
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)


# Classes
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)  # returns all players
        self.board_size = board_size
        self.current_player = next(self._players)  # returns the next player in the iterable
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]               # returns all rows, columns, and diagonals (all winning combos)
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        self.current_player = next(self._players)   # Switches player X to Player O

    def is_valid_move(self, move):
        row, col = move.row, move.col       # Return True if move is valid, and False otherwise.
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:                  # check winning combinations
            results = set(self._current_moves[n][m].label for n, m in combo)    # check board status with winning possibilities
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:                                      # check if is_win is True
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner             # returns a bool if game has a winner

    def is_tied(self):
        no_winner = not self._has_winner    # Return True if the game is tied, and False otherwise.
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)       # Resets all spaces
        self._has_winner = False
        self.winner_combo = []                          # Resets all variables accumulated in the game


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):  # menu option dropdown, under "file", has option to play again or exit app
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Tic Tac Toe",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self, bg="black")
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):                # creating spaces for the complete board
                button = tk.Button(                                    # Each space is a button, seen here
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=4,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)            # binding left click on a button to the function play()
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        clicked_btn = event.widget  # once player clicks
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):  # check it hasn't already been clicked
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():  # check for winner
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:  # if game hasn't ended, switch players
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):  # update squares/buttons to show players move
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg,
                        color="black"):  # updates the text above the game to display player's turn, and/or who's won
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):  # Reset board when user clicks "play again"
        self._game.reset_game()
        self._update_display(msg="Tic Tac Toe")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")


# Run methods
def main():  # Create the game's board and run its main loop
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()

# https://realpython.com/tic-tac-toe-python/  <-- Tutorial guide
