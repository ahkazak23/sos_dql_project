import unittest
from game.game_env import SOSGame

class TestSOSGame(unittest.TestCase):
    def setUp(self):
        self.game = SOSGame()

    def test_board_initialization(self):
        self.assertEqual(self.game.board.shape, (5, 5))
        self.assertTrue((self.game.board == " ").all())

    def test_valid_move(self):
        self.assertTrue(self.game.make_move(0, 0, "S"))
        self.assertEqual(self.game.board[0, 0], "S")
        self.assertFalse(self.game.make_move(0, 0, "O"))  # Invalid, already occupied

    def test_sos_check(self):
        self.game.make_move(0, 0, "S")
        self.game.make_move(0, 1, "O")
        self.game.make_move(0, 2, "S")
        self.assertEqual(self.game.check_sos(0, 1), 1)

    def test_switch_player(self):
        self.assertEqual(self.game.current_player, "player")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "ai")
