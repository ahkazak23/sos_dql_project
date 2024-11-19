# tests/test_game_env.py

import unittest
from game.game_env import SOSGameEnv


class TestSOSGameEnv(unittest.TestCase):
    def setUp(self):
        self.env = SOSGameEnv()

    def test_initial_state(self):
        state = self.env.get_state()
        self.assertEqual(state.shape, (5, 5))
        self.assertTrue((state == 0).all())

    def test_valid_move(self):
        action = (0, 0, 'S')
        state, reward, done, info = self.env.step(action)
        self.assertEqual(reward, 0)
        self.assertFalse(done)
        self.assertFalse(info['invalid_move'])
        self.assertEqual(self.env.board[0, 0], 'S')

    def test_invalid_move(self):
        action = (0, 0, 'S')
        self.env.step(action)  # First move
        state, reward, done, info = self.env.step(action)  # Invalid move
        self.assertEqual(reward, -1)
        self.assertFalse(done)
        self.assertTrue(info['invalid_move'])

    def test_sos_detection_horizontal(self):
        # Place 'S' at (0,0), 'O' at (0,1)
        self.env.board[0, 0] = 'S'
        self.env.board[0, 1] = 'O'
        action = (0, 2, 'S')  # This should form an SOS horizontally
        state, reward, done, info = self.env.step(action)
        self.assertEqual(reward, 1)
        self.assertFalse(done)
        self.assertEqual(self.env.scores[self.env.current_player], 1)

    def test_sos_detection_diagonal(self):
        # Place 'S' at (0,0), 'O' at (1,1)
        self.env.board[0, 0] = 'S'
        self.env.board[1, 1] = 'O'
        action = (2, 2, 'S')  # This should form an SOS diagonally
        state, reward, done, info = self.env.step(action)
        self.assertEqual(reward, 1)
        self.assertFalse(done)

    def test_game_over(self):
        # Fill the board completely
        for row in range(5):
            for col in range(5):
                self.env.board[row, col] = 'S'
        self.env.check_game_over()
        self.assertTrue(self.env.game_over)

    def test_switch_player(self):
        self.env.current_player = 'player1'
        self.env.switch_player()
        self.assertEqual(self.env.current_player, 'player2')
        self.env.switch_player()
        self.assertEqual(self.env.current_player, 'player1')

    def test_render(self):
        self.env.board[0, 0] = 'S'
        self.env.board[1, 1] = 'O'
        self.env.render()
        # Visually inspect the output or redirect stdout to test programmatically


if __name__ == '__main__':
    unittest.main()
