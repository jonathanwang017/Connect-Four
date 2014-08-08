import os, pygame, math, sys
import pygame._view
from pygame.locals import *

# directory variables
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# screen constants
# SCREEN_X = 112
# SCREEN_Y = 128
# TILE_SIZE = 16
SCREEN_X = 224
SCREEN_Y = 256
TILE_SIZE = 32

# image constants
# RED_PIECE_IMG = 'red_piece_16.gif'
# YELLOW_PIECE_IMG = 'yellow_piece_16.gif'
# RIGHT_ARROW_IMG = 'right_arrow_16.gif'
# LEFT_ARROW_IMG = 'left_arrow_16.gif'
# DOWN_ARROW_IMG = 'down_arrow_16.gif'
# BOARD_IMG = 'board_16.gif'
# WIN_RED_IMG = 'win_red_16.gif'
# WIN_YELLOW_IMG = 'win_yellow_16.gif'
RED_PIECE_IMG = 'red_piece_32.gif'
YELLOW_PIECE_IMG = 'yellow_piece_32.gif'
RIGHT_ARROW_IMG = 'right_arrow_32.gif'
LEFT_ARROW_IMG = 'left_arrow_32.gif'
DOWN_ARROW_IMG = 'down_arrow_32.gif'
BOARD_IMG = 'board_32.gif'
WIN_RED_IMG = 'win_red_32.gif'
WIN_YELLOW_IMG = 'win_yellow_32.gif'

BACKGROUND_COLOR = (120, 170, 240)

# function to load image
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(pygame.compat.geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# piece base sprite
class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, image, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        self.image, self.rect = load_image(image)

    def update(self):
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.screen.blit(self.image, self.rect)

class DroppedPieceSprite(PieceSprite):
    def __init__(self, screen, x, y, color):
        if color == 1:
            PieceSprite.__init__(self, RED_PIECE_IMG, screen, x, y)
        elif color == 2:
            PieceSprite.__init__(self, YELLOW_PIECE_IMG, screen, x, y)

class SelectedPieceSprite(PieceSprite):
    def __init__(self, screen, x, y, color):
        if color == 1:
            PieceSprite.__init__(self, RED_PIECE_IMG, screen, x, y)
        elif color == 2:
            PieceSprite.__init__(self, YELLOW_PIECE_IMG, screen, x, y)

class RightArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, RIGHT_ARROW_IMG, screen, x, y)

class LeftArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, LEFT_ARROW_IMG, screen, x, y)

class DownArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, DOWN_ARROW_IMG, screen, x, y)

class BoardSprite(PieceSprite):
    def __init__(self, screen):
        PieceSprite.__init__(self, BOARD_IMG, screen, 0, 2)

class WinScreenSprite(PieceSprite):
    def __init__(self, screen, player):
        if player == 1:
            PieceSprite.__init__(self, WIN_RED_IMG, screen, 0, 0)
        elif player == 2:
            PieceSprite.__init__(self, WIN_YELLOW_IMG, screen, 0, 0)

# check player win
def check_win(board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 1:
                if check_link(board, x, y, 1, None) == 4:
                    win_screen(1)
            elif board[x][y] == 2:
                if check_link(board, x, y, 2, None) == 4:
                    win_screen(2)

# find length of connections
def check_link(board, x, y, player, direction):
    if direction == None:
        if x + 1 < 7 and board[x + 1][y] == player:
            return 1 + check_link(board, x + 1, y, player, 'horizontal_right')
        elif x - 1 >= 0 and board[x - 1][y] == player:
            return 1 + check_link(board, x - 1, y, player, 'horizontal_left')
        elif y + 1 < 6 and board[x][y + 1] == player:
            return 1 + check_link(board, x, y + 1, player, 'vertical_down')
        elif y - 1 >= 0 and board[x][y - 1] == player:
            return 1 + check_link(board, x, y - 1, player, 'vertical_up')
        elif x + 1 < 7 and y + 1 < 6 and board[x + 1][y + 1] == player:
            return 1 + check_link(board, x + 1, y + 1, player, 'diagonal_right_down')
        elif x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] == player:
            return 1 + check_link(board, x - 1, y - 1, player, 'diagonal_left_up')
        elif x + 1 < 7 and y - 1 >= 0 and board[x + 1][y - 1] == player:
            return 1 + check_link(board, x + 1, y - 1, player, 'diagonal_right_up')
        elif x - 1 >= 0 and y + 1 < 6 and board[x - 1][y + 1] == player:
            return 1 + check_link(board, x - 1, y + 1, player, 'diagonal_left_down')
    elif direction == 'vertical_down':
        if y + 1 < 6 and board[x][y + 1] == player:
            return 1 + check_link(board, x, y + 1, player, 'vertical_down')
    elif direction == 'vertical_up':
        if y - 1 >= 0 and board[x][y - 1] == player:
            return 1 + check_link(board, x, y - 1, player, 'vertical_up')
    elif direction == 'horizontal_right':
        if x + 1 < 7 and board[x + 1][y] == player:
            return 1 + check_link(board, x + 1, y, player, 'horizontal_right')
    elif direction == 'horizontal_left':
        if x - 1 >= 0 and board[x - 1][y] == player:
            return 1 + check_link(board, x - 1, y, player, 'horizontal_left')
    elif direction == 'diagonal_right_down':
        if x + 1 < 7 and y + 1 < 6 and board[x + 1][y + 1] == player:
            return 1 + check_link(board, x + 1, y + 1, player, 'diagonal_right_down')
    elif direction == 'diagonal_left_up':
        if x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] == player:
            return 1 + check_link(board, x - 1, y - 1, player, 'diagonal_left_up')
    elif direction == 'diagonal_right_up':
        if x + 1 < 7 and y - 1 >= 0 and board[x + 1][y - 1] == player:
            return 1 + check_link(board, x + 1, y - 1, player, 'diagonal_right_up')
    elif direction == 'diagonal_left_down':
        if x - 1 >= 0 and y + 1 < 6 and board[x - 1][y + 1] == player:
            return 1 + check_link(board, x - 1, y + 1, player, 'diagonal_left_down')
    return 1

def main_loop():
    # initialize pygame and variables
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Connect Four')
    pygame.mouse.set_visible(0)

    # initialize board
    board = [[0,0,0,0,0,0], \
             [0,0,0,0,0,0], \
             [0,0,0,0,0,0], \
             [0,0,0,0,0,0], \
             [0,0,0,0,0,0], \
             [0,0,0,0,0,0], \
             [0,0,0,0,0,0]]

    # initialize variables and sprite lists
    pieces = []
    arrows = []
    turn = 1
    sel_col = 3

    arrows.append(RightArrowSprite(screen, sel_col + 1, 0))
    arrows.append(LeftArrowSprite(screen, sel_col - 1, 0))
    arrows.append(DownArrowSprite(screen, sel_col, 1))
    sel_piece = SelectedPieceSprite(screen, sel_col, 0, turn)
    board_bg = BoardSprite(screen)

    # game loop
    while True:

        # check event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_r:
                    main_loop()
                elif event.key == K_RETURN:
                    printBoard = ''
                    for i in range(6):
                        for j in range(7):
                            printBoard += str(board[j][i]) + ','
                        printBoard += '\n'
                    print printBoard
                elif event.key == K_DOWN:
                    if board[sel_col][0] == 0:
                        filled = -1
                        row = SCREEN_Y / TILE_SIZE - 1
                        while board[sel_col][filled] != 0:
                            row -= 1
                            filled -= 1
                        board[sel_col][filled] = turn
                        pieces.append(DroppedPieceSprite(screen, sel_col, row, turn))
                        turn = 3 - turn
                        sel_col = 3
                        sel_piece = SelectedPieceSprite(screen, sel_col, 0, turn)
                elif event.key == K_LEFT:
                    if sel_col > 0:
                        sel_col -= 1
                elif event.key == K_RIGHT:
                    if sel_col < 6:
                        sel_col += 1

        # draw sprites on screen
        screen.fill(BACKGROUND_COLOR)

        arrows[0].x = sel_col + 1
        arrows[1].x = sel_col - 1
        arrows[2].x = sel_col
        sel_piece.x = sel_col

        board_bg.update()
        for piece in pieces:
            piece.update()
        for arrow in arrows:
            arrow.update()
        sel_piece.update()

        # refresh screen
        pygame.display.flip()

        # check game end
        check_win(board)

def win_screen(player):
    # initialize pygame and variables
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Connect Four')
    pygame.mouse.set_visible(0)

    winScreen = WinScreenSprite(screen, player)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_r:
                    main_loop()
                elif event.key == K_RETURN:
                    main_loop()

        winScreen.update()
        pygame.display.flip()

def main():
    main_loop()

if __name__ == '__main__':
    main()
