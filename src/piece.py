from constants import *
import pygame
import math

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
        self.radius = CELL_SIZE//2 - 5

        # # Calculate position
        # def get_position(self):
        #     self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        #     self.y = CELL_SIZE * self.row + CELL_SIZE // 2

    # drawing the individual piece
    def draw(self, win) -> None:
        radius = CELL_SIZE//2 
        pygame.draw.circle(win, self.color, (self.x, self.y), radius-10)
        
    def is_clicked(self, pos):
        mouse_x, mouse_y = pos
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius

    def clicked(self, pos):
        if self.is_clicked(pos):
            print(f"CLICKED THE PIECE AT row: {self.row+1}, column: {self.column+1}")
        