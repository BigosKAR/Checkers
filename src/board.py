import pygame
from constants import *
from piece import Piece

class Board():
    # Perimeters for the board such as pieces each color has, number of kings, and current selected piece
    # With initialization it also creates the 2D array
    def __init__(self):
        self.board = []
        self.pieces = {'RED': 12, 'WHITE': 12}
        self.kings = {'RED': 0, 'WHITE': 0}
        self.selected_piece = None
        self.add_pieces()

    # FUNCTIONS FOR INITIALIZING THE BOARD

    def draw_board(self, window) -> None:
        for row in range(ROWS):
            # It start at rows%2 so it can be either 0 or 1
            # (the white tiles are in opposite positions every row)
            # Increasing twice every iteration to skip over the black tile
            # Drawing black and white tiles
            for white in range(row%2, COLUMNS, 2): 
                pygame.draw.rect(window, WHITE, (row*CELL_SIZE, white*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for black in range(row%2-1, ROWS, 2):
                pygame.draw.rect(window, BLACK, (row*CELL_SIZE, black*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Functions that adds the pieces to a 2D array
    # Either the object or zeros
    def add_pieces(self) -> None:
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    # Draws the whole board (first -> the board, then it looks at the 2D array to draw the pieces)
    def draw(self, window) -> None:
        self.draw_board(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)
                    
