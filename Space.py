import tkinter as tk


class Space:

    def __init__(self, x, y, play_area, value):
        super().__init__()
        self.x = x
        self.y = y
        self.value = None
        self.button = tk.Button(play_area, text="", width=10, height=5, command=lambda: self.onClick(value), bg='white')
        self.button.grid(row=x, column=y)

    def reset(self):
        self.button.configure(text="", bg='white', state=tk.ACTIVE)
        self.value = None

    def onClick(self, value):
        self.button.configure(text=value, bg='white', state=tk.DISABLED)
        self.value = value
