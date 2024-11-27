import random
import copy
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor


BOARD_SIZE = 5
WINNING_LENGTH = 4
SIMULATIONS = 300 

class GameState:
    def __init__(self):
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X"

    def is_valid_move(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == ""

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
    
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.check_line(row, col, 1, 0) or self.check_line(row, col, 0, 1) or \
                   self.check_line(row, col, 1, 1) or self.check_line(row, col, 1, -1):
                    return self.board[row][col]
        return None

    def check_line(self, row, col, d_row, d_col):
        start = self.board[row][col]
        if start == "":
            return False
        for i in range(1, WINNING_LENGTH):
            r, c = row + i * d_row, col + i * d_col
            if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE or self.board[r][c] != start:
                return False
        return True

    def get_available_moves(self):
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.is_valid_move(r, c)]

    def clone(self):
        new_state = GameState()
        new_state.board = copy.deepcopy(self.board)
        new_state.current_player = self.current_player
        return new_state

def simulate_game(state):
    current_state = state.clone()
    depth = 0
    while not current_state.check_winner() and current_state.get_available_moves() and depth < 20:
        move = random.choice(current_state.get_available_moves())
        current_state.make_move(*move)
        depth += 1
    return 1 if current_state.check_winner() == "O" else 0

def monte_carlo_tree_search(state):
    moves = state.get_available_moves()
    if not moves:
        return None
    move_scores = {move: 0 for move in moves}


    with ThreadPoolExecutor(max_workers=4) as executor:
        for move in moves:
            simulations = [executor.submit(simulate_move, state, move) for _ in range(SIMULATIONS)]
            results = [sim.result() for sim in simulations]
            move_scores[move] = sum(results)


    best_move = max(move_scores, key=move_scores.get)
    return best_move

def simulate_move(state, move):
    simulated_state = state.clone()
    simulated_state.make_move(*move)
    return simulate_game(simulated_state)

def play_game():
    root = tk.Tk()
    root.title("5x5 XOX - Monte Carlo Arama Ağacı")
    game_state = GameState()

    buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    result_label = tk.Label(root, text="", font=("Arial", 20))
    result_label.pack()

    def reset_game():
        nonlocal game_state
        game_state = GameState()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                buttons[row][col]["text"] = ""
                buttons[row][col]["state"] = "normal"
        result_label.config(text="")

    def handle_click(row, col):
        if game_state.make_move(row, col):
            buttons[row][col]["text"] = "X"
            buttons[row][col]["state"] = "disabled"
            if game_state.check_winner() == "X":
                result_label.config(text="Kazandın!", fg="red")
                disable_all_buttons()
                return
            ai_move = monte_carlo_tree_search(game_state)
            if ai_move:
                game_state.make_move(*ai_move)
                r, c = ai_move
                buttons[r][c]["text"] = "O"
                buttons[r][c]["state"] = "disabled"
                if game_state.check_winner() == "O":
                    result_label.config(text="Kaybettin!", fg="blue")
                    disable_all_buttons()
                    return
            if not game_state.get_available_moves():
                result_label.config(text="Berabere!", fg="black")

    def disable_all_buttons():
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                buttons[row][col]["state"] = "disabled"

    frame = tk.Frame(root)
    frame.pack()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            button = tk.Button(frame, text="", font=("Arial", 20), width=4, height=2,
                               command=lambda r=row, c=col: handle_click(r, c))
            button.grid(row=row, column=col)
            buttons[row][col] = button

    tk.Button(root, text="Tekrar Oyna", command=reset_game, font=("Arial", 14)).pack()

    root.mainloop()

if __name__ == "__main__":
    play_game()
