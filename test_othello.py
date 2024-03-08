import unittest
from unittest.mock import patch
from io import StringIO

from othello import Othello, Vector2D, Player

class TestOthelloGame(unittest.TestCase):

    def setUp(self):
        self.game = Othello()

    def test_get_valid_moves(self):
        valid_moves_player_1 = self.game.get_valid_moves(Player.WHITE)
        valid_moves_player_2 = self.game.get_valid_moves(Player.BLACK)
        self.assertEqual(len(valid_moves_player_1), 4)
        self.assertEqual(len(valid_moves_player_2), 4)
        self.assertIn(Vector2D(2, 3), valid_moves_player_2)
        self.assertIn(Vector2D(3, 2), valid_moves_player_1)

    def test_check_direction(self):
        tiles = self.game.check_direction(Vector2D(2, 3), Player.BLACK, Player.BLACK.opponent, Othello.EAST)
        self.assertEqual(tiles, [Vector2D(3, 4)])
        tiles = self.game.check_direction(Vector2D(3, 2), Player.WHITE, Player.WHITE.opponent, Othello.NORTH)
        self.assertEqual(tiles, [Vector2D(4, 3)])
        tiles = self.game.check_direction(Vector2D(3, 3), Player.WHITE, Player.WHITE.opponent, Othello.NORTHEAST)
        self.assertEqual(tiles, [])

    def test_make_move(self):
        self.game.make_move(Vector2D(2, 3), Player.BLACK)
        self.assertEqual(self.game.board[2][3], Player.BLACK)
        self.assertEqual(self.game.board[3][4], Player.BLACK)
        self.game.make_move(Vector2D(3, 2), Player.WHITE)
        self.assertEqual(self.game.board[3][2], Player.WHITE)
        self.assertEqual(self.game.board[4][3], Player.WHITE)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_board(self, mock_stdout):
        self.game.print_board()
        expected_output = """  0 1 2 3 4 5 6 7
0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0
3 0 0 1 2 1 0 0 0
4 0 0 2 1 0 0 0 0
5 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()