from constants import *
import pygame
import math


class Piece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False  # Indicates if the piece has been promoted to a king

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

    def get_position(self):
        """Calculates the x and y pixel positions of the piece."""
        self.x = MARGIN + CELL_SIZE * self.column + CELL_SIZE // 2
        self.y = CELL_SIZE * self.row + CELL_SIZE // 2

    def draw(self, win) -> None:
        """Draws the piece on the game window."""
        radius = self.radius
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius + 4)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # Draw the king indicator (e.g., a smaller circle or crown image)
            pygame.draw.circle(win, GOLD, (self.x, self.y), radius - 4)
            pygame.draw.circle(win, self.color, (self.x, self.y), radius - 8)

    def king_promotion(self):
        """Promotes the piece to a king."""
        self.king = True

    def update_position(self, row, column):
        """Updates the piece's position on the board and recalculates pixel position."""
        self.row = row
        self.column = column
        self.get_position()

    def clicked(self, pos):
        """Checks if the piece has been clicked based on mouse position."""
        mouse_x, mouse_y = pos
        distance = math.hypot(mouse_x - self.x, mouse_y - self.y)
        return distance <= self.radius
