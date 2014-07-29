import os, pygame, math, sys
import pygame._view
from pygame.locals import *

# directory variables
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# screen constants
SCREEN_X = 112
SCREEN_Y = 96
TILE_SIZE = 16

# image constants
RED_PIECE_16_IMG = 'red_piece_16.gif'
YELLOW_PIECE_16_IMG = 'yellow_piece_16.gif'
RED_PIECE_32_IMG = 'red_piece_32.gif'
YELLOW_PIECE_32_IMG = 'yellow_piece_32.gif'
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


def main_loop():
    # initialize pygame and variables
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Connect Four')
    pygame.mouse.set_visible(0)

    # sprite groups
    red_pieces = []
    yellow_pieces = []

    red_pieces.append(RedPieceSprite(screen, 0, 0))

    # game loop
    while True:
        # check event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

        # draw sprites on screen
        screen.fill(BACKGROUND_COLOR)
        for red_piece in red_pieces:
            red_piece.update()

        # refresh screen
        pygame.display.flip()

def main():
    main_loop()

if __name__ == '__main__':
    main()
