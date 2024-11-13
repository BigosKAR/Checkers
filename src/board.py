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
            for white in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, WHITE, (row * CELL_SIZE, white * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for black in range(row % 2 - 1, ROWS, 2):
                pygame.draw.rect(window, BLACK, (row * CELL_SIZE, black * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Functions that adds the pieces to a 2D array
    # Either the object or zeros
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

    # Draws the whole board (first -> the board, then it looks at the 2D array to draw the pieces)
    def draw(self, window) -> None:
        self.draw_board(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)

    # MOVEMENT FUNCTIONS

    def move(self, new_row, new_col):
        # Function for moving pieces and handling king promotion and capture logic.
        if not (0 <= new_row <= 7 and 0 <= new_col <= 7):
            self.selected_piece = None
            return
        if (new_row == 7 and self.selected_piece.color == WHITE) or (new_row == 0 and self.selected_piece.color == RED):
            self.selected_piece.king_promotion()

        move_details = self.get_valid_moves(self.selected_piece).get((new_row, new_col))
        if move_details:
            for jump in move_details:
                self.delete_piece(self.board[jump[0]][jump[1]])

        self.board[self.selected_piece.row][self.selected_piece.column], self.board[new_row][new_col] = \
        self.board[new_row][new_col], self.board[self.selected_piece.row][self.selected_piece.column]
        self.selected_piece.update_position(new_row, new_col)

    def delete_piece(self, piece):
        self.board[piece.row][piece.column] = 0

    def check_game_over(self):
        # Check if a player has no pieces left or no valid moves.
        red_pieces, white_pieces = 0, 0
        red_moves, white_moves = 0, 0

        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    moves = self.get_valid_moves(piece)
                    if piece.color == RED:
                        red_pieces += 1
                        red_moves += len(moves)
                    elif piece.color == WHITE:
                        white_pieces += 1
                        white_moves += len(moves)

        if red_pieces == 0 or red_moves == 0:
            return "WHITE wins"
        if white_pieces == 0 or white_moves == 0:
            return "RED wins"
        if red_pieces == 1 and white_pieces == 1 and red_moves == 0 and white_moves == 0:
            return "Tie"

        return None  # Game continues

    def get_valid_moves(self, piece):
        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if not piece.king:
            # Forward movement restricted for non-kings.
            directions = [d for d in directions if d[0] == piece.direction]

        for dx, dy in directions:
            self.dfs(piece, piece.row, piece.column, dx, dy, moves, [])
        return moves

    def dfs(self, piece, row, col, dx, dy, moves, jumped):
        new_row, new_col = row + dx, col + dy
        if not (0 <= new_row < ROWS and 0 <= new_col < COLUMNS):
            return  # Out of bounds

        target = self.board[new_row][new_col]
        if target == 0:
            # Valid move
            moves[(new_row, new_col)] = jumped
        elif target.color != piece.color and (new_row + dx, new_col + dy) not in jumped:
            # Possible jump move
            jump_row, jump_col = new_row + dx, new_col + dy
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLUMNS and self.board[jump_row][jump_col] == 0:
                self.dfs(piece, jump_row, jump_col, dx, dy, moves, jumped + [(new_row, new_col)])

    def highlight_moves(self, window, moves):
        for move in moves.keys():
            x = move[1] * CELL_SIZE + CELL_SIZE // 2
            y = move[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(window, LIGHT_BLUE, (x, y), 15)
