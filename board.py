import pygame

# CONSTANTS

ROWS = 8
COLUMNS = 8
WIDTH = HEIGHT = 1000
CELL_SIZE = WIDTH // COLUMNS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Board():
    # NEED TO FINISH THIS
    def __init__(self):
        self.board = []
        self.pieces = {'P1': 12, 'P2': 12}
        self.kings = {'P1': 0, 'P2': 0}


    def draw(self, window):
        window.fill(BLACK)

        # DRAWS THE BOARD

        for row in range(ROWS):
            # It start at rows%2 so it can be either 0 or 1
            # (the white tiles are in opposite positions every row)
            # Increasing twice every iteration to skip over the black tile
            for column in range(row%2, COLUMNS, 2): 
                pygame.draw.rect(window, WHITE, (row*CELL_SIZE, column*CELL_SIZE, CELL_SIZE, CELL_SIZE))

