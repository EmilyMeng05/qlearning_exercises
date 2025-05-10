class TicTacToe:
    #Initialize the constructor 
    #Parameters: 
    #- player1_symbol: default to be X 
    #- player2_symbol: default to be O 
    def __init__(self, player1_symbol="X", player2_symbol="O"):
        self.player1 = player1_symbol
        self.player2 = player2_symbol
        # Create a 3x3 grid filled with spaces
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
        # Boolean to keep track of whose turn it is
        self.current_turn = True  

    #Prints the current game grid in a formatted way.
    def display_grid(self):
        for row in self.grid:
            print(" | ".join(row))
            print("-" * 9)
    #checks if the chosen cell is unoccupied or not 
    #return true if the cell is free, else false 
    def is_free_cell(self, cell):
        row, col = divmod(cell - 1, 3)
        return self.grid[row][col] == " "

    # places the current player's symbol in the selected cell 
    def write_cell(self, cell):
        row, col = divmod(cell - 1, 3)
        if self.current_turn:
            self.grid[row][col] = self.player1
        else:
            self.grid[row][col] = self.player2

    # switch turn to the next plaer
    def switch_turn(self):
        self.current_turn = not self.current_turn

    # check the winning combinations to see if there's a winner
    def check_winner(self):
        lines = []

        # Check rows and columns
        for i in range(3):
            lines.append(self.grid[i])
            lines.append([self.grid[0][i], self.grid[1][i], self.grid[2][i]])
        # Check diagonals
        lines.append([self.grid[0][0], self.grid[1][1], self.grid[2][2]])
        lines.append([self.grid[0][2], self.grid[1][1], self.grid[2][0]])

        # Check for three identical non-empty symbols in any line
        for line in lines:
            if line.count(line[0]) == 3 and line[0] != " ":
                return line[0]
        return None

    # plays the game!!
    def play_game(self):
        print("Starting Tic Tac Toe!\n")
        self.display_grid()

        for turn in range(9):
            player_symbol = self.player1 if self.current_turn else self.player2
            while True:
                try:
                    cell = int(input(f"Player {player_symbol}, choose a cell (1-9): "))
                    # if it's a valid move
                    if 1 <= cell <= 9 and self.is_free_cell(cell):
                        break
                    else:
                        print("Invalid or taken cell. Try again.")
                except ValueError:
                    print("Enter a number between 1 and 9.")

            # Place the symbol on the board
            self.write_cell(cell)
            # Show updated board
            self.display_grid()

            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                return

            # Change to the other player's turn
            self.switch_turn()

        # If loop completes without winner, it's a draw
        print("Game ends in a draw.")
    def is_draw(self):
        return all(cell != " " for row in self.grid for cell in row) and self.check_winner() is None

    def game_over(self):
        return self.check_winner() is not None or self.is_draw()

