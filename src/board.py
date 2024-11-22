import pygame
from constants import *
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.add_pieces()

    def draw_board(self, window) -> None:
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def add_pieces(self) -> None:
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window) -> None:
        self.draw_board(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)

    def move(self, piece, new_row, new_col):
        valid_moves = self.get_valid_moves(piece)
        move_details = valid_moves.get((new_row, new_col))
        if move_details is None:
            print("Invalid move.")
            self.selected_piece = None
            return False

        old_row, old_col = piece.row, piece.column

        # Proceed with the move
        # Remove captured pieces
        captured_pieces = []
        for capture in move_details['captures']:
            captured_piece = self.board[capture[0]][capture[1]]
            captured_pieces.append((capture[0], capture[1], captured_piece))
            self.delete_piece(captured_piece)

        # Move the piece
        self.board[old_row][old_col], self.board[new_row][new_col] = 0, piece
        piece.update_position(new_row, new_col)

        # Check for king promotion
        was_king = piece.king
        if (new_row == 7 and piece.player == 'WHITE') or (new_row == 0 and piece.player == 'RED'):
            piece.king_promotion()

        # Return move details
        move_data = {
            'piece': piece,
            'old_pos': (old_row, old_col),
            'new_pos': (new_row, new_col),
            'captured': captured_pieces,
            'was_king': was_king,
            'became_king': piece.king
        }

        return move_data

    def delete_piece(self, piece):
        self.board[piece.row][piece.column] = 0

    def undo_move(self, move_data):
        piece = move_data['piece']
        old_row, old_col = move_data['old_pos']
        new_row, new_col = move_data['new_pos']

        # Move piece back to old position
        self.board[new_row][new_col] = 0
        self.board[old_row][old_col] = piece
        piece.update_position(old_row, old_col)

        # Restore captured pieces
        for row, col, captured_piece in move_data['captured']:
            self.board[row][col] = captured_piece

        # Undo king promotion if it occurred
        if move_data['became_king'] and not move_data['was_king']:
            piece.king = False

    def redo_move(self, move_data):
        piece = move_data['piece']
        old_row, old_col = move_data['old_pos']
        new_row, new_col = move_data['new_pos']

        # Remove piece from old position
        self.board[old_row][old_col] = 0
        self.board[new_row][new_col] = piece
        piece.update_position(new_row, new_col)

        # Remove captured pieces
        for row, col, captured_piece in move_data['captured']:
            self.board[row][col] = 0

        # Redo king promotion if it occurred
        if move_data['became_king'] and not move_data['was_king']:
            piece.king = True

    def check_game_over(self):
        red_pieces, white_pieces = 0, 0
        red_moves, white_moves = 0, 0

        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    moves = self.get_valid_moves(piece)
                    if piece.player == 'RED':
                        red_pieces += 1
                        red_moves += len(moves)
                    elif piece.player == 'WHITE':
                        white_pieces += 1
                        white_moves += len(moves)

        if red_pieces == 0 or red_moves == 0:
            return "WHITE wins"
        if white_pieces == 0 or white_moves == 0:
            return "RED wins"
        if red_pieces == 1 and white_pieces == 1 and red_moves == 0 and white_moves == 0:
            return "Tie"

        return None

    def get_valid_moves(self, piece):
        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if not piece.king:
            # Only allow forward directions for non-king pieces
            directions = [d for d in directions if d[0] == piece.direction]

        # Get capturing moves
        capturing_moves = {}
        self._get_captures(piece, piece.row, piece.column, [], directions, capturing_moves)

        # If capturing moves are available, include both capturing and non-capturing moves
        for dx, dy in directions:
            new_row = piece.row + dx
            new_col = piece.column + dy
            if 0 <= new_row < ROWS and 0 <= new_col < COLUMNS:
                if self.board[new_row][new_col] == 0:
                    # Add normal move if the destination is empty
                    moves[(new_row, new_col)] = {'captures': []}

        # Add capturing moves to the possible moves
        if capturing_moves:
            moves.update(capturing_moves)

        return moves


    def _get_captures(self, piece, row, col, skipped, directions, moves):
        for dx, dy in directions:
            new_row = row + dx
            new_col = col + dy
            jump_row = new_row + dx
            jump_col = new_col + dy
            if 0 <= new_row < ROWS and 0 <= new_col < COLUMNS and 0 <= jump_row < ROWS and 0 <= jump_col < COLUMNS:
                current = self.board[new_row][new_col]
                if current != 0 and current.player != piece.player:
                    if self.board[jump_row][jump_col] == 0:
                        if (jump_row, jump_col) not in moves:
                            new_skipped = skipped + [(new_row, new_col)]
                            # Temporarily move the piece and remove the captured piece
                            original_piece = self.board[jump_row][jump_col]
                            self.board[row][col] = 0
                            self.board[new_row][new_col] = 0
                            self.board[jump_row][jump_col] = piece

                            # Recursive call to continue capturing
                            self._get_captures(piece, jump_row, jump_col, new_skipped, directions, moves)

                            # If no further captures, add the move
                            if not any(jump_row in move and jump_col in move for move in moves):
                                moves[(jump_row, jump_col)] = {'captures': new_skipped}

                            # Restore the board
                            self.board[row][col] = piece
                            self.board[new_row][new_col] = current
                            self.board[jump_row][jump_col] = original_piece

    def highlight_moves(self, window, moves):
        for move in moves.keys():
            row, col = move
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(window, LIGHT_BLUE, (x, y), 15)

    def get_piece_at_position(self, pos):
        row, col = self.coords_to_row_col(pos)
        if row is not None and col is not None:
            return self.board[row][col]
        return None

    def coords_to_row_col(self, pos):
        x, y = pos
        if 0 <= y < (HEIGHT - BUTTON_HUD_HEIGHT) and 0 <= x < WIDTH:
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            return int(row), int(col)
        return None, None
