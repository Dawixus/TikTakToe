import tkinter as tk            # GUI
import ctypes                   # Better GUI quality
from random import choice       # Random choice for client/server symbol
import socket                   # Network library for communication


class PlayerVSComputer:
    def __init__(self):
        # Set global variables for game settings
        self.symbol = "X"
        self.player_symbol = "X"
        self.AI_symbol = "O"
        self.label_width = 17
        self.label_height = 8
        self.game_end = False
        self.line_color_x = '#545454'
        self.line_color_o = '#eeeeee'
        self.label_color = '#01B1FF'  # Color of game tiles
        self.border_color = '#019CE0'  # Color of the borders
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # Game grid initialization
        self.x_points = 0
        self.o_points = 0

        # Window setup
        self.root = tk.Tk()
        self.root.iconbitmap('tiktac.ico')  # Set icon for the window
        self.root.resizable(False, False)  # Disable window resizing
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Close on Escape key
        self.root.bind("<space>", lambda e: self.switch_symbols())  # Switch symbols on Space key
        ctypes.windll.shcore.SetProcessDpiAwareness(True)  # Set high-quality DPI
        self.setup_window()  # Initialize game window

    def set_up_restart_button(self):
        # Setup restart button to reset the game
        reset_b = tk.Button(width=self.label_width, height=self.label_height, bg=self.border_color,
                             borderwidth=0, activebackground=self.border_color, command=self.setup_window)
        reset_l = tk.Label(self.root, text="Retry", font=('Arial', 30, 'bold'), bg=self.border_color,
                           fg=self.line_color_o)
        reset_l.bind("<Button-1>", lambda e: self.setup_window())  # Restart on click
        # Place restart button
        self.game_end = True
        for i in self.game_list:
            if 1 in i:
                reset_b.grid(row=self.game_list.index(i) + 1, column=i.index(1))
                reset_l.grid(row=self.game_list.index(i) + 1, column=i.index(1))
                break
            else:
                reset_b.grid(row=2, column=1)
                reset_l.grid(row=2, column=1)

    def switch_symbols(self):
        # Switch between player and AI symbols
        if self.game_list == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]:
            self.player_symbol = "O"
            self.AI_symbol = "X"
            self.second_player_turn()

    def increment_score(self):
        # Increment score based on the winner
        if not self.game_end:
            if self.symbol == self.player_symbol:
                self.o_points += 1
            else:
                self.x_points += 1

    def find_pattern(self):
        # Check for winning or draw conditions
        if not self.game_end:
            game_list = self.game_list
            text_color = self.line_color_x if self.symbol == "X" else self.line_color_o
            self.symbol = "O" if self.symbol == "X" else "X"  # Switch turns

            # Setup label for winning lines
            vertical_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=170, width=7)
            horizontal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=300)
            diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)

            # Check vertical, horizontal, and diagonal lines for a win
            for i, (col1, col2, col3) in enumerate(zip(*game_list)):
                if col1 == col2 == col3 != 1:  # All three cells in a column are the same and not empty
                    vertical_line.grid(row=1, column=i, rowspan=3)  # Display winning line
                    return self.handle_win()

            for b, row in enumerate(game_list):
                if 1 not in row and ("O" not in row or "X" not in row):  # Check horizontal win
                    horizontal_line.grid(row=b + 1, column=0, columnspan=3)
                    return self.handle_win()

            # Check diagonals for a win
            if game_list[0][0] == game_list[1][1] == game_list[2][2] != 1:
                for i in range(3):
                    diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)
                    diagonal_line.grid(row=i + 1, column=i)  # Display diagonal line
                return self.handle_win()
            if game_list[0][2] == game_list[1][1] == game_list[2][0] != 1:
                for i in range(3):
                    diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)
                    diagonal_line.grid(row=i + 1, column=2-i)  # Display diagonal line
                return self.handle_win()

            # Check for a draw if all cells are filled
            if all(1 not in row for row in game_list):
                self.set_up_restart_button()

    def handle_win(self):
        # Update the score and handle the win
        if not self.game_end:
            if self.symbol == self.player_symbol:
                self.o_points += 1  # Increment points for server if they win
            else:
                self.x_points += 1  # Increment points for client if they win
        self.set_up_restart_button()

    def play(self, row, column):
        # Place the player's symbol on the clicked tile
        symbol = self.symbol
        if symbol == "X":
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                     foreground=self.line_color_x, font=('Arial', 70, 'bold'))
        else:
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                     foreground=self.line_color_o, font=('Arial', 70, 'bold'))

        # Check if tile is not already used and game hasn't ended
        if self.game_list[row - 1][column] == 1 and not self.game_end:
            label_symbol.grid(row=row, column=column)
            if symbol == "X":
                self.game_list[row - 1][column] = "X"
            else:
                self.game_list[row - 1][column] = "O"
            self.find_pattern()
            self.root.update()  # Update window
            if self.symbol == self.AI_symbol:
                self.second_player_turn()

    def create_button(self, row, column):
        # Create a button for each tile in the grid
        return tk.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                         activebackground=self.label_color, command=lambda: self.play(row, column))

    def setup_window(self):
        # Initialize the game window with a fresh game state
        self.player_symbol = "X"
        self.AI_symbol = "O"
        title = f"{self.x_points} - {self.o_points}"
        self.root.title(title)
        self.symbol = self.player_symbol
        self.game_end = False
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

        for i in range(3):
            for j in range(3):
                set_up_restart_button = self.create_button(i + 1, j)
                set_up_restart_button.grid(row=i + 1, column=j)

        # Setup borderlines for grid
        def create_label(row, column, rowspan, columnspan, height, width):
            label = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=height, width=width)
            label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)

        create_label(1, 0, 3, 2, 187, 7)
        create_label(1, 1, 3, 2, 187, 7)
        create_label(1, 0, 2, 3, 3, 369)
        create_label(2, 0, 2, 3, 3, 369)

        # Launch the window
        self.root.mainloop()

    def second_player_turn(self):
        # Determine the best move for the AI player using minimax algorithm
        def is_winner(board, player):
            # Check rows, columns, and diagonals for a winner
            for i in range(3):
                if all(board[i][j] == player for j in range(3)):  # Rows
                    return True
                if all(board[j][i] == player for j in range(3)):  # Columns
                    return True
            if all(board[i][i] == player for i in range(3)):  # Diagonal \
                return True
            if all(board[i][2 - i] == player for i in range(3)):  # Diagonal /
                return True
            return False

        def is_draw(board):
            # Check if there are no empty cells
            return all(board[i][j] != 1 for i in range(3) for j in range(3))

        def minimax(board, depth, is_maximizing):
            # Minimax algorithm for optimal AI move
            if is_winner(board, self.AI_symbol):  # AI win
                return 10 - depth
            if is_winner(board, self.player_symbol):  # Player win
                return depth - 10
            if is_draw(board):  # Draw
                return 0

            if is_maximizing:
                max_eval = -float("inf")
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == 1:  # Empty cell
                            board[i][j] = self.AI_symbol
                            eval = minimax(board, depth + 1, False)
                            board[i][j] = 1
                            max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float("inf")
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == 1:  # Empty cell
                            board[i][j] = self.player_symbol
                            eval = minimax(board, depth + 1, True)
                            board[i][j] = 1
                            min_eval = min(min_eval, eval)
                return min_eval

        def best_move():
            best_val = -float("inf")
            move = None
            for i in range(3):
                for j in range(3):
                    if self.game_list[i][j] == 1:  # Empty cell
                        self.game_list[i][j] = self.AI_symbol
                        move_val = minimax(self.game_list, 0, False)
                        self.game_list[i][j] = 1
                        if move_val > best_val:
                            best_val = move_val
                            move = (i, j)
            return move

        # AI makes the best move
        if self.game_list != [[1, 1, 1], [1, 1, 1], [1, 1, 1]]:
            move = best_move()
        else:
            move = (choice([0, 2]), choice([0, 2]))
        self.play(move[0] + 1, move[1])


if __name__ == '__main__':
    a = PlayerVSComputer()