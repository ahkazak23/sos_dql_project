import tkinter as tk
from tkinter import simpledialog  # Import simpledialog explicitly

from models.dq_network import DQNetworkCNN
from game.game_env import SOSGameEnv
from training.train import decode_action, encode_action
import torch


class SOSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")

        # Initialize the game environment
        self.env = SOSGameEnv()
        self.board_size = self.env.board_size

        # Load the trained agent
        action_size = self.board_size * self.board_size * 2
        self.policy_net = DQNetworkCNN(action_size)
        self.policy_net.load_state_dict(torch.load('../training/outputs/models/sos_dqn.pth'))
        self.policy_net.eval()

        # Create the game board (grid of buttons)
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.create_board()

        # Display scores
        self.score_label = tk.Label(self.root, text="Scores: Player: 0 | Agent: 0")
        self.score_label.grid(row=self.board_size, column=0, columnspan=self.board_size)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=self.board_size + 1, column=0, columnspan=self.board_size)

        # Initialize game state
        self.reset_game()

    def create_board(self):
        """Create the game board as a grid of buttons."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = tk.Button(
                    self.root,
                    text=" ",
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.player_move(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def reset_game(self):
        """Reset the game board and environment."""
        self.env.reset()
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(text=" ", state=tk.NORMAL)
        self.update_score()

    def player_move(self, row, col):
        """Handle the player's move."""
        # Ask the player to select 'S' or 'O'
        letter = tk.simpledialog.askstring("Input", "Enter 'S' or 'O':", parent=self.root)
        if letter not in ['S', 'O']:
            return  # Invalid input, do nothing

        # Perform the move
        state, reward, done, _ = self.env.step((row, col, letter))
        self.buttons[row][col].config(text=letter, state=tk.DISABLED)

        # Update the board and check if the game is over
        self.update_score()
        if done:
            self.end_game()
            return

        # Agent's turn
        self.agent_move()

    def agent_move(self):
        """Handle the agent's move."""
        state_tensor = torch.FloatTensor(self.env.get_state()).unsqueeze(0)
        with torch.no_grad():
            q_values = self.policy_net(state_tensor)

        # Determine valid actions
        valid_actions = self.env.available_actions()
        if not valid_actions:
            self.end_game()
            return

        valid_action_indices = [encode_action(a, self.board_size) for a in valid_actions]
        q_values_valid = q_values[0, valid_action_indices]
        max_q_index = torch.argmax(q_values_valid).item()
        action_index = valid_action_indices[max_q_index]
        row, col, letter = decode_action(action_index, self.board_size)

        # Perform the agent's move
        state, reward, done, _ = self.env.step((row, col, letter))
        self.buttons[row][col].config(text=letter, state=tk.DISABLED)

        # Update the board and check if the game is over
        self.update_score()
        if done:
            self.end_game()

    def update_score(self):
        """Update the score display."""
        scores = self.env.scores
        self.score_label.config(text=f"Scores: Player: {scores['player1']} | Agent: {scores['player2']}")

    def end_game(self):
        """End the game and disable the board."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(state=tk.DISABLED)
        scores = self.env.scores
        winner = "Player" if scores['player1'] > scores['player2'] else "Agent"
        tk.messagebox.showinfo("Game Over", f"Game Over! {winner} Wins!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()
