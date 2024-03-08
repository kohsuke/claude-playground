import unittest
from othello import Othello, Player, Vector2D

class TestOthello(unittest.TestCase):
    def setUp(self):
        self.game = Othello()

    def test_initial_board(self):
        expected_board = [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.WHITE, Player.BLACK, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.BLACK, Player.WHITE, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        self.assertEqual(self.game.board, expected_board)

    def test_get_cell(self):
        self.assertEqual(self.game.get_cell(Vector2D(3, 3)), Player.WHITE)
        self.assertEqual(self.game.get_cell(Vector2D(3, 4)), Player.BLACK)
        self.assertEqual(self.game.get_cell(Vector2D(4, 3)), Player.BLACK)
        self.assertEqual(self.game.get_cell(Vector2D(4, 4)), Player.WHITE)
        self.assertEqual(self.game.get_cell(Vector2D(0, 0)), Player.EMPTY)

    def test_set_cell(self):
        self.game.set_cell(Vector2D(0, 0), Player.WHITE)
        self.assertEqual(self.game.get_cell(Vector2D(0, 0)), Player.WHITE)

    def test_get_valid_moves(self):
        valid_moves_black = [Vector2D(2, 3), Vector2D(3, 2), Vector2D(4, 5), Vector2D(5, 4)]
        valid_moves_white = [Vector2D(2, 4), Vector2D(3, 5), Vector2D(4, 2), Vector2D(5, 3)]
        self.assertEqual(self.game.get_valid_moves(Player.BLACK), valid_moves_black)
        self.assertEqual(self.game.get_valid_moves(Player.WHITE), valid_moves_white)

    def test_check_direction(self):
        self.assertEqual(self.game.check_direction(Vector2D(2, 3), Player.BLACK, Othello.EAST), [Vector2D(3, 4)])
        self.assertEqual(self.game.check_direction(Vector2D(3, 2), Player.WHITE, Othello.NORTH), [Vector2D(4, 3)])
        self.assertEqual(self.game.check_direction(Vector2D(3, 3), Player.WHITE, Othello.NORTHEAST), [])

    def test_is_on_board(self):
        self.assertTrue(self.game.is_on_board(Vector2D(0, 0)))
        self.assertTrue(self.game.is_on_board(Vector2D(7, 7)))
        self.assertFalse(self.game.is_on_board(Vector2D(-1, 0)))
        self.assertFalse(self.game.is_on_board(Vector2D(0, 8)))

    def test_make_move(self):
        self.game.make_move(Vector2D(2, 3), Player.BLACK)
        self.assertEqual(self.game.get_cell(Vector2D(2, 3)), Player.BLACK)
        self.assertEqual(self.game.get_cell(Vector2D(3, 3)), Player.BLACK)
        self.assertEqual(self.game.get_cell(Vector2D(3, 4)), Player.BLACK)

        self.game.make_move(Vector2D(2, 4), Player.WHITE)
        self.assertEqual(self.game.get_cell(Vector2D(2, 4)), Player.WHITE)
        self.assertEqual(self.game.get_cell(Vector2D(3, 4)), Player.WHITE)


if __name__ == "__main__":
    unittest.main()