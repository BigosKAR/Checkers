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

        self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        self.y = CELL_SIZE * self.row + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2 - 5\
        
        # Will be used to store possible moves/jumps when selecting this piece
        self.moves = None
        self.jumped = None

    # Calculate position
    def get_position(self):
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        self.x = CELL_SIZE * self.column + CELL_SIZE // 2
        self.y = CELL_SIZE * self.row + CELL_SIZE // 2

    # Drawing the individual piece
    def draw(self, win) -> None:
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        radius = CELL_SIZE // 2
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius - 8)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius - 10)
        if self.king:
            pygame.draw.circle(win, LIGHT_BLUE, (self.x, self.y), radius - 12, 3)

    def king_promotion(self):
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        self.king = True
        self.radius += 5  # Visual cue for king

    # Changing the position attributes for a piece
    def update_position(self, row, column):
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        self.row = row
        self.column = column
        self.get_position()

    def is_clicked(self, pos):
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        mouse_x, mouse_y = pos
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius

    def clicked(self, pos):
        """
        Runtime Complexity:
        - Average case = Worst case = O(1)
        """
        if self.is_clicked(pos):
            return True
