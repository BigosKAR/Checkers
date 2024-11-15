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

        def popup(window, first_index, second_index):
            """
            Function made solely to handle one of the edge cases where there are two paths to one place.
            After the player chooses this specific place he will be displayed a popup window.
            The player must choose which direction he wants to go.
            """

            # Creating the pop up window
            popup_width, popup_height = 450, 150
            popup_x = (WIDTH - popup_width) // 2
            popup_y = (HEIGHT - popup_height) // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            # Creating buttons
            button_width, button_height = 150, 50
            left_rect = pygame.Rect(popup_x + 50, popup_y + 75, button_width, button_height)
            right_rect = pygame.Rect(popup_x + 250, popup_y + 75, button_width, button_height)

            # Creating text for window and buttons
            font = pygame.font.SysFont('arial', 24)
            message_surface = font.render('Which way? (not relative to the piece!)', True, (0, 0, 0))
            left_surface = font.render('LEFT PATH', True, (0, 0, 0))
            right_surface = font.render('RIGHT PATH', True, (0, 0, 0))

            # Running the pop up window and waiting for response
            # Returns different indexes based on the player's choice
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if left_rect.collidepoint(event.pos):
                            return first_index
                        elif right_rect.collidepoint(event.pos):
                            return second_index

                # Draw the pop up window
                pygame.draw.rect(window, (200, 200, 200), popup_rect)
                window.blit(message_surface, (popup_x + 50, popup_y + 30))
                pygame.draw.rect(window, (0, 255, 0), left_rect)
                pygame.draw.rect(window, (255, 0, 0), right_rect)
                window.blit(left_surface, (left_rect.x + 10, left_rect.y + 10))
                window.blit(right_surface, (right_rect.x + 10, right_rect.y + 10))

                pygame.display.update()

        def get_index(array: list, coords: tuple):
            for i in range(len(array)):
                if array[i] == coords:
                    return i
            return None
        
        # Helper function (only call when you have the result of get_index) Checks for a second possible way to get to that location
        def double_check_index(array, coords, i):
            if i is None:
                return None
            for j in range(i+1, len(array)):
                if array[j] == coords:
                    return j
            return None

        print(f"Attempting to move to ({new_row}, {new_col})")
        print(
            f"Valid moves for {self.selected_piece.player} piece at ({self.selected_piece.row}, {self.selected_piece.column}): {self.selected_piece.moves[1:]}")

        
        if (new_row, new_col) not in self.selected_piece.moves:
            print("Invalid move.")
            self.reset_move_details()
            self.selected_piece = None
            return False

        # Proceed with the move since it's valid
        if (new_row == 7 and self.selected_piece.player == 'WHITE') or \
                (new_row == 0 and self.selected_piece.player == 'RED'):
            self.selected_piece.king_promotion()

        # j is calculated to deal with an edge case
        i = get_index(self.selected_piece.moves, (new_row, new_col))
        j = double_check_index(self.selected_piece.moves, (new_row, new_col), i)

        # If the edge case is present, then user can choose the direction
        if j is not None:
            index = popup(window=self.window, first_index=i, second_index=j)
        else:
            index = i
        for jump in self.selected_piece.jumped[index]:
            self.delete_piece(self.board[jump[0]][jump[1]])

        # Swap pieces on the board
        self.board[self.selected_piece.row][self.selected_piece.column], self.board[new_row][new_col] = \
            self.board[new_row][new_col], self.board[self.selected_piece.row][self.selected_piece.column]
        self.selected_piece.update_position(new_row, new_col)
        return True

    def delete_piece(self, piece):
        self.board[piece.row][piece.column] = 0

    def reset_move_details(self):
        """
        Everytime you are either after a move or you selected another piece
        you need to reset the moves and jumped array for that specific piece so that
        it will not be stored and used for future moves (future moves will probably be different)
        """
        if self.selected_piece.moves:
            self.selected_piece.moves = None
        if self.selected_piece.jumped:
            self.selected_piece.jumped = None
    
    def generate_valid_moves(self):
        """
        Firstly, we create a root of the tree that will contain every possible move and capture. It is going to be the coordinates of the selected piece.
        We are defining two functions in this function:
        - add_moves_to_tree: it is going to populate the tree with possible selected piece positions. It is also going to store the position of captured pieces
        - add_node: it adds a singular node to the tree but then also checks for every possibility in the next branches. So it is a recursion with two functions
        """
        move_tree_root = TreeNode(coords=(self.selected_piece.row, self.selected_piece.column))
        possible_directions = [d for d in ALL_DIRECTIONS if d[0] == self.selected_piece.direction]

        def add_moves_to_tree(node: TreeNode, row, col, jumped, capturing):
            for dx, dy in possible_directions:
                new_row, new_col = row + dx, col + dy
                if not (0 <= new_row < ROWS and 0 <= new_col < COLUMNS):
                    continue
                """
                Target symbolizes the tile where the new row and new column point to.
                If it is a piece (different from 0), then it has to calculate the new coordinates because we need to jump over a piece.
                To the current node's jumped list we are adding the coordinates of the piece we are jumping over.
                Then, with add_node we are looking for any additional possible jumps from the new row and column.
                In the other case we are looking at an empty tile so depending on the direction we add a node.
                """
                target = self.board[new_row][new_col]

                if target != 0 and target.color != self.selected_piece.color:
                    jump_row, jump_col = new_row + dx, new_col + dy
                    if 0 <= jump_row < ROWS and 0 <= jump_col < COLUMNS and self.board[jump_row][jump_col] == 0:
                        updated_jump = node.jumped + [(new_row, new_col)]
                        captured_a_piece = True
                        add_node(node, jump_row, jump_col, dx, dy, updated_jump)
                elif target == 0 and not jumped and not capturing:
                    if dy == 1:
                        node.insert_right(coords=(new_row, new_col), jumped=jumped)
                    else:
                        node.insert_left(coords=(new_row, new_col), jumped=jumped)

        def add_node(node, row, column, dx, dy, jumped):
            """
            Attaching a new node to the parent with respect to the direction on the checkers board.
            Moves getting closer to the right side of the board are going to add a .right branch.
            Moves getting closer to the left side of the board are going to add a .left branch.
            """
            if dy == 1:
                node.insert_right(coords=(row, column), jumped=jumped)
                add_moves_to_tree(node.right, row, column, jumped, True)
            else:
                node.insert_left(coords=(row, column), jumped=jumped)
                add_moves_to_tree(node.left, row, column, jumped, True)

        # Executing everything and returning the root of the created tree
        add_moves_to_tree(move_tree_root, self.selected_piece.row, self.selected_piece.column, [], False)
        return move_tree_root
                       
    def get_valid_moves(self, root):
        """
        Function made for better readability
        Just returns two lists made by fetch_moves_from_tree located in movement_tree.py
        """
        moves, jumped = fetch_moves_from_tree(root)
        return moves, jumped

    def highlight_moves(self):
        """
        This function draws small circles in the possible positions of the selected piece.
        It goes from [1:] because the 0 position is the current position of the selected_piece
        """
        for move in self.selected_piece.moves[1:]:
            x = move[1] * CELL_SIZE + CELL_SIZE // 2
            y = move[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.window, RED, (x, y), 15)

    def store_valid_moves(self):
        """
        Helper function calls a function to create a create with the moves and jumped pieces
        Then it stores the information of those trees in the attributes of the selected_piece
        """
        root = self.generate_valid_moves()
        self.selected_piece.moves, self.selected_piece.jumped = self.get_valid_moves(root)
