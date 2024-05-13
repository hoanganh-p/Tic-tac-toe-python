import os
import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk

dirname = os.path.dirname(os.path.dirname(__file__))
import sys

sys.path.append(dirname)


class VsComputer:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.board = [" " for _ in range(9)]
        self.difficulty = "Medium"
        self.turn = "X"
        self.player_win_count = 0
        self.computer_win_count = 0
        self.draw_count = 0

        self.create_widgets()

        if self.player_symbol == "O":
            self.random_first_move()

    def back(self):
        import home

        self.master.withdraw()
        home.main()

    def set_turn(self, turn):
        self.turn = turn
        txt = "Your turn" if self.player_symbol == self.turn else "Computer's turn"
        self.turn_label.config(text=txt)
        # self.master.update()
        self.master.update_idletasks()

    def set_difficulty(self, event=None):
        self.difficulty = self.difficulty_cbb.get()
        self.reset_board()

    def swap_symbol(self):
        self.player_symbol, self.computer_symbol = (
            self.computer_symbol,
            self.player_symbol,
        )
        self.symbol_label.config(text="Symbol: " + self.player_symbol)

        self.reset_board()

    def reset_board(self):
        for i in range(9):
            self.broad_buttons[i].config(text="", bg="white")
            self.board[i] = " "

        # Cập nhật lại lượt đi khi reset
        self.set_turn("X")

        if self.player_symbol == "O":
            self.random_first_move()

    def on_click(self, row, col):
        if self.turn == self.player_symbol:
            index = row * 3 + col
            if self.board[index] == " ":
                color = "blue" if self.player_symbol == "X" else "red"
                self.broad_buttons[index].config(text=self.player_symbol, fg=color)
                self.board[index] = self.player_symbol
                self.set_turn(self.computer_symbol)

                if self.check_winner(self.player_symbol):
                    self.highlight_winning(self.player_symbol)
                    self.set_win_count("Win")
                    messagebox.showinfo("Congratulations!", "You wins!\t")
                    self.reset_board()
                elif " " not in self.board:
                    self.set_win_count("Draw")
                    messagebox.showinfo("Draw!", "It's a draw!")
                    self.reset_board()
                else:
                    self.master.after(500, self.computer_move)

    def random_first_move(self):
        index = random.randint(0, 8)
        color = "blue" if self.computer_symbol == "X" else "red"
        self.broad_buttons[index].config(text=self.computer_symbol, fg=color)
        self.board[index] = self.computer_symbol
        self.set_turn("O")

    def computer_move(self):
        if self.difficulty == "Easy":
            index = self.get_random_move()
        elif self.difficulty == "Medium":
            index = self.get_medium_move()
        else:  # Hard
            index = self.get_best_move()

        color = "blue" if self.computer_symbol == "X" else "red"
        self.broad_buttons[index].config(text=self.computer_symbol, fg=color)
        self.board[index] = self.computer_symbol
        self.set_turn(self.player_symbol)

        if self.check_winner(self.computer_symbol):
            self.highlight_winning(self.computer_symbol)
            self.set_win_count("Lose")
            messagebox.showinfo("Game Over!", "The computer wins!")
            self.reset_board()
        elif " " not in self.board:
            self.set_win_count("Draw")
            messagebox.showinfo("Draw!", "It's a draw!")
            self.reset_board()

    def get_random_move(self):
        empty_indices = [i for i, val in enumerate(self.board) if val == " "]
        return random.choice(empty_indices)

    def get_medium_move(self):
        best_score = -1
        best_move = None
        for i in range(9):
            if self.board[i] == " ":

                score = self.evaluate_move(i)
                if score >= best_score:
                    if score > best_score:
                        best_score = score
                        best_move = i
                    else:
                        best_score = random.choice([score, best_score])
                        best_move = random.choice([i, best_move])
        return best_move

    def evaluate_move(self, index):
        player = self.player_symbol
        computer = self.computer_symbol

        self.board[index] = computer
        if self.check_winner(computer):
            self.board[index] = " "
            return 2
        
        self.board[index] = player
        if self.check_winner(player):
            self.board[index] = " "
            return 1
        self.board[index] = " "
        return 0

    def get_best_move(self):
        best_score = -float("inf")
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.computer_symbol
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner(self.player_symbol, board)
        if result:
            return -1
        result = self.check_winner(self.computer_symbol, board)
        if result:
            return 1
        if " " not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.computer_symbol
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.player_symbol
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player, board=None):
        if board is None:
            board = self.board
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for combo in winning_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False

    def highlight_winning(self, winner):
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for combo in winning_combinations:
            if all(self.board[i] == winner for i in combo):
                for index in combo:
                    self.broad_buttons[index].config(bg="#217346")
                break

    def set_win_count(self, marker):
        if marker == "Win":
            self.player_win_count += 1
            self.win_count_player_lb.config(
                text="Player: " + str(self.player_win_count) + "\t\t"
            )
        elif marker == "Lose":
            self.computer_win_count += 1
            self.win_count_computer_lb.config(
                text="Computer: " + str(self.computer_win_count) + "\t\t"
            )
        else:
            self.draw_count += 1
            self.draw_count_lb.config(text="Draw: " + str(self.draw_count) + "\t\t")

    def create_icon(self, img):
        filename = os.path.join(dirname, img)
        image = Image.open(filename)
        image = image.resize((20, 20))
        icon = ImageTk.PhotoImage(image)
        label = tk.Label(self.master, image=icon)
        label.image = icon  # Giữ tham chiếu đến hình ảnh
        return icon

    def create_widgets(self):
        # Nút back
        icon = self.create_icon(r"imgs/back-icon.png")
        self.back_button = ttk.Button(
            self.master, image=icon, style="Accent.TButton", command=self.back
        )
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Top frame
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=(30, 0), padx=(0, 130))
        # Chọn mức độ
        self.difficulty_label = tk.Label(
            self.top_frame, text="Difficulty:", font=("Arial", 12)
        )
        self.difficulty_label.grid(row=0, column=0, sticky="nsew")
        self.difficulty_cbb = ttk.Combobox(
            self.top_frame,
            values=["Easy", "Medium", "Hard"],
            font=("Arial", 11),
            state="readonly",
        )
        self.difficulty_cbb.set("Medium")
        self.difficulty_cbb.bind("<<ComboboxSelected>>", self.set_difficulty)
        self.difficulty_cbb.grid(row=0, column=1, sticky="nsew")
        # Chọn phe
        self.symbol_label = tk.Label(
            self.top_frame, text="Symbol: " + self.player_symbol, font=("Arial", 12)
        )
        self.symbol_label.grid(row=0, column=2, padx=(220, 25), sticky="nsew")
        icon = self.create_icon(r"imgs/swap-icon.png")
        self.swap_symbol_button = ttk.Button(
            self.top_frame,
            image=icon,
            style="Accent.TButton",
            command=self.swap_symbol,
        )
        self.swap_symbol_button.grid(row=0, column=3, padx=(0, 0), sticky="nsew")

        # Label hiển thị lượt đi
        txt = "Your turn" if self.player_symbol == self.turn else "Computer's turn"
        self.turn_label = tk.Label(self.master, text=txt, font=("Arial", 20))
        self.turn_label.pack(pady=(50, 0))

        # Mid frame
        self.mid_frame = tk.Frame(self.master)
        self.mid_frame.pack(padx=50)
        # Hiển thị bảng
        self.broad_frame = tk.Frame(self.mid_frame)
        self.broad_frame.pack(side="left", padx=(275, 0))
        self.broad_buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.broad_frame,
                    text="",
                    font=("Arial", 45),
                    width=3,
                    height=1,
                    bg="white",
                    # relief="groove",
                    command=lambda row=i, col=j: self.on_click(row, col),
                )
                button.grid(row=i, column=j, sticky="nsew")
                self.broad_buttons.append(button)

        # Đếm số trận thắng
        self.win_count_frame = ttk.LabelFrame(
            self.mid_frame, text="Win count", padding=(20, 10)
        )
        self.win_count_frame.pack(side="right", padx=(50, 0))
        # Player win
        self.win_count_player_lb = ttk.Label(
            self.win_count_frame, text="You: " + str(self.player_win_count) + "\t\t"
        )
        self.win_count_player_lb.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        # Computer win
        self.win_count_computer_lb = ttk.Label(
            self.win_count_frame,
            text="Computer: " + str(self.computer_win_count) + "\t\t",
        )
        self.win_count_computer_lb.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        # Draw
        self.draw_count_lb = ttk.Label(
            self.win_count_frame, text="Draw: " + str(self.draw_count) + "\t\t"
        )
        self.draw_count_lb.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        # Nút reset
        self.reset_button = ttk.Button(
            self.master,
            text="Reset",
            style="Accent.TButton",
            command=self.reset_board,
        )
        self.reset_button.pack(side="bottom", pady=30)

        self.master.geometry("+200+10")


def main():
    root = tk.Tk()
    game = VsComputer(root)

    style = ttk.Style(root)
    path = os.path.join(dirname, r"themes/forest-dark.tcl")
    root.tk.call("source", path)
    style.theme_use("forest-dark")

    root.mainloop()


if __name__ == "__main__":
    main()
