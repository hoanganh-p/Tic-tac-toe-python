import tkinter as tk
from tkinter import ttk
import os

dirname = os.path.dirname(__file__)
import sys

sys.path.append(dirname)

from vs_computer import vs_computer
from vs_player import client


class Home:
    def __init__(self, master):
        self.master = master

        self.master.title("Tic Tac Toe")
        self.master.geometry("700x500+350+100")

        self.label = ttk.Label(master, text="Tic Tac Toe", font=("Helvetica", 35))
        self.label.pack(pady=50)

        # Tạo các nút
        self.button_1player = ttk.Button(
            master,
            text="Vs. Computer",
            width=15,
            style="Accent.TButton",
            command=self.vs_computer,
        )
        self.button_2player = ttk.Button(
            master,
            text="Vs. Player",
            width=15,
            style="Accent.TButton",
            command=self.vs_player,
        )
        self.button_1player.pack(pady=25)
        self.button_2player.pack(pady=25)

    def vs_computer(self):
        self.master.withdraw()
        top = tk.Toplevel()
        vs_computer.VsComputer(top)

    def vs_player(self):
        self.master.withdraw()
        top = tk.Toplevel()
        client.Client(top)


def main():
    root = tk.Tk()
    game = Home(root)

    style = ttk.Style(root)
    path = os.path.join(dirname, r"themes/forest-dark.tcl")
    root.tk.call("source", path)
    style.theme_use("forest-dark")

    root.mainloop()


if __name__ == "__main__":
    main()
