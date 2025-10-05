#!/usr/bin/python3
import pygame
import sys
import math

# --- Constants ---
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
YELLOW= (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

def print_board(board):
    for row in reversed(board):
        print(row)

def winning_move(board, piece):
    # Horizontal check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (board[r][c] == piece and board[r][c+1] == piece and
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r+1][c] == piece and
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True

    # Diagonal (up-right) check: r -> r+1, c -> c+1
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True

    # Diagonal (down-right) check: r -> r-1, c -> c+1
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (board[r][c] == piece and board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True

    return False

def is_draw(board):
    for c in range(COLUMN_COUNT):
        if board[ROW_COUNT - 1][c] == 0:
            return False
    return True

def draw_board(screen, board, SQUARESIZE, RADIUS, width, height):
    # Draw the board (blue rectangles and empty circles)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE,
                             (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(c * SQUARESIZE + SQUARESIZE / 2),
                                int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),
                               RADIUS)

    # Draw the pieces (flip row when drawing)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2),
                                    int(height - (r * SQUARESIZE + SQUARESIZE / 2))),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2),
                                    int(height - (r * SQUARESIZE + SQUARESIZE / 2))),
                                   RADIUS)
    pygame.display.update()

def main():
    pygame.init()

    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE  # extra row on top for the indicator
    size = (width, height)
    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect Four")

    # Font: try default, fall back if not available
    try:
        myfont = pygame.font.SysFont("monospace", 75)
    except:
        myfont = pygame.font.Font(None, 75)

    board = create_board()
    print_board(board)

    game_over = False
    turn = 0  # 0 -> player 1 (RED), 1 -> player 2 (YELLOW)

    draw_board(screen, board, SQUARESIZE, RADIUS, width, height)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse motion: show floating piece on top row
            if event.type == pygame.MOUSEMOTION:
                # clear the top area
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            # Mouse click: place piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if col < 0 or col >= COLUMN_COUNT:
                    # safety, shouldn't happen from clicks inside window
                    continue

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    if row is None:
                        continue

                    # place piece
                    piece = 1 if turn == 0 else 2
                    drop_piece(board, row, col, piece)

                    # draw board after move
                    draw_board(screen, board, SQUARESIZE, RADIUS, width, height)
                    print_board(board)

                    # check for win
                    if winning_move(board, piece):
                        label_text = "Player 1 wins!" if piece == 1 else "Player 2 wins!"
                        label_color = RED if piece == 1 else YELLOW
                        label = myfont.render(label_text, True, label_color)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                    elif is_draw(board):
                        label = myfont.render("Draw!", True, (200, 200, 200))
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True

                    # switch turns
                    turn = (turn + 1) % 2

        if game_over:
            pygame.time.wait(2500)
            pygame.quit()
            return

if __name__ == "__main__":
    main()

