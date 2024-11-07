import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button

class Game():
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.lower_section = LowerSection(window, SILVER)

    # Function used to select a piece or 
    def select(self, pos):
        if self.board.selected_piece == None:
            for row in range(ROWS):
                for column in range(COLUMNS):
                    if self.board.board[row][column] != 0:
                        if self.board.board[row][column].clicked(pos):
                            self.board.selected_piece = self.board.board[row][column]
        else:
            dest_row, dest_column = self.coords_to_row_col(pos)
            self.board.move(dest_row, dest_column)
            self.board.selected_piece = None

    def select_button(self, pos):
        for button in self.lower_section.buttons:
            if button.b_clicked(pos):
                return button
        return None

    # Function turns coordinates from get_pos() and turns into row and column number
    def coords_to_row_col(self, pos):
        x, y = pos
        if 0 <= y < (HEIGHT-BUTTON_HUD_HEIGHT) and 0 <= x < WIDTH:
            row = y // CELL_SIZE
            column = x // CELL_SIZE
            return row, column
        return None, None
                    
    