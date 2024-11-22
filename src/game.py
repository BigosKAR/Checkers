import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button
from piece import Piece


class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.lower_section = LowerSection(window, SILVER)
        self.move_history = []
        self.redo_stack = []
        self.turn = 'RED'  # Keep track of which player's turn it is
        self.red_takes = []   # Stores data of pieces taken by red player (white pieces taken)
        self.white_takes = []  # Stores data of pieces taken by white player (red pieces taken)

    def inverted_bubble_sort(self, arr):
        """Sorts the array so that all 1s (kings) are on the left and 0s (normal pieces) on the right."""
        n = len(arr)
        for i in range(n):
            for j in range(n - 1, i, -1):
                if arr[j] > arr[j - 1]:
                    arr[j], arr[j - 1] = arr[j - 1], arr[j]

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

        # Update taken pieces arrays
        for row, col, captured_piece in move_details['captured']:
            captured_piece_data = 1 if captured_piece.king else 0
            if piece.player == 'RED':
                self.red_takes.append(captured_piece_data)
                # Perform inverted bubble sort
                self.inverted_bubble_sort(self.red_takes)
            elif piece.player == 'WHITE':
                self.white_takes.append(captured_piece_data)
                # Perform inverted bubble sort
                self.inverted_bubble_sort(self.white_takes)

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

        capturing_player = last_move['piece'].player

        # Remove captured pieces from taken arrays
        for row, col, captured_piece in last_move['captured']:
            captured_piece_data = 1 if captured_piece.king else 0
            if capturing_player == 'RED':
                if captured_piece_data in self.red_takes:
                    self.red_takes.remove(captured_piece_data)
            elif capturing_player == 'WHITE':
                if captured_piece_data in self.white_takes:
                    self.white_takes.remove(captured_piece_data)

        # Switch turn
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

        capturing_player = move['piece'].player

        # Add captured pieces back to taken arrays
        for row, col, captured_piece in move['captured']:
            captured_piece_data = 1 if captured_piece.king else 0
            if capturing_player == 'RED':
                self.red_takes.append(captured_piece_data)
                self.inverted_bubble_sort(self.red_takes)
            elif capturing_player == 'WHITE':
                self.white_takes.append(captured_piece_data)
                self.inverted_bubble_sort(self.white_takes)

        # Switch turn
        self.switch_turn()
        print("Move redone.")

    def switch_turn(self):
        """Switches the turn to the other player."""
        self.turn = 'WHITE' if self.turn == 'RED' else 'RED'
        print(f"It is now {self.turn}'s turn.")

    def select(self, pos):
        """Handles piece selection and movement based on user input."""
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
        """Checks if any button in the lower section was clicked."""
        for button in self.lower_section.buttons:
            if button.b_clicked(pos):
                return button
        return None

    def draw_taken_pieces(self, window):
        """Draws the taken pieces on the left and right margins of the board."""
        # Constants for drawing
        piece_size = CELL_SIZE // 3  # Smaller size for taken pieces
        spacing = 10
        y_offset = 10  # Start from top

        # Draw red_takes (white pieces captured by red player) on the right side
        x_offset_red = MARGIN + BOARD_WIDTH + (MARGIN - piece_size) // 2

        for idx, data in enumerate(self.red_takes):
            temp_piece = Piece(0, 0, WHITE)
            temp_piece.king = bool(data)
            temp_piece.x = x_offset_red + piece_size // 2
            temp_piece.y = idx * (piece_size + spacing) + y_offset + piece_size // 2
            temp_piece.radius = piece_size // 2 - 2
            temp_piece.draw(window)

        # Draw white_takes (red pieces captured by white player) on the left side
        x_offset_white = (MARGIN - piece_size) // 2

        for idx, data in enumerate(self.white_takes):
            temp_piece = Piece(0, 0, RED)
            temp_piece.king = bool(data)
            temp_piece.x = x_offset_white + piece_size // 2
            temp_piece.y = idx * (piece_size + spacing) + y_offset + piece_size // 2
            temp_piece.radius = piece_size // 2 - 2
            temp_piece.draw(window)

    def draw(self, window):
        """Draws the entire game state to the window."""
        self.board.draw(window)
        if self.board.selected_piece:
            moves = self.board.get_valid_moves(self.board.selected_piece)
            self.board.highlight_moves(window, moves)
        self.lower_section.draw()
        self.draw_taken_pieces(window)
