import tkinter as tk            # Import Tkinter for GUI creation
import ctypes                   # Import ctypes to improve GUI quality with high DPI awareness
import socket                   # Import socket for network communication between client and server


def send_message(packet):
    try:
        server_socket.settimeout(1)  # Set a timeout for the socket connection
        server_message = packet  # Prepare the message to send
        server_socket.send(server_message.encode())  # Send the message over the network
        return True  # Indicate the message was sent successfully
    except socket.timeout:
        return False  # If the socket times out, return False


class TikTakToeClient:
    def __init__(self):
        # Initialize global variables for the game
        self.AI_symbol = "O"  # AI's symbol
        self.player_symbol = "X"  # Player's symbol
        self.start_game_symbol = "X"  # Symbol to start the game with
        self.game_end = False  # Flag to indicate if the game has ended
        self.symbol = "X"  # Current player's symbol
        self.label_width = 17  # Width of each label in the grid
        self.label_height = 8  # Height of each label in the grid
        self.line_color_x = '#019786'  # Line color for X
        self.line_color_o = '#ffc006'  # Line color for O
        self.label_color = '#3d4b61'  # Background color for labels
        self.border_color = '#607c8c'  # Border color for the grid
        self.x_points = 0  # Player X's score
        self.o_points = 0  # Player O's score
        self.client_socket = None  # Socket for network communication

        # Window setup (Tkinter GUI)
        self.root = tk.Tk()  # Create the main window
        self.root.iconbitmap('tiktac.ico')  # Set window icon
        self.root.resizable(False, False)  # Disable window resizing
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Bind Escape key to close the window
        ctypes.windll.shcore.SetProcessDpiAwareness(True)  # Set high-quality DPI settings for the window
        self.setup_window()  # Initialize the window setup (method to be defined later)

    def set_up_restart_button(self):
        self.game_end = True

    def recieve_message(self):
        if self.symbol == self.player_symbol or self.game_end:  # Check if it's the player's turn or the game has ended
            server_socket.settimeout(0.1)  # Set a timeout for the socket
            try:
                server_message = server_socket.recv(1024).decode()  # Receive message from server
                if "RES" in server_message:  # Check if the message is a reset command
                    self.setup_window()  # Reset the window for a new game
                elif "END" in server_message:  # If the message indicates the game has ended
                    self.root.destroy()  # Close the game window
                elif "MOV" in server_message:  # If the message is a move, update the game
                    self.play(int(server_message[4]), int(server_message[5]), 2)  # Play the move
                elif "STA" in server_message:  # If the message indicates the game status
                    self.AI_symbol = server_message[3]  # Set the AI symbol
                    self.player_symbol = "X" if self.AI_symbol == "O" else "O"  # Set the player's symbol based on AI's symbol
                    self.setup_window()
            except socket.timeout:
                pass  # Ignore timeout exceptions
            self.root.after(500, self.recieve_message)  # Call this function every 500ms to continue listening for messages

    def find_pattern(self):
        if not self.game_end:
            game_list = self.game_list
            text_color = self.line_color_x if self.symbol == "X" else self.line_color_o
            self.symbol = "O" if self.symbol == "X" else "X"  # Switch the symbol after each turn

            # Setup line labels for displaying winning lines
            vertical_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=170, width=7)
            horizontal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=300)
            diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)

            # Check for vertical winning line
            for i, (col1, col2, col3) in enumerate(zip(*game_list)):
                if col1 == col2 == col3 != 1:  # Check if all values in the column are equal and not empty
                    vertical_line.grid(row=1, column=i, rowspan=3)  # Display the winning line
                    return self.handle_win()  # Handle the win condition

            # Check for horizontal winning line
            for b, row in enumerate(game_list):
                if 1 not in row and ("O" not in row or "X" not in row):  # Check if the row is completely filled
                    horizontal_line.grid(row=b + 1, column=0, columnspan=3)  # Display the winning line
                    return self.handle_win()  # Handle the win condition

            # Check for diagonal winning line
            if game_list[0][0] == game_list[1][1] == game_list[2][2] != 1:
                for i in range(3):
                    diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)
                    diagonal_line.grid(row=i + 1, column=i)  # Display diagonal line
                return self.handle_win()
            if game_list[0][2] == game_list[1][1] == game_list[2][0] != 1:
                for i in range(3):
                    diagonal_line = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=3, width=100)
                    diagonal_line.grid(row=i + 1, column=2 - i)  # Display diagonal line
                return self.handle_win()

            # Check for a draw if no empty spaces are left
            if all(1 not in row for row in game_list):
                self.set_up_restart_button()  # Set up the restart button if the game is a draw

    def handle_win(self):
        if not self.game_end:
            if self.symbol == self.player_symbol:
                self.o_points += 1  # Player O scores
            else:
                self.x_points += 1  # Player X scores
        self.set_up_restart_button()  # Set up the restart button

    def play(self, row, column, player=1):
        symbol = self.symbol
        if player == 1 and symbol == self.AI_symbol:
            if not send_message(f"MOV{symbol}{row}{column}"):  # Send the move to the server
                return
        # Create the label for the symbol in the grid
        if symbol == "X":
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                    foreground=self.line_color_x, font=('Arial', 70, 'bold'))
        else:
            label_symbol = tk.Label(self.root, text=self.symbol, background=self.label_color,
                                    foreground=self.line_color_o, font=('Arial', 70, 'bold'))

        # Check if the cell is available and the game hasn't ended
        if self.game_list[row - 1][column] == 1 and not self.game_end and (
                player == 1 and symbol == self.AI_symbol or player == 2):
            label_symbol.grid(row=row, column=column)  # Place the symbol in the grid
            if symbol == "X":
                self.game_list[row - 1][column] = "X"
            else:
                self.game_list[row - 1][column] = "O"
            self.find_pattern()  # Check for a winning pattern after placing the symbol
            self.root.update()  # Update the window to reflect changes
            self.recieve_message()  # Load the latest server message

    def create_button(self, row, column):
        return tk.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                         activebackground=self.label_color, command=lambda: self.play(row, column))

    def setup_window(self):
        if self.game_end:
            if self.start_game_symbol == "X":
                self.start_game_symbol = "O"  # Switch starting symbol if the game has ended
            else:
                self.start_game_symbol = "X"
        self.symbol = self.start_game_symbol  # Set the starting symbol
        self.recieve_message()  # Start reading messages from the server
        title = f"{'STARTING' if self.symbol == self.AI_symbol else ''} {self.x_points} - {self.o_points}"
        self.root.title(title)  # Set the window title
        self.game_end = False  # Reset the game state
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # Initialize the game grid

        # Create buttons for the Tic-Tac-Toe grid
        for i in range(3):
            for j in range(3):
                button = self.create_button(i + 1, j)
                button.grid(row=i + 1, column=j)

        # Setup borderlines
        def create_label(row, column, rowspan, columnspan, height, width):
            label = tk.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=height, width=width)
            label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)

        create_label(1, 0, 3, 2, 187, 7)
        create_label(1, 1, 3, 2, 187, 7)
        create_label(1, 0, 2, 3, 3, 369)
        create_label(2, 0, 2, 3, 3, 369)

        # Launch the window
        self.root.mainloop()


if __name__ == '__main__':
    # Create and configure the server socket
    server_address = str(input("Zadejte IP adresu cíle ve formátu X.X.X.X:\n"))  # Prompt for server IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the server socket
    server_ip = server_address  # Set the server IP address
    server_port = 12345  # Set the server port number
    try:
        server_socket.connect((server_ip, server_port))  # Attempt to connect to the server
        a = TikTakToeClient()  # Initialize the game client if connected successfully
    except (ConnectionRefusedError, TimeoutError):
        print("Cíl není dostupný")  # Print message if the connection is refused or times out
    except socket.gaierror:
        print("Špatně jste zadal IP adresu")  # Print message if the IP address is invalid
