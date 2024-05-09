import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket
import threading


class Client:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.symbol = "X"
        self.board = [" " for _ in range(9)]
        self.difficulty = "Medium"
        self.turn = "X"
        self.player1_win_count = 0
        self.player2_win_count = 0
        self.draw_count = 0

        self.create_widgets()

        self.host = "192.168.56.1"
        self.port = 4444
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        # Thread nhận dữ liệu
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

    def back(self):
        import home

        self.master.withdraw()
        home.main()

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.choice_label.config(text="Symbol: " + symbol)

    def set_turn(self, turn):
        self.turn = turn

        txt = "Your turn" if self.symbol == self.turn else "Opponent's turn"
        self.turn_label.config(text=txt)
        # self.master.update()
        self.master.update_idletasks()

    def reset_board(self):
        for i in range(9):
            self.broad_buttons[i].config(text="", bg="white")
            self.board[i] = " "

        self.swap_symbol_button.config(state="normal")

        # Cập nhật lại lượt đi khi reset
        self.set_turn("X")

    def on_click(self, symbol, row, col):
        if self.turn == self.symbol:
            self.draw_board(symbol, row, col)
            self.send_data((symbol, row, col))

    def draw_board(self, symbol, row, col):
        self.swap_symbol_button.config(state="disable")
        index = row * 3 + col
        if self.board[index] == " ":
            color = "blue" if symbol == "X" else "red"
            self.broad_buttons[index].configure(text=symbol, fg=color)
            self.board[index] = symbol

            if self.check_winner(symbol):
                self.highlight_winning(symbol)
                text = "You win!" if symbol == self.symbol else "You lose!"
                messagebox.showinfo("Game over!", text)
                if symbol == self.symbol:
                    self.set_win_count("Win")
                else:
                    self.set_win_count("Lose")
                self.reset_board()
            elif " " not in self.board:
                messagebox.showinfo("Draw!", "It's a draw!")
                self.set_win_count("Draw")
                self.reset_board()
            else:
                turn = "O" if symbol == "X" else "X"
                self.set_turn(turn)

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
            self.player1_win_count += 1
            self.win_count_player1_lb.config(
                text="Player1(You): " + str(self.player1_win_count) + "\t\t"
            )
        elif marker == "Lose":
            self.player2_win_count += 1
            self.win_count_player2_lb.config(
                text="Player2: " + str(self.player2_win_count) + "\t\t"
            )
        else:
            self.draw_count += 1
            self.draw_count_lb.config(text="Draw: " + str(self.draw_count) + "\t\t")

    def receive_data(self):
        # Nhận dữ liệu từ server để xác định ký tự của client là "X" hay "O"
        self.symbol = self.client_socket.recv(1024).decode()
        if self.symbol == "O":
            self.set_symbol("O")
            self.set_turn("X")

        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break
            # data = data.decode()
            if data == "SwapSymbol":
                # Nếu nhận được yêu cầu thay đổi ký tự từ server
                confirm = messagebox.askyesno(
                    "Swap Symbol", "Player2 wants to swap symbol. Do you accept?"
                )
                if confirm:
                    # Nếu người chơi đồng ý, gửi phản hồi "Accept" cho server
                    self.client_socket.sendall("Accept".encode())
                    symbol = "X" if self.symbol == "O" else "O"
                    self.set_symbol(symbol)
                    self.set_turn("X")

            elif data == "Accept":
                symbol = "X" if self.symbol == "O" else "O"
                self.set_symbol(symbol)
                self.set_turn("X")

            else:
                # Nếu nhận được dữ liệu trò chơi
                choice, row, col = map(str, data.split(","))
                self.draw_board(choice, int(row), int(col))

    def send_data(self, data):
        message = ",".join(map(str, data))
        self.client_socket.sendall(message.encode())

    # Phương thức để thay đổi ký tự "X" và "O"
    def request_swap_symbol(self):
        confirm = messagebox.askyesno("Swap Symbol", "Do you want swap symbol?")
        if confirm:
            self.client_socket.sendall("SwapSymbol".encode())

    def create_widgets(self):
        # Nút back
        self.back_button = ttk.Button(
            self.master, text="Back", style="Accent.TButton", command=self.back
        )
        self.back_button.pack(anchor="nw", padx=10, pady=10)

        # Label hiển thị lượt đi
        # txt = "Your turn" if self.symbol == "X" else "Opponent's turn"
        self.turn_label = tk.Label(self.master, text="Your turn", font=("Arial", 20))
        self.turn_label.pack(anchor="w", fill="x", padx=(0, 270), pady=(30, 10))

        # Mid frame
        self.mid_frame = tk.Frame(self.master)
        self.mid_frame.pack(padx=50)
        # Hiển thị bảng
        self.broad_frame = tk.Frame(self.mid_frame)
        self.broad_frame.pack(ipadx=25)
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
                    command=lambda row=i, col=j: self.on_click(self.symbol, row, col),
                )
                button.grid(row=i, column=j, sticky="nsew")
                self.broad_buttons.append(button)

        # Right-mid frame
        self.right_mid_frame = tk.Frame(self.master)
        self.right_mid_frame.pack(side="right", before=self.broad_frame)

        # Chọn phe
        self.choice_frame = tk.Frame(self.right_mid_frame)
        self.choice_frame.pack(ipady=20, anchor="w")

        self.choice_label = tk.Label(
            self.choice_frame, text="Symbol: " + self.symbol, font=("Arial", 12)
        )
        self.choice_label.grid(row=0, column=1, sticky="nsew")
        # Nút swap phe
        self.swap_symbol_button = ttk.Button(
            self.choice_frame,
            text="Swap",
            style="Accent.TButton",
            command=self.request_swap_symbol,
        )
        self.swap_symbol_button.grid(row=0, column=2, padx=(50, 0), sticky="nsew")

        # Hiển thị số trận thắng
        self.win_count_frame = ttk.LabelFrame(
            self.right_mid_frame, text="Win count", padding=(20, 10)
        )
        self.win_count_frame.pack()
        # Player win
        self.win_count_player1_lb = ttk.Label(
            self.win_count_frame,
            text="Player1(You): " + str(self.player1_win_count) + "\t\t",
        )
        self.win_count_player1_lb.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        # Computer win
        self.win_count_player2_lb = ttk.Label(
            self.win_count_frame,
            text="Player2: " + str(self.player2_win_count) + "\t\t",
        )
        self.win_count_player2_lb.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
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
        self.reset_button.pack(pady=(30, 50))


if __name__ == "__main__":
    root = tk.Tk()
    client = Client(root)

    style = ttk.Style(root)
    current_file_path = os.path.abspath(__file__)
    path = os.path.join(
        os.path.dirname(os.path.dirname(current_file_path)), "forest-dark.tcl"
    )
    root.tk.call("source", path)
    style.theme_use("forest-dark")

    root.mainloop()
