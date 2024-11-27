import pygame
import sys
import math

# Pygame Initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen Settings
ROWS, COLS = 5, 5
CELL_SIZE = 120  # Keeping cells equal-sized
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS + 100  # Extra space for scoreboard
LINE_WIDTH = 5
MARKER_WIDTH = 15
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5x5 Tic-Tac-Toe with AI")
SCREEN.fill(WHITE)

# Board Settings
board = [["" for _ in range(COLS)] for _ in range(ROWS)]

# Fonts
FONT = pygame.font.Font(None, 80)
BUTTON_FONT = pygame.font.Font(None, 40)

# Player and AI Symbols
PLAYER = "X"
AI = "O"

# Scores
player_score = 0
ai_score = 0

# Winning Condition Length
WIN_LENGTH = 4  # Change to 3 if needed

def draw_lines():
    """Draw the grid lines for the board."""
    for row in range(1, ROWS):
        pygame.draw.line(SCREEN, BLACK, (0, CELL_SIZE * row), (WIDTH, CELL_SIZE * row), LINE_WIDTH)
    for col in range(1, COLS):
        pygame.draw.line(SCREEN, BLACK, (CELL_SIZE * col, 0), (CELL_SIZE * col, ROWS * CELL_SIZE), LINE_WIDTH)


def display_score():
    """Display the scoreboard and feedback message below the board without covering it."""

    # Display the scoreboard
    score_height = 50  # Adjust the height of the score area
    score_y_start = ROWS * CELL_SIZE  # Position just below the game board
    pygame.draw.rect(SCREEN, WHITE, (0, score_y_start, WIDTH, score_height))  # Draw the score background
    score_text = BUTTON_FONT.render(f"Skorlar | Oyuncu: {player_score} - AI: {ai_score}", True, BLACK)
    SCREEN.blit(score_text, (
    WIDTH // 2 - score_text.get_width() // 2, score_y_start + (score_height - score_text.get_height()) // 2))

    # Display the feedback message
    feedback_message = "Good Luck"
    feedback_height = 50  # Height of the feedback area
    feedback_y_start = score_y_start + score_height  # Position right after the score area
    pygame.draw.rect(SCREEN, WHITE, (0, feedback_y_start, WIDTH, feedback_height))  # Draw the feedback background
    feedback_text = BUTTON_FONT.render(feedback_message, True, BLACK)
    SCREEN.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2,
                                feedback_y_start + (feedback_height - feedback_text.get_height()) // 2))


# Rest of your code...




def count_sequences(player, length):
    """Count sequences of a specific length for a player."""
    count = 0
    for row in range(ROWS):
        for col in range(COLS - length + 1):
            if all(board[row][col + i] == player for i in range(length)):
                count += 1
    for col in range(COLS):
        for row in range(ROWS - length + 1):
            if all(board[row + i][col] == player for i in range(length)):
                count += 1
    for row in range(ROWS - length + 1):
        for col in range(COLS - length + 1):
            if all(board[row + i][col + i] == player for i in range(length)):
                count += 1
        for col in range(length - 1, COLS):
            if all(board[row + i][col - i] == player for i in range(length)):
                count += 1
    return count



def draw_board():
    """Draw X and O markers only for updated cells."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == PLAYER:
                pygame.draw.line(SCREEN, RED,
                                 (col * CELL_SIZE + MARKER_WIDTH, row * CELL_SIZE + MARKER_WIDTH),
                                 ((col + 1) * CELL_SIZE - MARKER_WIDTH, (row + 1) * CELL_SIZE - MARKER_WIDTH), LINE_WIDTH)
                pygame.draw.line(SCREEN, RED,
                                 (col * CELL_SIZE + MARKER_WIDTH, (row + 1) * CELL_SIZE - MARKER_WIDTH),
                                 ((col + 1) * CELL_SIZE - MARKER_WIDTH, row * CELL_SIZE + MARKER_WIDTH), LINE_WIDTH)
            elif board[row][col] == AI:
                pygame.draw.circle(SCREEN, BLUE,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3, LINE_WIDTH)


def is_winner(player):
    """Check if the given player has won."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player for i in range(WIN_LENGTH)):
                return True
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player for i in range(WIN_LENGTH)):
                return True
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player for i in range(WIN_LENGTH)):
                return True
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player for i in range(WIN_LENGTH)):
                return True
    return False


def is_full():
    """Check if the board is full."""
    return all(cell != "" for row in board for cell in row)


def reset_board():
    """Reset the board to start a new game."""
    global board
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    print("Board reset. Starting new game.")


def evaluate_board():
    """
    Evaluate the board state and return a score.
    Positive scores favor AI, and negative scores favor the player.
    """
    ai_score = count_sequences(AI, WIN_LENGTH) * 10 + count_sequences(AI, WIN_LENGTH - 1) * 5
    player_score = count_sequences(PLAYER, WIN_LENGTH) * 10 + count_sequences(PLAYER, WIN_LENGTH - 1) * 5
    return ai_score - player_score


def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Alpha-Beta Pruning ile minimax algoritması.
    """
    # Kazanma durumunu kontrol et
    if is_winner(AI):
        return 100 - depth  # Daha hızlı kazanmak daha iyidir
    if is_winner(PLAYER):
        return -100 + depth  # Daha hızlı kaybetmek daha kötüdür
    if is_full() or depth == 0:  # Derinlik sınırı veya beraberlik
        return evaluate_board()

    # Maximizing AI
    if is_maximizing:
        max_eval = float('-inf')
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == "":
                    board[row][col] = AI
                    evaluation = minimax(board, depth - 1, alpha, beta, False)
                    board[row][col] = ""  # Hamleyi geri al
                    max_eval = max(max_eval, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break  # Budama
        return max_eval

    # Minimizing Player
    else:
        min_eval = float('inf')
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == "":
                    board[row][col] = PLAYER
                    evaluation = minimax(board, depth - 1, alpha, beta, True)
                    board[row][col] = ""  # Hamleyi geri al
                    min_eval = min(min_eval, evaluation)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break  # Budama
        return min_eval


def ai_move():
    """
    Alpha-Beta Pruning kullanarak AI için en iyi hamleyi seç.
    """
    print("AI is thinking...")
    best_score = float('-inf')
    best_move = None

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "":
                board[row][col] = AI  # Deneme hamlesi
                score = minimax(board, depth=3, alpha=float('-inf'), beta=float('inf'), is_maximizing=False)
                board[row][col] = ""  # Hamleyi geri al
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        board[best_move[0]][best_move[1]] = AI
        print(f"AI places at {best_move}. Best score: {best_score}")
    else:
        print("No valid moves for AI!")
    print(f"AI places at {best_move}. Best score: {best_score}")



def display_winner(winner):
    """Display the winner on the screen."""
    SCREEN.fill(WHITE)  # Clear the screen
    winner_text = BUTTON_FONT.render(f"The winner is: {winner}", True, BLACK)
    SCREEN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 100))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds to show the winner

def game_over():
    """End game and ask to play again."""
    draw_board()
    display_score()
    pygame.display.update()

    # Determine winner
    winner = "AI" if is_winner(AI) else "Player" if is_winner(PLAYER) else "Draw"
    display_winner(winner)

    # Game over message
    SCREEN.fill(WHITE)  # Clear the screen for the question
    game_over_text = BUTTON_FONT.render(f"The winner is: {winner}", True, BLACK)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))

    question_text = BUTTON_FONT.render("Play again?", True, BLACK)
    SCREEN.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, HEIGHT // 2))

    # "Yes" and "No" buttons
    yes_button = pygame.draw.rect(SCREEN, BLUE, (WIDTH // 2 - 120, HEIGHT // 2 + 50, 100, 50))
    no_button = pygame.draw.rect(SCREEN, RED, (WIDTH // 2 + 20, HEIGHT // 2 + 50, 100, 50))

    yes_text = BUTTON_FONT.render("Yes", True, WHITE)
    no_text = BUTTON_FONT.render("No", True, WHITE)
    SCREEN.blit(yes_text,
                (yes_button.centerx - yes_text.get_width() // 2, yes_button.centery - yes_text.get_height() // 2))
    SCREEN.blit(no_text, (no_button.centerx - no_text.get_width() // 2, no_button.centery - no_text.get_height() // 2))
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    reset_board()  # Reset the board
                    SCREEN.fill(WHITE)  # Clear the screen to remove "Play Again" text
                    waiting_for_input = False  # Restart the game
                elif no_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Exit the game



def main():
    """Main game loop."""
    global player_score, ai_score, feedback_message
    game_over_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over_flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    clicked_row = mouse_y // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE

                    if clicked_row < ROWS and board[clicked_row][clicked_col] == "":
                        board[clicked_row][clicked_col] = PLAYER
                        feedback_message = "AI is thinking..."
                        if is_winner(PLAYER):
                            player_score += 1
                            feedback_message = "You win!"
                            game_over_flag = True
                        else:
                            ai_move()
                            if is_winner(AI):
                                ai_score += 1
                                feedback_message = "AI wins!"
                                game_over_flag = True
                            else:
                                feedback_message = "Your Turn!"

        draw_lines()
        draw_board()
        display_score()


        if game_over_flag:
            game_over()
            game_over_flag = False

        pygame.display.update()


if __name__ == "__main__":
    main()
