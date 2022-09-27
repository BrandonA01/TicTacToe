from tkinter import *
from Space import Space


class TicTacToeBoard(Space):

    def __init__(self, tk, player):
        self.player = player
        self.play_area = Frame(tk, width=300, height=300, bg='white')
        self.cells = []
        self.generateSpaces()

    def generateSpaces(self):
        for x in range(1, 4):
            for y in range(1, 4):
                self.cells.append(Space(x, y, self.play_area, self.player))
        self.play_area.pack(pady=10, padx=10)

    def resetSpaces(self):
        for i in range(0, len(self.cells)):
            self.cells[i].reset()
