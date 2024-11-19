import tkinter as tk
from tkinter import messagebox
import torch
from game.game_env import SOSGame
from models.dq_network import DQNetwork

# Load the trained AI model
def load_model(model_path, state_size, action_size):
    model = DQNetwork(state_size, action_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# AI makes a move
def ai_move(env, model):
    state = torch.FloatTensor(env._get_numeric_board()).unsqueeze(0)
    with torch.no_grad():
        q_values = model(state)
    action = q_values.argmax().item()
    row, col = divmod(action, env.size)
    return row, col

# Main GUI Application
class SOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.env = SOSGame()
        self.model = load_model("outputs/models/sos_dqn.pth", state_size=25, action_size=25)

        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        # Create the game grid
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                btn = tk.Button(self.root, text=" ", font=("Arial", 24), width=3, height=1,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        # Status label
        self.status_label = tk.Label(self.root, text="Player's Turn", font=("Arial", 16))
        self.status_label.grid(row=5, column=0, columnspan=5, pady=10)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Arial", 14),
                                      command=self.reset_game)
        self.reset_button.grid(row=6, column=0, columnspan=5, pady=10)

    def player_move(self, row, col):
        if self.env.board[row, col] != " ":
            messagebox.showwarning("Invalid Move", "This cell is already occupied!")
            return

        letter = "S"  # Fixed letter for simplicity
        self.env.make_move(row, col, letter)
        self.update_board()
        self.env.switch_player()
        self.update_status()

        # Check if game is over
        if " " not in self.env.board:
            self.end_game()
        else:
            self.ai_turn()

    def ai_turn(self):
        if self.env.current_player == "ai":
            row, col = ai_move(self.env, self.model)
            letter = "S"  # AI plays "S" for simplicity
            self.env.make_move(row, col, letter)
            self.update_board()
            self.env.switch_player()
            self.update_status()

        # Check if game is over
        if " " not in self.env.board:
            self.end_game()

    def update_board(self):
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].config(text=self.env.board[i, j])

    def update_status(self):
        self.status_label.config(text=f"{self.env.current_player.capitalize()}'s Turn")

    def reset_game(self):
        self.env.reset()
        self.update_board()
        self.update_status()

    def end_game(self):
        messagebox.showinfo("Game Over", f"Final Scores: {self.env.scores}")
        self.reset_game()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SOSApp(root)
    root.mainloop()
