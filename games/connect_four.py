# Previous work done by me
# I coded this in java and so I changed it into a python file
class ConnectFour():
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [['-' for _ in range(self.cols)] for _ in range(self.rows)]
        self.is_x_turn = True

    def instructions(self):
        return (
            "Welcome to Connect Four!\n"
            "2 Players take turns dropping their tokens into one of the columns (0-6).\n"
            "The token will fall to the lowest empty space in the column.\n"
            "The first player to connect four of their tokens\n"
            "either horizontally, vertically, or diagonally wins.\n"
            "Good luck and enjoy!"
        )

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.board])

    def check_winner(self):
        # Horizontal
        for i in range(self.rows):
            for j in range(self.cols - 3):
                player = self.board[i][j]
                if player != '-' and all(self.board[i][j + k] == player for k in range(4)):
                    return 1 if player == 'X' else 2

        # Vertical
        for i in range(self.rows - 3):
            for j in range(self.cols):
                player = self.board[i][j]
                if player != '-' and all(self.board[i + k][j] == player for k in range(4)):
                    return 1 if player == 'X' else 2

        # Diagonal '\'
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                player = self.board[i][j]
                if player != '-' and all(self.board[i + k][j + k] == player for k in range(4)):
                    return 1 if player == 'X' else 2

        # Diagonal '/'
        for i in range(self.rows - 3):
            for j in range(3, self.cols):
                player = self.board[i][j]
                if player != '-' and all(self.board[i + k][j - k] == player for k in range(4)):
                    return 1 if player == 'X' else 2

        return -1

    def get_next_player(self):
        return -1 if self.is_game_over() else (1 if self.is_x_turn else 2)

    def make_move(self):
        player_symbol = 'X' if self.is_x_turn else 'O'
        try:
            col = int(input(f"Player {player_symbol}, choose a column (0-{self.cols - 1}): "))
            self._make_move(col, player_symbol)
            self.is_x_turn = not self.is_x_turn
        except ValueError as e:
            print(f"** Illegal move: {e}")
            self.make_move()

    def _make_move(self, col, symbol):
        if col < 0 or col >= self.cols:
            raise ValueError(f"Column {col} is out of range.")
        if self.board[0][col] != '-':
            raise ValueError(f"Column {col} is full.")
        row = self.rows - 1
        while self.board[row][col] != '-':
            row -= 1
        self.board[row][col] = symbol

    def is_draw(self):
        # The game is a draw if no '-' exists in the top row
        return all(cell != '-' for cell in self.board[0])

    def game_over(self):
        return self.check_winner() is not None or self.is_draw()



def main():
    game = ConnectFour()
    print(game.instructions())
    print()

    while not game.is_game_over():
        print(game)
        print(f"Player {game.get_next_player()}'s turn.")
        game.make_move()

    print(game)
    winner = game.get_winner()
    if winner > 0:
        print(f"Player {winner} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
