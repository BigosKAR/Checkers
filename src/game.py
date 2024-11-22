import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button


class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.lower_section = LowerSection(window, SILVER)
        self.move_history = []
        self.redo_stack = []
        self.turn = 'RED'  # Keep track of which player's turn it is

    def move_piece(self, piece, new_row, new_col):
        """Move a piece and save the move details."""
        move_details = self.board.move(piece, new_row, new_col)
        if not move_details:
            # Move was invalid; do not proceed
            print("Move was invalid.")
            return False  # Return early since move failed

        # Save move details for undo
        self.move_history.append(move_details)
        self.redo_stack.clear()  # Clear redo stack after a new move

        # Switch turn
        self.switch_turn()

        game_over_status = self.board.check_game_over()
        if game_over_status:
            print(game_over_status)  # Notify the result (can later be integrated into UI)
            return game_over_status  # Optional return for game-over state

        print(f"Move recorded: {piece.player} piece to ({new_row}, {new_col})")
        return True

    def undo_move(self):
        """Undo the last move."""
        if not self.move_history:
            print("No moves to undo!")
            return
        last_move = self.move_history.pop()
        self.board.undo_move(last_move)
        self.redo_stack.append(last_move)
        self.switch_turn()
        print("Move undone.")

    def redo_move(self):
        """Redo the last undone move."""
        if not self.redo_stack:
            print("No moves to redo!")
            return
        move = self.redo_stack.pop()
        self.board.redo_move(move)
        self.move_history.append(move)
        self.switch_turn()
        print("Move redone.")

    def switch_turn(self):
        self.turn = 'WHITE' if self.turn == 'RED' else 'RED'

    def select(self, pos):
        if self.board.selected_piece is None:
            piece = self.board.get_piece_at_position(pos)
            if piece and piece.player == self.turn:
                self.board.selected_piece = piece
                print(f"Selected {piece.player} piece at ({piece.row}, {piece.column})")
                return True  # Piece selected
            else:
                print("No valid piece selected.")
                return False
        else:
            dest_row, dest_column = self.board.coords_to_row_col(pos)
            if dest_row is not None and dest_column is not None:
                valid_moves = self.board.get_valid_moves(self.board.selected_piece)
                if (dest_row, dest_column) in valid_moves:
                    move_result = self.move_piece(self.board.selected_piece, dest_row, dest_column)
                    self.board.selected_piece = None  # Reset selection after attempting move
                    return move_result
                else:
                    print("Invalid move selected.")
                    self.board.selected_piece = None
                    return False
            else:
                print("Invalid position.")
                self.board.selected_piece = None
                return False

    def select_button(self, pos):
        for button in self.lower_section.buttons:
            if button.b_clicked(pos):
                return button
        return None
