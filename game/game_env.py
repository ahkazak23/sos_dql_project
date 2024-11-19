# game/game_env.py

import numpy as np
from config.game_config import BOARD_SIZE


class SOSGameEnv:
    def __init__(self):
        self.board_size = BOARD_SIZE
        self.reset()

    def reset(self):
        self.board = np.full((self.board_size, self.board_size), '', dtype=str)
        self.current_player = 'player1'
        self.scores = {'player1': 0, 'player2': 0}
        self.game_over = False
        return self.get_state()

    def get_state(self):
        state = np.copy(self.board)
        state[state == ''] = 0
        state[state == 'S'] = 1
        state[state == 'O'] = 2
        return state.astype(np.float32)

    def available_actions(self):
        actions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row, col] == '':
                    actions.append((row, col, 'S'))
                    actions.append((row, col, 'O'))
        return actions

    def step(self, action):
        row, col, letter = action
        if not self.is_valid_position(row, col) or self.board[row, col] != '':
            reward = -1  # Penalty for invalid move
            done = False
            info = {'invalid_move': True}
        else:
            self.board[row, col] = letter
            points = self.check_sos(row, col, letter)
            self.scores[self.current_player] += points
            # Enhanced reward function
            reward = points * 10  # Increase the reward magnitude
            if points == 0:
                reward -= 0.1  # Small penalty for not forming an SOS
            self.check_game_over()
            done = self.game_over
            info = {'invalid_move': False}
            # Do not switch player if points were scored
            if points == 0:
                self.switch_player()
        return self.get_state(), reward, done, info

    def switch_player(self):
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'

    def check_sos(self, row, col, letter):
        points = 0
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            if letter == 'S':
                # Check for 'S' at the start of 'SOS'
                x1, y1 = row + dx, col + dy
                x2, y2 = row + 2 * dx, col + 2 * dy
                if self.is_valid_position(x1, y1) and self.is_valid_position(x2, y2):
                    if self.board[x1, y1] == 'O' and self.board[x2, y2] == 'S':
                        points += 1
            elif letter == 'O':
                # Check for 'O' in the middle of 'SOS'
                x1, y1 = row - dx, col - dy
                x2, y2 = row + dx, col + dy
                if self.is_valid_position(x1, y1) and self.is_valid_position(x2, y2):
                    if self.board[x1, y1] == 'S' and self.board[x2, y2] == 'S':
                        points += 1
        return points

    def is_valid_position(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def check_game_over(self):
        if not any(self.board.flatten() == ''):
            self.game_over = True

    def render(self):
        print('\n'.join([' '.join(cell or '.' for cell in row) for row in self.board]))
        print(f"Scores: {self.scores}")
