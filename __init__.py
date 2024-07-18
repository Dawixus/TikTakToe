# ---------------------------------- IMPORTS ---------------------------------------------------------------------------

import tkinter  # GUI
import ctypes  # GUI quality handler
import random  # Random


# ------------------------------------ APP -----------------------------------------------------------------------------

class GameAI:
    def __init__(self):
        # Set global variables
        self.symbol = "X"
        self.label_width = 17
        self.label_height = 8
        self.game_end = False
        self.line_color_x = '#545454'
        self.line_color_o = '#eeeeee'
        self.label_color = '#01B1FF'  # #fc210d
        self.border_color = '#019CE0'  # #ba0b02
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.x_points = 0
        self.o_points = 0

        # Window setup
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.iconbitmap("tiktak.ico")
        ctypes.windll.shcore.SetProcessDpiAwareness(True)  # Set good quality
        self.WindowSetup()

    def button(self):
        # Setup restart button
        reset_b = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.border_color,
                                 borderwidth=0,
                                 activebackground=self.border_color, command=self.WindowSetup)
        reset_l = tkinter.Label(self.root, text="Retry", font=('Arial', 30, 'bold'), bg=self.border_color,
                                fg=self.line_color_o)
        reset_l.bind("<Button-1>", lambda e: self.WindowSetup())
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

    def Plus_one(self):
        # Score
        if not self.game_end:
            if self.symbol == "X":
                self.o_points += 1
            else:
                self.x_points += 1

    def Find_Patern(self):
        # Check if someone has won
        if not self.game_end:
            game_list = self.game_list
            if self.symbol == "X":
                text_color = self.line_color_x
                self.symbol = "O"
            else:
                text_color = self.line_color_o
                self.symbol = "X"

            # Setup cross lines
            vertical_line = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, height=170, width=7)
            horizontal_line = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, width=300, height=3)

            # Check for vertical line
            a = 0
            for i, j, q in zip(game_list[0], game_list[1], game_list[2]):
                if i == j == q != 1:
                    vertical_line.grid(row=1, column=a, rowspan=3)
                    self.Plus_one()
                    self.button()
                a += 1
            # Check for horizontal line
            b = 1
            for i in game_list:
                if 1 not in i and ("O" not in i or "X" not in i):
                    horizontal_line.grid(row=b, column=0, columnspan=3)
                    self.Plus_one()
                    self.button()
                b += 1
            # Check for diagonal line
            if game_list[0][0] == game_list[1][1] == game_list[2][2] != 1:
                for i in range(3):
                    diagonal_line = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, width=100,
                                                  height=3)
                    diagonal_line.grid(row=i + 1, column=i)
                self.Plus_one()
                self.button()
            if game_list[0][2] == game_list[1][1] == game_list[2][0] != 1:
                for i in range(3):
                    diagonal_line = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=text_color, width=100,
                                                  height=3)
                    diagonal_line.grid(row=i + 1, column=2 - i)
                self.Plus_one()
                self.button()
            # In case of draw
            if 1 not in self.game_list[0] and 1 not in self.game_list[1] and 1 not in self.game_list[2]:
                self.button()

    def Click(self, row, column):
        # Write symbol on tile on click
        symbol = self.symbol
        if symbol == "X":
            label_symbol = tkinter.Label(self.root, text=self.symbol, background=self.label_color,
                                         foreground=self.line_color_x, font=('Arial', 70, 'bold'))
        else:
            label_symbol = tkinter.Label(self.root, text=self.symbol, background=self.label_color,
                                         foreground=self.line_color_o, font=('Arial', 70, 'bold'))

        # Check if tile isn't already used and game hasn't ended
        if self.game_list[row - 1][column] == 1 and not self.game_end:
            label_symbol.grid(row=row, column=column)
            if symbol == "X":
                self.game_list[row - 1][column] = "X"
            else:
                self.game_list[row - 1][column] = "O"
            self.Find_Patern()
            self.root.update()  # Load window
            if self.symbol == "O":
                self.SecondPlayer()

    def WindowSetup(self):
        title = f"{self.x_points} - {self.o_points}"
        self.root.title(title)
        self.symbol = "X"
        self.game_end = False
        self.game_list = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

        # Setup buttons
        L1 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(1, 0))
        L2 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(1, 1))
        L3 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(1, 2))
        C1 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(2, 0))
        C2 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(2, 1))
        C3 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(2, 2))
        D1 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(3, 0))
        D2 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(3, 1))
        D3 = tkinter.Button(width=self.label_width, height=self.label_height, bg=self.label_color, borderwidth=0,
                            activebackground=self.label_color, command=lambda: self.Click(3, 2))

        # Setup borderlines
        V1 = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=187, width=7)
        V2 = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=187, width=7)
        H1 = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=3, width=369)
        H2 = tkinter.Label(self.root, font=('Arial', 1, 'bold'), bg=self.border_color, height=3, width=369)

        # Place the buttons
        L1.grid(row=1, column=0)
        L2.grid(row=1, column=1)
        L3.grid(row=1, column=2)
        C1.grid(row=2, column=0)
        C2.grid(row=2, column=1)
        C3.grid(row=2, column=2)
        D1.grid(row=3, column=0)
        D2.grid(row=3, column=1)
        D3.grid(row=3, column=2)

        # Place borderlines
        V1.grid(row=1, column=0, rowspan=3, columnspan=2)
        V2.grid(row=1, column=1, rowspan=3, columnspan=2)
        H1.grid(row=1, column=0, rowspan=2, columnspan=3)
        H2.grid(row=2, column=0, rowspan=2, columnspan=3)

        # Launch window
        self.root.mainloop()

    # ###################################### AI ############################################################################
    def SecondPlayer(self):
        game_list = self.game_list
        diagonal_listA = (game_list[0][0], game_list[1][1], game_list[2][2])
        diagonal_listB = (game_list[0][2], game_list[1][1], game_list[2][0])
        # ###################################### WIN ###########################################################################
        # Check for horizontal line
        row = 0
        for i in game_list:
            if i.count("O") == 2 and 1 in i:
                self.Click(row + 1, i.index(1))
                return
            row += 1
        # Check for vertical line
        column = 0
        for i, j, q in zip(game_list[0], game_list[1], game_list[2]):
            if (i, j, q).count("O") == 2 and 1 in (i, j, q):
                self.Click((i, j, q).index(1) + 1, column)
                return
            column += 1
        # Check for diagonal line right
        if diagonal_listA.count("O") == 2 and 1 in diagonal_listA:
            self.Click(diagonal_listA.index(1) + 1, diagonal_listA.index(1))
            return
        # Check for diagonal line left
        if diagonal_listB.count("O") == 2 and 1 in diagonal_listB:
            self.Click(diagonal_listB.index(1) + 1, 2 - diagonal_listB.index(0))
            return
        # ################################## BLOCK ENEMY #######################################################################
        # Check for horizontal line
        row = 0
        for i in game_list:
            if i.count("X") == 2 and 1 in i:
                self.Click(row + 1, i.index(1))
                return
            row += 1
        # Check for vertical line
        column = 0
        for i, j, q in zip(game_list[0], game_list[1], game_list[2]):
            if (i, j, q).count("X") == 2 and 1 in (i, j, q):
                self.Click((i, j, q).index(1) + 1, column)
                return
            column += 1
        # Check for diagonal line right
        if diagonal_listA.count("X") == 2 and 1 in diagonal_listA:
            self.Click(diagonal_listA.index(1) + 1, diagonal_listA.index(1))
            return
        # Check for diagonal line left
        if diagonal_listB.count("X") == 2 and 1 in diagonal_listB:
            self.Click(diagonal_listB.index(1) + 1, 2 - diagonal_listB.index(1))
            return
        # ################################## MAKE ROW ##########################################################################
        # Check for horizontal line
        row = 0
        for i in game_list:
            if i.count("O") == 1 and i.count("X") == 0:
                self.Click(row + 1, abs(i.index("O") - 1))
                return
            row += 1
        # Check for vertical line
        column = 0
        for i, j, q in zip(game_list[0], game_list[1], game_list[2]):
            if (i, j, q).count("O") == 1 and "X" not in (i, j, q):
                self.Click(abs((i, j, q).index(1)) + 1, column)
                return
            column += 1
        # Check for diagonal line right
        if diagonal_listA.count("O") == 1 and "X" not in diagonal_listA:
            self.Click(diagonal_listA.index(1) + 1, diagonal_listA.index(1))
            return
        # Check for diagonal line left
        if diagonal_listB.count("O") == 1 and "X" not in diagonal_listB:
            self.Click(diagonal_listB.index(1) + 1, 2 - diagonal_listB.index(1))
            return
        # ################################## MAKE STARTUP POINT ################################################################
        while not self.game_end:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            if self.game_list[row][column] == 1:
                self.root.after(1000, self.Click(row + 1, column))
                return


if __name__ == '__main__':
    a = GameAI()
