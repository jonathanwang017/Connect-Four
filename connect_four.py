import os, pygame, math, sys
import pygame._view
from pygame.locals import *

# directory variables
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# screen constants
SCREEN_X = 112
SCREEN_Y = 128
TILE_SIZE = 16

# image constants
RED_PIECE_16_IMG = 'red_piece_16.gif'
YELLOW_PIECE_16_IMG = 'yellow_piece_16.gif'
RED_PIECE_32_IMG = 'red_piece_32.gif'
YELLOW_PIECE_32_IMG = 'yellow_piece_32.gif'
RIGHT_ARROW_16_IMG = 'right_arrow_16.gif'
LEFT_ARROW_16_IMG = 'left_arrow_16.gif'
DOWN_ARROW_16_IMG = 'down_arrow_16.gif'
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

class YellowPieceSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, YELLOW_PIECE_16_IMG, screen, x, y)

class RedPieceSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, RED_PIECE_16_IMG, screen, x, y)

class DroppedPieceSprite(PieceSprite):
    def __init__(self, screen, x, y, color):
        if color == 1:
            PieceSprite.__init__(self, RED_PIECE_16_IMG, screen, x, y)
        elif color == 2:
            PieceSprite.__init__(self, YELLOW_PIECE_16_IMG, screen, x, y)

class SelectedPieceSprite(PieceSprite):
    def __init__(self, screen, x, y, color):
        if color == 1:
            PieceSprite.__init__(self, RED_PIECE_16_IMG, screen, x, y)
        elif color == 2:
            PieceSprite.__init__(self, YELLOW_PIECE_16_IMG, screen, x, y)

    def update(self, x):
        self.x = x
        self.rect.topleft = (self.x * TILE_SIZE, 0)
        self.screen.blit(self.image, self.rect)


class RightArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, RIGHT_ARROW_16_IMG, screen, x, y)

class LeftArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, LEFT_ARROW_16_IMG, screen, x, y)

class DownArrowSprite(PieceSprite):
    def __init__(self, screen, x, y):
        PieceSprite.__init__(self, DOWN_ARROW_16_IMG, screen, x, y)

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

    # sprite groups
    # red_pieces = []
    # yellow_pieces = []
    pieces = []
    arrows = []
    turn = 1
    sel_col = 3

    arrows.append(RightArrowSprite(screen, sel_col + 1, 0))
    arrows.append(LeftArrowSprite(screen, sel_col - 1, 0))
    arrows.append(DownArrowSprite(screen, sel_col, 1))
    sel_piece = SelectedPieceSprite(screen, sel_col, 0, turn)

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
                    main_loop();
                elif event.key == K_RETURN:
                    print [board[i] for i in range(6)]
                elif event.key == K_DOWN:
                    if board[sel_col][0] == 0:
                        filled = -1
                        row = SCREEN_Y / 16 - 1
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

        for piece in pieces:
            piece.update()
        for arrow in arrows:
            arrow.update()
        sel_piece.update(sel_col)

        # refresh screen
        pygame.display.flip()

def main():
    main_loop()

if __name__ == '__main__':
    main()
