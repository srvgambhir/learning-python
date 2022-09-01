from random import random
import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COL_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_TOKEN = 1
AI_TOKEN = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_token(board, row, col, token):
    board[row][col] = token


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, token):
    # Check horizontal locations for win
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == token and board[r][c + 1] == token and board[r][c + 2] == token and board[r][
                c + 3] == token:
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == token and board[r + 1][c] == token and board[r + 2][c] == token and board[r + 3][
                c] == token:
                return True

    # Check for positively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == token and board[r + 1][c + 1] == token and board[r + 2][c + 2] == token and board[r + 3][
                c + 3] == token:
                return True

    # Check for negatively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == token and board[r - 1][c + 1] == token and board[r - 2][c + 2] == token and board[r - 3][
                c + 3] == token:
                return True

def eval_window(window, token):
    score = 0

    opp_token = PLAYER_TOKEN
    if token == PLAYER_TOKEN:
        opp_token = AI_TOKEN

    # this condition is probably redundant
    if window.count(token) == 4:
        score += 100


    elif window.count(token) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(token) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Weigh us getting 3 in a row above opponent getting 3 in a row
    if window.count(opp_token) == 3 and window.count(EMPTY) == 1:
        score -= 4   

    return score 

def score_pos(board, token):
    score = 0

    # Score for center
    # Preference given to moves in the center column
    center_arr = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center_arr.count(token)
    score += center_count * 3

    # Score for horizontal
    for r in range(ROW_COUNT):
        row_arr = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = row_arr[c:c+WINDOW_LENGTH]
            score += eval_window(window, token)

    # Score for Vertical
    for c in range(COL_COUNT):
        col_arr = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_arr[r:r+WINDOW_LENGTH]
            score += eval_window(window, token)

    # Score for positive sloped diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, token)

    # Score for negative sloped diagonals
    #
    # Alternative nested for loop:
    #
    # for r in range(ROW_COUNT-3):
    #     for c in range(COL_COUNT-3):
    #         window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
    #
    for r in range(ROW_COUNT-3):
        for c in range(3,COL_COUNT):
            window = [board[r+i][c-i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, token)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_TOKEN) or winning_move(board, AI_TOKEN) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Base case - terminal conditions
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_TOKEN):
                return (1000000000000000, None)
            elif winning_move(board, PLAYER_TOKEN):
                return (-1000000000000000, None)
            else: # Game is over, no more valid moves
                return (0, None)
        else: # Depth is zero
            return (score_pos(board, AI_TOKEN), None)

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_token(temp_board, row, col, AI_TOKEN)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[0]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value, best_col)
    
    else: # Minimizing Player
        value = math.inf
        worst_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_token(temp_board, row, col, PLAYER_TOKEN)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[0]
            if new_score < value:
                value = new_score
                worst_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (value, worst_col)


def get_valid_locations(board):
    valid_locations = []
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, token):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_token(temp_board, row, col, token)
        score = score_pos(temp_board, token)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_TOKEN:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_TOKEN:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()


board = create_board()
game_over = False
turn = random.randint(PLAYER, AI)

pygame.init()

SQUARESIZE = 100

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:

                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_token(board, row, col, PLAYER_TOKEN)

                    if winning_move(board, PLAYER_TOKEN):
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    
                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2


    # Ask for Player 2 Input
    if turn == AI and not game_over:

        col = minimax(board, 5, -math.inf, math.inf, True)[1]

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_token(board, row, col, AI_TOKEN)

            if winning_move(board, AI_TOKEN):
                label = myfont.render("Player 2 Wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)