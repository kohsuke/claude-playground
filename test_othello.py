import unittest
from unittest.mock import patch
from io import StringIO

from othello import Othello

class TestOthelloGame(unittest.TestCase):

    def setUp(self):
        self.game = Othello()

    def test_get_valid_moves(self):
        valid_moves_player_1 = self.game.get_valid_moves(1)
        valid_moves_player_2 = self.game.get_valid_moves(2)
        self.assertEqual(len(valid_moves_player_1), 4)
        self.assertEqual(len(valid_moves_player_2), 4)
        self.assertIn((2, 3), valid_moves_player_2)
        self.assertIn((3, 2), valid_moves_player_1)

    def test_check_direction(self):
        tiles = self.game.check_direction(2, 3, 2, 1, 0, 1)
        self.assertEqual(tiles, [(3, 4)])
        tiles = self.game.check_direction(3, 2, 1, 2, 1, 0)
        self.assertEqual(tiles, [(4, 3)])
        tiles = self.game.check_direction(3, 3, 1, 2, 1, 1)
        self.assertEqual(tiles, [])

    def test_make_move(self):
        self.game.make_move(2, 3, 2)
        self.assertEqual(self.game.board[2][3], 2)
        self.assertEqual(self.game.board[3][4], 2)
        self.game.make_move(3, 2, 1)
        self.assertEqual(self.game.board[3][2], 1)
        self.assertEqual(self.game.board[4][3], 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_board(self, mock_stdout):
        self.game.print_board()
        expected_output = """  0 1 2 3 4 5 6 7
0                
1                
2       B        
3     WB BW      
4       BW       
5                
6                
7                
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()