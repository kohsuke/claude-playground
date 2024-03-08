# othello.py
from enum import Enum

class Player(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    @property
    def opponent(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE

class Vector2D:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        return Vector2D(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Vector2D(self.row - other.row, self.col - other.col)

    def __str__(self):
        return f"({self.row}, {self.col})"

    def __repr__(self):
        return str(self)


class Othello:
    NORTH = Vector2D(-1, 0)
    NORTHEAST = Vector2D(-1, 1)
    EAST = Vector2D(0, 1)
    SOUTHEAST = Vector2D(1, 1)
    SOUTH = Vector2D(1, 0)
    SOUTHWEST = Vector2D(1, -1)
    WEST = Vector2D(0, -1)
    NORTHWEST = Vector2D(-1, -1)

    DIRECTIONS = [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST]

    def __init__(self):
        self.BOARD_SIZE = 8
        self.board = [[Player.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.board[3][3] = self.board[4][4] = Player.WHITE
        self.board[3][4] = self.board[4][3] = Player.BLACK

    def print_board(self):
        print('  ' + '  '.join([str(i) for i in range(self.BOARD_SIZE)]))
        for row in range(self.BOARD_SIZE):
            print(str(row) + ' ' + ' '.join([str(self.board[row][col]) for col in range(self.BOARD_SIZE)]))

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                position = Vector2D(row, col)
                if self.board[row][col] == Player.EMPTY:
                    if any(self.check_direction(position, player, player.opponent, direction) for direction in self.DIRECTIONS):
                        valid_moves.append(position)
        return valid_moves

    def check_direction(self, position, player, opponent, direction):
        current_position = position + direction
        tiles = []

        while self.is_on_board(current_position) and self.board[current_position.row][current_position.col] == opponent:
            tiles.append(current_position)
            current_position += direction

        if (
            tiles
            and self.is_on_board(current_position)
            and self.board[current_position.row][current_position.col] == player
        ):
            return tiles

        return []

    def is_on_board(self, position):
        return 0 <= position.row < self.BOARD_SIZE and 0 <= position.col < self.BOARD_SIZE

    def make_move(self, position, player):
        self.board[position.row][position.col] = player
        opponent = player.opponent
        for direction in self.DIRECTIONS:
            tiles = self.check_direction(position, player, opponent, direction)
            for tile in tiles:
                self.board[tile.row][tile.col] = player

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