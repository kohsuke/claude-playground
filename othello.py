# othello.py

class Othello:
    def __init__(self):
        self.BOARD_SIZE = 8
        self.PLAYER_SYMBOLS = {
            0: ' ',
            1: 'W',
            2: 'B'
        }
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.board[3][3] = self.board[4][4] = 1  # Player 1 (White)
        self.board[3][4] = self.board[4][3] = 2  # Player 2 (Black)

    def print_board(self):
        print('  ' + '  '.join([str(i) for i in range(self.BOARD_SIZE)]))
        for row in range(self.BOARD_SIZE):
            print(str(row) + ' ' + ' '.join([self.PLAYER_SYMBOLS[self.board[row][col]] for col in range(self.BOARD_SIZE)]))

    def get_valid_moves(self, player):
        valid_moves = []
        opponent = 2 if player == 1 else 1
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 0:
                    if any(self.check_direction(row, col, player, opponent, dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)):
                        valid_moves.append((row, col))
        return valid_moves

    def check_direction(self, row, col, player, opponent, dx, dy):
        x, y = row + dx, col + dy
        tiles = []
        while 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE and self.board[x][y] == opponent:
            tiles.append((x, y))
            x += dx
            y += dy
        if tiles and 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE and self.board[x][y] == player:
            return tiles
        return []

    def make_move(self, row, col, player):
        self.board[row][col] = player
        opponent = 2 if player == 1 else 1
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) != (0, 0):
                    tiles = self.check_direction(row, col, player, opponent, dx, dy)
                    for x, y in tiles:
                        self.board[x][y] = player

    def play(self):
        player = 1
        while True:
            self.print_board()
            valid_moves = self.get_valid_moves(player)
            if not valid_moves:
                if all(self.board[row][col] != 0 for row in range(self.BOARD_SIZE) for col in range(self.BOARD_SIZE)):
                    # Game over, count the pieces
                    white_count = sum(row.count(1) for row in self.board)
                    black_count = sum(row.count(2) for row in self.board)
                    if white_count > black_count:
                        print("White wins!")
                    elif black_count > white_count:
                        print("Black wins!")
                    else:
                        print("It's a tie!")
                    break
                else:
                    print(f"Player {self.PLAYER_SYMBOLS[player]} has no valid moves. Skipping turn.")
                    player = 2 if player == 1 else 1
                    continue

            print(f"Player {self.PLAYER_SYMBOLS[player]}'s turn. Valid moves: {valid_moves}")
            while True:
                try:
                    row, col = map(int, input("Enter your move (row col): ").split())
                    if (row, col) in valid_moves:
                        break
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Invalid input, try again.")

            self.make_move(row, col, player)
            player = 2 if player == 1 else 1