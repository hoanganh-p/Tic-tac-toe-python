import tkinter as tk
from tkinter import ttk
import os

from vscomputer import vscomputer
from vsplayer import client


class Home:
    def __init__(self, master):
        self.master = master

        self.master.title("Tic Tac Toe")
        self.master.geometry("500x400+400+150")
        self.master.config()

        self.label = ttk.Label(master, text="Tic Tac Toe", font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Tạo các nút
        self.button_1player = ttk.Button(
            master,
            text="Vs. Computer",
            width=15,
            style="Accent.TButton",
            command=self.vs_computer
        )
        self.button_2player = ttk.Button(
            master,
            text="Vs. Player",
            width=15,
            style="Accent.TButton",
            command=self.vs_player
        )
        self.button_1player.pack(pady=25)
        self.button_2player.pack(pady=25)

    def vs_computer(self):
        self.master.withdraw()
        top = tk.Toplevel()
        vscomputer.VsComputer(top)

    def vs_player(self):
        self.master.withdraw()
        top = tk.Toplevel()
        client.Client(top)

def main():
    root = tk.Tk()
    game = Home(root)

    style = ttk.Style(root)
    current_file_path = os.path.dirname(__file__)
    path = os.path.join(current_file_path, "forest-dark.tcl")
    root.tk.call("source", path)
    style.theme_use("forest-dark")

    root.mainloop()


if __name__ == "__main__":
    main()
