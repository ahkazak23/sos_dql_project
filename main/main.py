import pygame
import sys
import math

# Pygame Ayarları
pygame.init()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Ekran Ayarları
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
MARKER_WIDTH = 15
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("XOX - Minimax ile Yapay Zeka")
SCREEN.fill(WHITE)

# Tahta
ROWS, COLS = 3, 3
CELL_SIZE = WIDTH // COLS

# Tahta Tanımları
board = [["" for _ in range(COLS)] for _ in range(ROWS)]

# Yazı Tipi
FONT = pygame.font.Font(None, 80)
BUTTON_FONT = pygame.font.Font(None, 40)

# Oyuncu ve AI
PLAYER = "X"
AI = "O"

# Çizgiler
def draw_lines():
    for row in range(1, ROWS):
        pygame.draw.line(SCREEN, BLACK, (0, CELL_SIZE * row), (WIDTH, CELL_SIZE * row), LINE_WIDTH)
    for col in range(1, COLS):
        pygame.draw.line(SCREEN, BLACK, (CELL_SIZE * col, 0), (CELL_SIZE * col, HEIGHT), LINE_WIDTH)

# Tahta Çizimi
def draw_board():
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

# Tahta Kontrol
def is_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    if all(board[i][i] == player for i in range(ROWS)) or all(board[i][ROWS - 1 - i] == player for i in range(ROWS)):
        return True
    return False

def is_full():
    return all(cell != "" for row in board for cell in row)

# Minimax Algoritması
def minimax(depth, is_maximizing):
    if is_winner(AI):
        return 1
    if is_winner(PLAYER):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == "":
                    board[row][col] = AI
                    score = minimax(depth + 1, False)
                    board[row][col] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == "":
                    board[row][col] = PLAYER
                    score = minimax(depth + 1, True)
                    board[row][col] = ""
                    best_score = min(best_score, score)
        return best_score

# AI'nin Hamlesi
def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "":
                board[row][col] = AI
                score = minimax(0, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = AI
# Kazananı Ekrana Yazdırma
def display_winner(winner):
    if winner == "Oyuncu":
        winner_text = FONT.render("Kazandın!", True, BLUE)
        winner_rect = pygame.Rect(WIDTH // 2 - winner_text.get_width() // 2 - 20, HEIGHT // 2 - winner_text.get_height() // 2 - 50, winner_text.get_width() + 40, winner_text.get_height() + 20)
        pygame.draw.rect(SCREEN, (0, 255, 0), winner_rect)  # Yeşil arka plan
    elif winner == "AI":
        winner_text = FONT.render("Kaybettin!", True, WHITE)
        winner_rect = pygame.Rect(WIDTH // 2 - winner_text.get_width() // 2 - 20, HEIGHT // 2 - winner_text.get_height() // 2 - 50, winner_text.get_width() + 40, winner_text.get_height() + 20)
        pygame.draw.rect(SCREEN, (255, 0, 0), winner_rect)  # Kırmızı arka plan
    elif winner == "Beraberlik":
        winner_text = FONT.render("Beraberlik!", True, WHITE)
        winner_rect = pygame.Rect(WIDTH // 2 - winner_text.get_width() // 2 - 20, HEIGHT // 2 - winner_text.get_height() // 2 - 50, winner_text.get_width() + 40, winner_text.get_height() + 20)
        pygame.draw.rect(SCREEN, (169, 169, 169), winner_rect)  # Gri arka plan

    # Yazıyı ekrana yerleştir
    SCREEN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2 - 50))

# Tekrar Oyna Butonu
def draw_play_again_button():
    button_text = BUTTON_FONT.render("Tekrar Oyna", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(SCREEN, GREEN, button_rect)
    SCREEN.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    return button_rect

# Ana Döngü
def main():
    global board  # Buraya global eklenmeli
    draw_lines()
    running = True
    player_turn = True
    winner = None
    button_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not winner:
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE

                if board[clicked_row][clicked_col] == "":
                    board[clicked_row][clicked_col] = PLAYER
                    if is_winner(PLAYER):
                        winner = "Oyuncu"
                    elif is_full():
                        winner = "Beraberlik"
                    else:
                        player_turn = False

            # Tekrar oyna butonuna tıklanması
            if event.type == pygame.MOUSEBUTTONDOWN and winner:
                mouse_x, mouse_y = event.pos
                if button_rect and button_rect.collidepoint(mouse_x, mouse_y):
                    # Oyun sıfırlama
                    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
                    player_turn = True
                    winner = None

        if not player_turn and running and not winner:
            ai_move()
            if is_winner(AI):
                winner = "AI"
            elif is_full():
                winner = "Beraberlik"
            else:
                player_turn = True

        SCREEN.fill(WHITE)
        draw_lines()
        draw_board()

        if winner:
            display_winner(winner)
            button_rect = draw_play_again_button()

        pygame.display.update()

if __name__ == "__main__":
    main()
