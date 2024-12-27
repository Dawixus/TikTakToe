import tkinter as tk            # GUI
import ctypes                   # Better GUI quality
from random import choice       # Random choice for client/server symbol
import socket                   # Network library for communication


class TikTakToeServer:
    def __init__(self):  # Initialize variables for game and network
        self.game_list = None  # Grid representation of the game (3x3)

        # Randomly assign symbol to client and server
        self.client_symbol = choice(['O', 'X'])
        self.server_symbol = "X" if self.client_symbol == "O" else "O"
        self.game_end = False  # Flag to check if the game has ended
        self.start_game_symbol = "X"  # Symbol to start the game with
        self.symbol = "X"  # Current symbol in use for the player

        # Parameters for GUI appearance
        self.label_width = 17
        self.label_height = 8
        self.line_color_x = '#019786'  # Color for 'X' lines
        self.line_color_o = '#ffc006'  # Color for 'O' lines
        self.label_color = '#3d4b61'  # Background color for labels
        self.border_color = '#607c8c'  # Border color for the game grid

        # Game score initialization
        self.x_points, self.o_points = (0, 0)

        # Network-related variables
        self.connection_estabilished = False  # Connection status flag
        self.client_socket = None  # Socket for client communication

        # Initialize the main window for the game
        self.root = tk.Tk()
        self.root.iconbitmap('tiktac.ico')  # Set game window icon
        self.root.resizable(False, False)  # Prevent resizing the window
        self.root.bind("<Escape>", lambda e: (self.root.destroy(), self.send_message("END")))  # Esc closes the window
        ctypes.windll.shcore.SetProcessDpiAwareness(True)  # High DPI awareness for better display quality
        self.setup_window()  # Set up the game window

    def restart(self):
        # Restart the game by sending a restart message to the client
        self.send_message("RES")
        self.setup_window()  # Re-setup window for a new game

    def recieve_message(self):  # Method to listen for incoming messages from the client
        if self.symbol is self.client_symbol and not self.game_end:
            self.client_socket.settimeout(0.1)  # Set a timeout for socket operation
            try:
                server_message = self.client_socket.recv(1024).decode()  # Receive message from client
                if "MOV" in server_message:  # If it's a move command
                    self.play(int(server_message[4]), int(server_message[5]), 2)  # Play the move
            except socket.timeout:
                pass  # Ignore timeout errors
            self.root.after(500, self.recieve_message)  # Retry after 500ms

    def send_message(self, packet):  # Send message to client
        try:
            if not self.connection_estabilished:
                server_socket.settimeout(0.1)  # Set socket timeout before accepting client connection
                self.client_socket, addr = server_socket.accept()  # Accept client connection
                self.connection_estabilished = True  # Mark the connection as established
            server_message = packet  # Set the packet to send
            self.client_socket.send(server_message.encode())  # Send the message to the client
            return True
        except socket.timeout:
            return False  # Return False if there is a timeout

    def set_up_restart_button(self):
        # Setup the restart button for restarting the game
        reset_b = tk.Button(width=self.label_width, height=self.label_height, bg=self.border_color,
                            borderwidth=0, activebackground=self.border_color, command=self.restart)
        reset_l = tk.Label(self.root, text="Retry", font=('Arial', 30, 'bold'), bg=self.border_color,
                           fg=self.label_color)
        reset_l.bind("<Button-1>", lambda e: self.restart())  # Restart on button click
        self.game_end = True  # Mark the game as ended

        # Position the restart button
        for i in self.game_list:
            if 1 in i:
                reset_b.grid(row=self.game_list.index(i) + 1, column=i.index(1))
                reset_l.grid(row=self.game_list.index(i) + 1, column=i.index(1))
                break
            else:
                reset_b.grid(row=2, column=1)  # Default position if no spaces are found
                reset_l.grid(row=2, column=1)

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
                    for i in range(3):
                        diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3,
                                                 width=100)
                        diagonal_line.grid(row=i + 1, column=i)  # Display diagonal line
                return self.handle_win()
            if game_list[0][2] == game_list[1][1] == game_list[2][0] != 1:
                for i in range(3):
                    for i in range(3):
                        diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3,
                                                 width=100)
                        diagonal_line.grid(row=i + 1, column=2 - i)  # Display diagonal line
                return self.handle_win()

            # Check for a draw if all cells are filled
            if all(1 not in row for row in game_list):
                self.set_up_restart_button()

    def handle_win(self):
        # Update the score and handle the win
        if not self.game_end:
            if self.symbol == self.server_symbol:
                self.o_points += 1  # Increment points for server if they win
            else:
                self.x_points += 1  # Increment points for client if they win
        self.set_up_restart_button()

    def play(self, row, column, player=1):
        # Handle a player's move
        symbol = self.symbol
        if player == 1 and symbol == self.server_symbol:
            if not self.send_message(f"MOV{symbol}{row}{column}"):  # Send move to client
                return
        if symbol == "X":
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                    foreground=self.line_color_x, font=('Arial', 70, 'bold'))
        else:
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                    foreground=self.line_color_o, font=('Arial', 70, 'bold'))

        # Check if tile is not used and game is ongoing
        if self.game_list[row - 1][column] == 1 and not self.game_end and (
                player == 1 and symbol == self.server_symbol or player == 2):
            label_symbol.grid(row=row, column=column)  # Place the symbol on the grid
            if symbol == "X":
                self.game_list[row - 1][column] = "X"
            else:
                self.game_list[row - 1][column] = "O"
            self.find_pattern()  # Check for a winner or draw
            self.root.update()  # Update the GUI
            self.recieve_message()  # Wait for client's next move

    def send_starting_message(self):
        # Send starting message to client
        if not self.connection_estabilished:
            message = f"STA{self.client_symbol}"
            if not self.send_message(message):  # Retry if sending fails
                self.root.after(500, self.send_starting_message)
            else:
                self.setup_window()  # Setup window after starting message is sent

    def create_button(self, row, column):
        # Create a new button for each tile in the grid
        return tk.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                         activebackground=self.label_color, command=lambda: self.play(row, column))

    def setup_window(self):
        # Setup the game window, resetting the game and displaying grid buttons
        if self.game_end:
            self.start_game_symbol = "O" if self.start_game_symbol == "X" else "X"
        self.symbol = self.start_game_symbol  # Set starting symbol
        title = f"{'STARTING' if self.symbol == self.server_symbol else ''} {self.x_points} - {self.o_points}"
        if not self.connection_estabilished:
            title = f"{socket.gethostbyname(socket.gethostname())}"  # Show local IP address if not connected
        self.root.title(title)  # Set window title
        self.game_end = False  # Reset game over flag
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # Reset game grid
        if self.connection_estabilished:
            self.recieve_message()  # Start receiving messages if connected
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

        self.send_starting_message()  # Send the starting message to the client
        self.root.mainloop()  # Start the GUI event loop


if __name__ == '__main__':
    # Server socket initialization
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create server socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set socket options
    server_socket.bind(("0.0.0.0", 12345))  # Bind to all available interfaces on port 12345
    server_socket.listen(1)  # Listen for one connection at a time
    a = TikTakToeServer()  # Start the server and initialize the game
