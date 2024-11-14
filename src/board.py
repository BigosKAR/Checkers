import pygame
from constants import *
from piece import Piece
from movement_tree import *


class Board():
    def __init__(self, window):
        self.window = window
        self.board = []
        self.pieces = {'RED': 12, 'WHITE': 12}
        self.kings = {'RED': 0, 'WHITE': 0}
        self.selected_piece = None
        self.add_pieces()

    def draw_board(self, window) -> None:
        for row in range(ROWS):
            for white in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, LIGHT_YELLOW, (row * CELL_SIZE, white * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for black in range(row % 2 - 1, ROWS, 2):
                pygame.draw.rect(window, GREEN, (row * CELL_SIZE, black * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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

    # In board.py
    def move(self, new_row, new_col):
        if self.selected_piece.row == new_row and self.selected_piece.column == new_col:
            self.selected_piece = None
            return
        
        def get_index(array: list, coords: tuple):
            for i in range(len(array)):
                if array[i] == coords:
                    return i
            return None
        print(f"Attempting to move to ({new_row}, {new_col})")

        root = self.generate_valid_moves()
        moves, jumped = self.get_valid_moves(root)
        print(
            f"Valid moves for {self.selected_piece.player} piece at ({self.selected_piece.row}, {self.selected_piece.column}): {moves[1:]}")

        
        if (new_row, new_col) not in moves:
            print("Invalid move.")
            self.selected_piece = None
            return False

        # Proceed with the move since it's valid
        if (new_row == 7 and self.selected_piece.player == 'WHITE') or \
                (new_row == 0 and self.selected_piece.player == 'RED'):
            self.selected_piece.king_promotion()

        i = get_index(moves, (new_row, new_col))

        for jump in jumped[i]:
            self.delete_piece(self.board[jump[0]][jump[1]])

        # Swap pieces on the board
        self.board[self.selected_piece.row][self.selected_piece.column], self.board[new_row][new_col] = \
            self.board[new_row][new_col], self.board[self.selected_piece.row][self.selected_piece.column]
        self.selected_piece.update_position(new_row, new_col)
        return True

    def delete_piece(self, piece):
        self.board[piece.row][piece.column] = 0

    # In board.py
    # def check_game_over(self):
    #     red_pieces, white_pieces = 0, 0
    #     red_moves, white_moves = 0, 0

    #     for row in range(ROWS):
    #         for col in range(COLUMNS):
    #             piece = self.board[row][col]
    #             if piece != 0:
    #                 moves = self.get_valid_moves(piece)
    #                 if piece.player == 'RED':
    #                     red_pieces += 1
    #                     red_moves += len(moves)
    #                 elif piece.player == 'WHITE':
    #                     white_pieces += 1
    #                     white_moves += len(moves)

    #     if red_pieces == 0 or red_moves == 0:
    #         return "WHITE wins"
    #     if white_pieces == 0 or white_moves == 0:
    #         return "RED wins"
    #     if red_pieces == 1 and white_pieces == 1 and red_moves == 0 and white_moves == 0:
    #         return "Tie"

    #     return None

    # def get_valid_moves(self, piece):
    #     moves = {}
    #     directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    #     if not piece.king:
    #         # Only allow forward directions for non-king pieces
    #         directions = [d for d in directions if d[0] == piece.direction]

    #     for dx, dy in directions:
    #         self.dfs(piece, piece.row, piece.column, dx, dy, moves, [])

    #     print(f"Valid moves for {piece.player} piece at ({piece.row}, {piece.column}): {moves}")
    #     return moves

    def generate_valid_moves(self):
        move_tree_root = TreeNode(coords=(self.selected_piece.row, self.selected_piece.column))
        possible_directions = [d for d in ALL_DIRECTIONS if d[0] == self.selected_piece.direction]
        def add_moves_to_tree(node: TreeNode, row, col, jumped):
            captured_a_piece = False
            for dx, dy in possible_directions:
                new_row, new_col = row + dx, col + dy
                if not (0 <= new_row < ROWS and 0 <= new_col < COLUMNS):
                        continue
                target = self.board[new_row][new_col]

                if target != 0 and target.color != self.selected_piece.color:
                    jump_row, jump_col = new_row + dx, new_col + dy
                    if 0 <= jump_row < ROWS and 0 <= jump_col < COLUMNS and self.board[jump_row][jump_col] == 0:
                        updated_jump = node.jumped + [(new_row, new_col)]
                        captured_a_piece = True
                        add_node(node, jump_row, jump_col, dx, dy, updated_jump)
                elif target == 0 and not jumped:
                    if captured_a_piece is False:
                        if dy == 1:
                            node.insert_right(coords=(new_row, new_col), jumped=jumped)
                        else:
                            node.insert_left(coords=(new_row, new_col), jumped=jumped)
                    
        def add_node(node, row, column, dx, dy, jumped):
            if dy == 1:    
                node.insert_right(coords=(row, column), jumped=jumped)
                add_moves_to_tree(node.right, row, column, jumped)
            else:
                node.insert_left(coords=(row, column), jumped=jumped)
                add_moves_to_tree(node.left, row, column, jumped)   
        
        add_moves_to_tree(move_tree_root, self.selected_piece.row, self.selected_piece.column, [])
        return move_tree_root
                       
    def get_valid_moves(self, root):
        moves, jumped = fetch_moves_from_tree(root)
        return moves, jumped

    def highlight_moves(self):
        root = self.generate_valid_moves()
        moves, jumped = self.get_valid_moves(root)
        for move in moves[1:]:
            x = move[1] * CELL_SIZE + CELL_SIZE // 2
            y = move[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.window, RED, (x, y), 15)

