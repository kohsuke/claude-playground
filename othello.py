from enum import Enum

class Player(Enum):
    EMPTY = ' '
    WHITE = 'W'
    BLACK = 'B'

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

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

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
        self.set_cell(Vector2D(3, 3), Player.WHITE)
        self.set_cell(Vector2D(4, 4), Player.WHITE)
        self.set_cell(Vector2D(3, 4), Player.BLACK)
        self.set_cell(Vector2D(4, 3), Player.BLACK)

    def print_board(self):
        print(' ' + ' '.join([str(i) for i in range(self.BOARD_SIZE)]))
        for row in range(self.BOARD_SIZE):
            print(str(row) + ' ' + ' '.join([self.get_cell(Vector2D(row, col)).value for col in range(self.BOARD_SIZE)]))

    def get_cell(self, position):
        return self.board[position.row][position.col]

    def set_cell(self, position, player):
        self.board[position.row][position.col] = player

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                position = Vector2D(row, col)
                if self.get_cell(position) == Player.EMPTY:
                    if any(self.check_direction(position, player, direction) for direction in self.DIRECTIONS):
                        valid_moves.append(position)
        return valid_moves

    def check_direction(self, position, player, direction):
        current_position = position + direction
        tiles = []

        while self.is_on_board(current_position) and self.get_cell(current_position) == player.opponent:
            tiles.append(current_position)
            current_position += direction

        if (
            tiles
            and self.is_on_board(current_position)
            and self.get_cell(current_position) == player
        ):
            return tiles

        return []

    def is_on_board(self, position):
        return 0 <= position.row < self.BOARD_SIZE and 0 <= position.col < self.BOARD_SIZE

    def make_move(self, position, player):
        self.set_cell(position, player)
        for direction in self.DIRECTIONS:
            tiles = self.check_direction(position, player, direction)
            for tile in tiles:
                self.set_cell(tile, player)

    def play(self):
        current_player = Player.BLACK
        while True:
            self.print_board()
            valid_moves = self.get_valid_moves(current_player)
            if not valid_moves:
                print(f"No valid moves for {current_player.name}. Skipping turn.")
                current_player = current_player.opponent
                if not self.get_valid_moves(current_player):
                    break
                continue

            print(f"{current_player.name}'s turn. Valid moves: {valid_moves}")
            row = int(input("Enter the row: "))
            col = int(input("Enter the column: "))
            position = Vector2D(row, col)

            if position in valid_moves:
                self.make_move(position, current_player)
                current_player = current_player.opponent
            else:
                print("Invalid move. Try again.")

        print("Game over!")
        self.print_board()
        white_count = sum(row.count(Player.WHITE) for row in self.board)
        black_count = sum(row.count(Player.BLACK) for row in self.board)
        print(f"White: {white_count}, Black: {black_count}")
        if white_count > black_count:
            print("White wins!")
        elif black_count > white_count:
            print("Black wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    game = Othello()
    game.play()