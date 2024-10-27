import pygame
from constants import *

class Board():
    # NEED TO FINISH THIS
    def __init__(self):
        self.board = []
        self.pieces = {'P1': 12, 'P2': 12}
        self.kings = {'P1': 0, 'P2': 0}


    def draw(self, window):

        # DRAWS THE BOARD
        for row in range(ROWS):
            # It start at rows%2 so it can be either 0 or 1
            # (the white tiles are in opposite positions every row)
            # Increasing twice every iteration to skip over the black tile
            # Drawing black and white tiles
            for white in range(row%2, COLUMNS, 2): 
                pygame.draw.rect(window, WHITE, (row*CELL_SIZE, white*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for black in range(row%2-1, ROWS, 2):
                pygame.draw.rect(window, BLACK, (row*CELL_SIZE, black*CELL_SIZE, CELL_SIZE, CELL_SIZE))
