import unittest
from othello import Board, Piece

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        self.assertEqual(self.board.grid[3][3], Piece.WHITE)
        self.assertEqual(self.board.grid[3][4], Piece.BLACK)
        self.assertEqual(self.board.grid[4][3], Piece.BLACK)
        self.assertEqual(self.board.grid[4][4], Piece.WHITE)

    def test_is_valid_move(self):
        self.assertTrue(self.board.is_valid_move(2, 3, Piece.BLACK))
        self.assertTrue(self.board.is_valid_move(3, 2, Piece.BLACK))
        self.assertTrue(self.board.is_valid_move(4, 5, Piece.BLACK))
        self.assertTrue(self.board.is_valid_move(5, 4, Piece.BLACK))
        self.assertFalse(self.board.is_valid_move(0, 0, Piece.BLACK))
        self.assertFalse(self.board.is_valid_move(3, 3, Piece.BLACK))

    def test_make_move(self):
        self.assertTrue(self.board.make_move(2, 3, Piece.BLACK))
        self.assertEqual(self.board.grid[2][3], Piece.BLACK)
        self.assertEqual(self.board.grid[3][3], Piece.BLACK)
        self.assertFalse(self.board.make_move(3, 3, Piece.WHITE))
        self.assertEqual(self.board.grid[3][3], Piece.BLACK)

    def test_get_valid_moves(self):
        valid_moves = self.board.get_valid_moves(Piece.BLACK)
        self.assertCountEqual(valid_moves, [(2, 3), (3, 2), (4, 5), (5, 4)])
        valid_moves = self.board.get_valid_moves(Piece.WHITE)
        self.assertCountEqual(valid_moves, [(2, 4), (3, 5), (4, 2), (5, 3)])

    def test_is_game_over(self):
        self.assertFalse(self.board.is_game_over())
        self.board.grid = [[Piece.BLACK] * 8 for _ in range(8)]
        self.assertTrue(self.board.is_game_over())

    def test_get_score(self):
        self.assertEqual(self.board.get_score(), (2, 2))
        self.board.grid[0][0] = Piece.BLACK
        self.board.grid[0][1] = Piece.WHITE
        self.assertEqual(self.board.get_score(), (3, 3))

if __name__ == '__main__':
    unittest.main()