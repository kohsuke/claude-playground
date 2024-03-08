import pygame
import sys
from enum import Enum

# Constants
BOARD_SIZE = 8
CELL_SIZE = 50
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)  # Toned down green color

# Piece enum
class Piece(Enum):
    BLACK = 1
    WHITE = 2

# Board class
class Board:
    def __init__(self):
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.grid[3][3] = Piece.WHITE
        self.grid[3][4] = Piece.BLACK
        self.grid[4][3] = Piece.BLACK
        self.grid[4][4] = Piece.WHITE

    def is_valid_move(self, row, col, color):
        if self.grid[row][col] is not None:
            return False
        for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            if self._check_direction(row, col, dx, dy, color):
                return True
        return False

    def _check_direction(self, row, col, dx, dy, color):
        x, y = row + dx, col + dy
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return False
        if self.grid[x][y] is None or self.grid[x][y] == color:
            return False
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if self.grid[x][y] is None:
                return False
            if self.grid[x][y] == color:
                return True
            x += dx
            y += dy
        return False

    def make_move(self, row, col, color):
        if not self.is_valid_move(row, col, color):
            return False
        self.grid[row][col] = color
        for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            self._flip_pieces(row, col, dx, dy, color)
        return True

    def _flip_pieces(self, row, col, dx, dy, color):
        x, y = row + dx, col + dy
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return
        if self.grid[x][y] is None or self.grid[x][y] == color:
            return
        pieces_to_flip = []
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if self.grid[x][y] is None:
                return
            if self.grid[x][y] == color:
                break
            pieces_to_flip.append((x, y))
            x += dx
            y += dy
        for piece in pieces_to_flip:
            self.grid[piece[0]][piece[1]] = color

    def get_valid_moves(self, color):
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, color):
                    valid_moves.append((row, col))
        return valid_moves

    def is_game_over(self):
        return len(self.get_valid_moves(Piece.BLACK)) == 0 and len(self.get_valid_moves(Piece.WHITE)) == 0

    def get_score(self):
        black_score = sum(row.count(Piece.BLACK) for row in self.grid)
        white_score = sum(row.count(Piece.WHITE) for row in self.grid)
        return black_score, white_score

# Drawing class
class Drawing:
    @staticmethod
    def draw_board(screen, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                if board.grid[row][col] is not None:
                    color = BLACK if board.grid[row][col] == Piece.BLACK else WHITE
                    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    @staticmethod
    def draw_valid_moves(screen, valid_moves):
        for move in valid_moves:
            row, col = move
            pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 5)

    @staticmethod
    def draw_score(screen, score):
        font = pygame.font.Font(None, 36)
        black_score_text = font.render(f"Black: {score[0]}", True, BLACK)
        white_score_text = font.render(f"White: {score[1]}", True, WHITE)
        screen.blit(black_score_text, (10, WINDOW_SIZE - 40))
        screen.blit(white_score_text, (WINDOW_SIZE - 120, WINDOW_SIZE - 40))

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Piece.BLACK

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Othello")

        game_over = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if self.board.make_move(row, col, self.current_player):
                        self.current_player = Piece.WHITE if self.current_player == Piece.BLACK else Piece.BLACK

            screen.fill(BLACK)
            Drawing.draw_board(screen, self.board)
            if not game_over:
                valid_moves = self.board.get_valid_moves(self.current_player)
                Drawing.draw_valid_moves(screen, valid_moves)
            score = self.board.get_score()
            Drawing.draw_score(screen, score)
            pygame.display.flip()

            if self.board.is_game_over() and not game_over:
                game_over = True
                self.show_game_over_screen(screen, score)

        pygame.quit()

    def show_game_over_screen(self, screen, score):
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        black_score, white_score = score
        winner_text = font.render("Black Wins!" if black_score > white_score else "White Wins!", True, WHITE)
        play_again_text = font.render("Click to play again", True, WHITE)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                    return

            screen.fill(BLACK)
            screen.blit(game_over_text, (WINDOW_SIZE // 2 - game_over_text.get_width() // 2, 100))
            screen.blit(winner_text, (WINDOW_SIZE // 2 - winner_text.get_width() // 2, 200))
            screen.blit(play_again_text, (WINDOW_SIZE // 2 - play_again_text.get_width() // 2, 300))
            pygame.display.flip()

    def reset_game(self):
        self.board = Board()
        self.current_player = Piece.BLACK

# Main function
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()