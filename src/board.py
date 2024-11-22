import pygame
from constants import *
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.pieces = {'RED': 12, 'WHITE': 12}
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

        # Proceed with the move since it's valid
        # Remove captured pieces
        captured_pieces = []
        for jump in move_details:
            captured_piece = self.board[jump[0]][jump[1]]
            captured_pieces.append((jump[0], jump[1], captured_piece))
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

        for dx, dy in directions:
            self._traverse(piece, piece.row, piece.column, dx, dy, moves, [], piece.king)

        return moves

    def _traverse(self, piece, row, col, dx, dy, moves, skipped, is_king):
        new_row, new_col = row + dx, col + dy
        if not (0 <= new_row < ROWS and 0 <= new_col < COLUMNS):
            return  # Out of bounds

        current = self.board[new_row][new_col]
        if current == 0:
            if skipped:
                # Must continue jumping if possible
                moves[(new_row, new_col)] = skipped
            else:
                moves[(new_row, new_col)] = skipped
            if not is_king:
                return
        elif current.player != piece.player:
            next_row, next_col = new_row + dx, new_col + dy
            if 0 <= next_row < ROWS and 0 <= next_col < COLUMNS:
                next_square = self.board[next_row][next_col]
                if next_square == 0:
                    new_skipped = skipped + [(new_row, new_col)]
                    self._traverse(piece, next_row, next_col, dx, dy, moves, new_skipped, is_king)
        else:
            return  # Blocked by own piece

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
