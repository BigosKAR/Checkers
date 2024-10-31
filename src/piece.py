from constants import *
import pygame

class Piece():
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False # used to check if the piece was promoted
        if self.color == RED:
            self.direction = 1
        else:
            self.direction = -1
        self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        self.y = CELL_SIZE * self.row + CELL_SIZE // 2

        # # Calculate position
        # def get_position(self):
        #     self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        #     self.y = CELL_SIZE * self.row + CELL_SIZE // 2

    # drawing the individual piece
    def draw(self, win) -> None:
        radius = CELL_SIZE//2 
        pygame.draw.circle(win, self.color, (self.x, self.y), radius-10)
        