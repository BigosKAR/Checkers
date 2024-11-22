from constants import *
import pygame
import math


class Piece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False  # Used to check if the piece was promoted

        # Assign player and direction based on color
        if self.color == RED:
            self.direction = -1  # RED pieces move upwards
            self.player = 'RED'
        else:
            self.direction = 1   # WHITE pieces move downwards
            self.player = 'WHITE'

        self.x = 0
        self.y = 0
        self.get_position()
        self.radius = CELL_SIZE // 2 - 10

    # Calculate position
    def get_position(self):
        self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        self.y = CELL_SIZE * self.row + CELL_SIZE // 2

    # Drawing the individual piece
    def draw(self, win) -> None:
        radius = CELL_SIZE // 2 - 10
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius + 4)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(win, GOLD, (self.x, self.y), radius - 4)
            pygame.draw.circle(win, self.color, (self.x, self.y), radius - 8)

    def king_promotion(self):
        self.king = True

    # Changing the position attributes for a piece
    def update_position(self, row, column):
        self.row = row
        self.column = column
        self.get_position()

    def clicked(self, pos):
        mouse_x, mouse_y = pos
        distance = math.hypot(mouse_x - self.x, mouse_y - self.y)
        return distance <= self.radius
