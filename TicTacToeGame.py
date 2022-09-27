from tkinter import *
import tkinter as tk

from TicTacToeBoard import TicTacToeBoard

root = Tk()
root.title("TicTacToe")
root.geometry('400x400')


class TicTacToeGame():
    WINNING_COMBOS = [
        {1, 2, 3}, {4, 5, 6}, {7, 8, 9},
        {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
        {1, 5, 9}, {3, 5, 7},
    ]

    def __init__(self, main):
        frame = Frame(main)
        frame.pack()

        self.label = Label(frame, text="Tic Tac Toe", font=('Ariel', 25))
        self.label.pack()
        self.board = TicTacToeBoard(main)
        self.resetButton = Button(frame, text="reset", font=('Ariel', 12), command=lambda: self.board.resetSpaces())
        self.resetButton.pack()

    def make_turn(self):
        pass

    def print_board(self):
        pass

    def is_game_over(self):
        pass

    def print_winner(self):
        pass

    def play(self):
        pass


game = TicTacToeGame(root)

root.mainloop()
