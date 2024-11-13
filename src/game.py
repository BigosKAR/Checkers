import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button
import copy

class Game():
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.lower_section = LowerSection(window, SILVER)

        # Stacks for board states
        self.main_stack = [copy.deepcopy(self.board.board)]  # Start with the initial board
        self.temp_stack = []

    def push(self):
        # Push the current board state to the main stack.
        self.main_stack.append(copy.deepcopy(self.board.board))

    def pop(self):
        # Undo the last move by reverting to the previous board state.
        if len(self.main_stack) > 1:
            self.temp_stack.append(self.main_stack.pop())  # Save current state for redo
            self.board.board = copy.deepcopy(self.main_stack[-1])
            print("Move undone.")
        else:
            print("No moves to undo!")

    def remove(self):
        """Clear the redo stack after a new move."""
        self.temp_stack = []

    def redo_move(self):
        """Redo the last undone move."""
        if self.temp_stack:
            self.main_stack.append(self.temp_stack.pop())
            self.board.board = copy.deepcopy(self.main_stack[-1])
            print("Move redone.")
        else:
            print("No moves to redo!")

    def move_piece(self, new_row, new_col):
        """Move a piece and save the new board state."""
        self.board.move(new_row, new_col)
        game_over_status = self.board.check_game_over()
        if game_over_status:
            print(game_over_status)  # Notify the result (can later be integrated into UI)
            return game_over_status  # Optional return for game-over state
        self.push()  # Save the new board state
        self.remove()  # Clear the redo stack
        print(f"Move recorded: {self.board.selected_piece} to ({new_row}, {new_col})")

    def undo_move(self):
        """Call pop to undo the last move."""
        self.pop()

    # Function used to select a piece or move selected piece
    def select(self, pos):
        if self.board.selected_piece is None:
            for row in range(ROWS):
                for column in range(COLUMNS):
                    if self.board.board[row][column] != 0:
                        if self.board.board[row][column].clicked(pos):
                            self.board.selected_piece = self.board.board[row][column]
        else:
            dest_row, dest_column = self.coords_to_row_col(pos)
            if dest_row is not None and dest_column is not None:
                if self.board.board[dest_row][dest_column] == 0:
                    return self.move_piece(dest_row, dest_column)
                else:
                    print("Invalid move, cell occupied.")
                    self.board.selected_piece = None
            else:
                print("Invalid position.")
                self.board.selected_piece = None

    def select_button(self, pos):
        for button in self.lower_section.buttons:
            if button.b_clicked(pos):
                return button
        return None

    # Function turns coordinates from get_pos() and turns into row and column number
    def coords_to_row_col(self, pos):
        x, y = pos
        if 0 <= y < (HEIGHT - BUTTON_HUD_HEIGHT) and 0 <= x < WIDTH:
            row = y // CELL_SIZE
            column = x // CELL_SIZE
            return row, column
        return None, None
