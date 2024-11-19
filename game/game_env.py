import numpy as np

class SOSGame:
    def __init__(self, size=5):
        """Initialize the SOS game with an empty board."""
        self.size = size  # Board size (default 5x5)
        self.board = np.full((size, size), " ")  # Empty board
        self.scores = {"player": 0, "ai": 0}  # Scores for player and AI
        self.current_player = "player"  # Current player ("player" or "AI")

    def reset(self):
        """Reset the game to the initial state."""
        self.board = np.full((self.size, self.size), " ")
        self.scores = {"player": 0, "ai": 0}
        self.current_player = "player"
        return self._get_numeric_board()

    def _get_numeric_board(self):
        """Convert the board to a numeric representation."""
        numeric_board = np.zeros_like(self.board, dtype=np.float32)
        numeric_board[self.board == "S"] = 1.0  # "S" becomes 1.0
        numeric_board[self.board == "O"] = -1.0  # "O" becomes -1.0
        return numeric_board.flatten()  # Flatten to 1D array

    def render(self):
        """Render the current board to the console."""
        for row in self.board:
            print(" | ".join(row))
            print("-" * (self.size * 4 - 1))

    def is_valid_move(self, row, col):
        """Check if a move is valid."""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row, col] == " "

    def make_move(self, row, col, letter):
        """Make a move on the board."""
        if self.is_valid_move(row, col) and letter in ["S", "O"]:
            self.board[row, col] = letter
            return self._get_numeric_board()  # Return the updated numeric board
        return None  # Return None if the move is invalid

    def check_sos(self, row, col):
        """Check for SOS formations around a specific position."""
        directions = [
            [(0, -1), (0, 1)],  # Horizontal
            [(-1, 0), (1, 0)],  # Vertical
            [(-1, -1), (1, 1)], # Diagonal top-left to bottom-right
            [(-1, 1), (1, -1)]  # Diagonal top-right to bottom-left
        ]
        score = 0
        for dir1, dir2 in directions:
            try:
                if (
                    self.get_cell(row + dir1[0], col + dir1[1]) == "S" and
                    self.get_cell(row + dir2[0], col + dir2[1]) == "S"
                ):
                    score += 1
            except IndexError:
                continue
        return score

    def get_cell(self, row, col):
        """Get the value of a cell, or None if out of bounds."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row, col]
        return None

    def switch_player(self):
        """Switch the current player."""
        self.current_player = "ai" if self.current_player == "player" else "player"
