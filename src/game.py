import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button
import copy

class Game():
    def __init__(self, window):
        self.window = window
        self.board = Board(window)
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
        #CHECK IF TWO POSSIBLE MOVEMENTS TO THE SAME PLACE
        """Move a piece and save the new board state."""
        move_successful = self.board.move(new_row, new_col)
        if not move_successful:
            print("Move was invalid.")
            return False

        # game_over_status = self.board.check_game_over()
        # if game_over_status:
        #     print(game_over_status)  # Notify the result (can later be integrated into UI)
        #     return game_over_status  # Optional return for game-over state

        self.push()  # Save the new board state
        self.remove()  # Clear the redo stack
        print(f"Move recorded: {self.board.selected_piece} to ({new_row}, {new_col})")
        return True

    def undo_move(self):
        """Call pop to undo the last move."""
        self.pop()

    # Function used to select a piece or move selected piece
    def select(self, pos):
        if self.board.selected_piece is None:
            for row in range(ROWS):
                for column in range(COLUMNS):
                    piece = self.board.board[row][column]
                    if piece != 0 and piece.clicked(pos):
                        self.board.selected_piece = piece
                        self.board.store_valid_moves()
                        print(f"Selected {piece.player} piece at ({piece.row}, {piece.column})")
                        return True  # Piece selected
            print("No piece selected.")
            return False
        else:
            dest_row, dest_column = self.coords_to_row_col(pos)
            if dest_row is not None and dest_column is not None:
                # GET MOVES IN MOVE_PIECE
                move_result = self.move_piece(dest_row, dest_column)
                if move_result:
                    self.board.reset_move_details()
                self.board.selected_piece = None  # Reset selection after attempting move
                return move_result
            else:
                print("Invalid position.")
                self.board.reset_move_details()
                self.board.selected_piece = None
                return False

    def select_button(self, pos):
        for button in self.lower_section.buttons:
            if button.b_clicked(pos):
                return button
        return None

    # Function turns coordinates from get_pos() and turns into row and column number
    # In game.py
    # In game.py
    def coords_to_row_col(self, pos):
        x, y = pos
        if 0 <= y < (HEIGHT - BUTTON_HUD_HEIGHT) and 0 <= x < WIDTH:
            column = x // CELL_SIZE
            row = y // CELL_SIZE
            return int(row), int(column)  # Ensure row and column are integers
        return None, None


