import pygame
from constants import *
from piece import Piece
from movement_tree import *


class Board():
    def __init__(self, window):
        self.window = window
        self.board = []

        self.pieces = {'RED': 12, 'WHITE': 12}
        self.red_pieces_taken = []
        self.white_pieces_taken = []
        self.selected_piece = None

        self.add_pieces()

    def mergesort_pieces_taken(self, pieces_taken: list) -> None:
        """
        Merge sort algorithms used to sort array containting pieces and kings taken by any of the players.
        Pieces are represented by 0 and kings by 1. This quick sort algorithm is going to sort the array in descending order.
        Function used for implementing the visual representation of the pieces taken by the players, 
        where kings appear on the left side and pieces on the right side.

        Runtime Complexity: 
        - Average Case: O(nlogn)
        - Worst Case: O(nlogn)

        """
        def combine(left: list, right: list) -> list:
            result = [0] * (len(left) + len(right))
            left_idx = right_idx = result_idx = 0
            while left_idx < len(left) and right_idx < len(right):
                if left[left_idx] > right[right_idx]:
                    result[result_idx] = left[left_idx]
                    left_idx += 1
                else:
                    result[result_idx] = right[right_idx]
                    right_idx += 1
                result_idx += 1
            while left_idx < len(left):
                result[result_idx] = left[left_idx]
                left_idx += 1
                result_idx += 1
            while right_idx < len(right):
                result[result_idx] = right[right_idx]
                right_idx += 1
                result_idx += 1
            return result
        
        def mergesort(arr: list) -> list:
            if not arr or len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = mergesort(arr[:mid])
            right = mergesort(arr[mid:])
            return combine(left, right)
        return mergesort(pieces_taken)

    def draw_board(self, window) -> None:
        """
        Function for drawing the checkers board
        Runtime Complexity:
        - Average Case = Worst Case: O(n^2) (columns = rows = 8)
        """
        for row in range(ROWS):
            for white in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, WHITE, (row * CELL_SIZE, white * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for black in range(row % 2 - 1, ROWS, 2):
                pygame.draw.rect(window, BLACK, (row * CELL_SIZE, black * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def add_pieces(self) -> None:
        """
        Function for initializing pieces on the logical representation of the board
        Runtime Complexity:
        - Average Case = Worst Case: O(n^2) (columns = rows = 8)
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE    ))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window, lower_section) -> None:
        """
        Function for visually representing pieces on the board. Also initializes the lower section of the game.
        Runtime Complexity:
        - Average Case = Worst Case: O(n^2) (columns = rows = 8)
        """
        self.draw_board(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)
        lower_section.initialize_lower_section(DIM_GRAY)
        lower_section.draw_taken_pieces(self.red_pieces_taken, RED, 25, HEIGHT - 50)
        lower_section.draw_taken_pieces(self.white_pieces_taken, WHITE, WIDTH - 290, HEIGHT - 50)

    # In board.py
    def move(self, new_row, new_col):
        """
        Function made for moving the selected piece to the new position.
        It is going to check if the move is valid and then proceed with the move.
        If the move is invalid, it will reset the moves and jumped arrays for the selected piece.
        Runtime Complexity:
        - Average Case = Worst Case: O(n)
        """
        if self.selected_piece.row == new_row and self.selected_piece.column == new_col:
            self.selected_piece = None
            return

        def popup(window, first_index, second_index):
            """
            Function made solely to handle one of the edge cases where there are two paths to one place.
            After the player chooses this specific place he will be displayed a popup window.
            The player must choose which direction he wants to go.

            Runtime Complexity:
            - Average Case = Worst Case: O(1) # Depends when player clicks on the button
            """

            popup_width, popup_height = 450, 150
            popup_x = (WIDTH - popup_width) // 2
            popup_y = (HEIGHT - popup_height) // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            button_width, button_height = 150, 50
            left_rect = pygame.Rect(popup_x + 50, popup_y + 75, button_width, button_height)
            right_rect = pygame.Rect(popup_x + 250, popup_y + 75, button_width, button_height)

            font = pygame.font.SysFont('arial', 24)
            message_surface = font.render('Which way? (not relative to the piece!)', True, (0, 0, 0))
            left_surface = font.render('LEFT PATH', True, (0, 0, 0))
            right_surface = font.render('RIGHT PATH', True, (0, 0, 0))

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
                        
                pygame.draw.rect(window, (200, 200, 200), popup_rect)
                window.blit(message_surface, (popup_x + 50, popup_y + 30))
                pygame.draw.rect(window, (0, 255, 0), left_rect)
                pygame.draw.rect(window, (255, 0, 0), right_rect)
                window.blit(left_surface, (left_rect.x + 10, left_rect.y + 10))
                window.blit(right_surface, (right_rect.x + 10, right_rect.y + 10))

                pygame.display.update()

        def get_index(array: list, coords: tuple):
            """
            Function used to get the index of the coordinates in the array
            Runtime Complexity:
            - Average Case = Worst Case: O(n)
            """
            for i in range(len(array)):
                if array[i] == coords:
                    return i
            return None
        
        # Helper function (only call when you have the result of get_index) Checks for a second possible way to get to that location
        def double_check_index(array, coords, i):
            """
            Function used to check if there is a second path to the same location
            Runtime Complexity:
            - Average Case = Worst Case: O(n)
            """
            if i is None:
                return None
            for j in range(i+1, len(array)):
                if array[j] == coords:
                    return j
            return None

        # print(f"Attempting to move to ({new_row}, {new_col})")
        # print(
        #     f"Valid moves for {self.selected_piece.player} piece at ({self.selected_piece.row}, {self.selected_piece.column}): {self.selected_piece.moves[1:]}")

        
        if (new_row, new_col) not in self.selected_piece.moves:
            print("Invalid move.")
            self.reset_move_details()
            self.selected_piece = None
            return False

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
        """
        Function used to delete a piece from the board by setting it to 0
        Runtime Complexity:
        - Average Case = Worst Case: O(nlogn) (because of mergesort_pieces_taken)
        """
        if isinstance(piece, Piece):
            if piece.color == RED:
                if piece.king:
                    self.red_pieces_taken.append(1)
                else:
                    self.red_pieces_taken.append(0)
                self.red_pieces_taken = self.mergesort_pieces_taken(self.red_pieces_taken) #change params
            else:
                if piece.king:
                    self.white_pieces_taken.append(1)
                else:
                    self.white_pieces_taken.append(0)
                self.white_pieces_taken = self.mergesort_pieces_taken(self.white_pieces_taken) # change params
            self.pieces[piece.player] -= 1
            self.board[piece.row][piece.column] = 0

    def reset_move_details(self):
        """
        Everytime you are either after a move or you selected another piece
        you need to reset the moves and jumped array for that specific piece so that
        it will not be stored and used for future moves (future moves will probably be different)

        Runtime Complexity:
        - Average Case = Worst Case: O(1)
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

        Runtime Complexity:
        - Average Case = Worst Case: O(possible_directions^depth)
        """
        possible_directions = ALL_DIRECTIONS if self.selected_piece.king else [d for d in ALL_DIRECTIONS if d[0] == self.selected_piece.direction]
        move_tree_root = TreeNode(coords=(self.selected_piece.row, self.selected_piece.column))
        
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
        Runtime Complexity:
        - Average Case = Worst Case: O(n) n-> number of nodes in the tree
        """
        if self.selected_piece.king == True:
            moves, jumped = fetch_moves_from_king_tree(root)
        else:
            moves, jumped = fetch_moves_from_tree(root)
        return moves, jumped

    def highlight_moves(self):
        """
        This function draws small circles in the possible positions of the selected piece.
        It goes from [1:] because the 0 position is the current position of the selected_piece
        Runtime Complexity:
        - Average Case = Worst Case: O(n) n-> number of possible moves
        """
        for move in self.selected_piece.moves[1:]:
            x = move[1] * CELL_SIZE + CELL_SIZE // 2
            y = move[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.window, RED, (x, y), 15)

    def store_valid_moves(self):
        """
        Helper function calls a function to create a create with the moves and jumped pieces
        Then it stores the information of those trees in the attributes of the selected_piece
        Runtime Complexity:
        - Average Case = Worst Case: O(depth*possible_directions^depth) (because of generate_valid_moves and generate_valid_king_moves)
        """
        if self.selected_piece.king == True:
            root = self.generate_valid_king_moves()
        else:
            root = self.generate_valid_moves()
        self.selected_piece.moves, self.selected_piece.jumped = self.get_valid_moves(root)

    def update_piece_count(self, white_pieces, red_pieces):
        """
        Function for updating the number of pieces each player has.
        Runtime Complexity:
        - Average Case = Worst Case: O(1)
        """
        self.pieces['WHITE'] = white_pieces
        self.pieces['RED'] = red_pieces

    def check_game_over(self):
        """
        Function for checking if the game is over.
        Runtime Complexity:
        - Average Case = Worst Case: O(1)
        """
        def win_popup(window, winner: str):
            """
            Inner function for creating a win message
            """
            
            popup_width, popup_height = 450, 150
            popup_x = (WIDTH - popup_width) // 2
            popup_y = (HEIGHT - popup_height) // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            button_width, button_height = 150, 50
            win_notification = pygame.Rect(popup_x + 150, popup_y + 50, button_width, button_height)

            font = pygame.font.SysFont('arial', 15)
            message_surface = font.render(f'{winner.upper()} won!', True, (0, 0, 0))
            restart_surface = font.render(f'Restart', True, (0, 0, 0))
        
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if win_notification.collidepoint(event.pos):
                            return True


                # Draw the pop up window
                pygame.draw.rect(window, (200, 200, 200), popup_rect)
                window.blit(message_surface, (popup_x + 50, popup_y + 30))
                pygame.draw.rect(window, (0, 255, 0), win_notification)
                window.blit(restart_surface, (win_notification.x + 10, win_notification.y + 10))

                pygame.display.update()

        if self.pieces['WHITE'] <= 0:
            return win_popup(self.window, 'RED') # 0 -> White wins
        elif self.pieces['RED'] <= 0:
            return win_popup(self.window, 'WHITE')
        return False

    def generate_valid_king_moves(self):
            """
            Firstly, we create a root of the tree that will contain every possible move and capture. It is going to be the coordinates of the selected piece.
            We are defining two functions in this function:
            - add_moves_to_tree: it is going to populate the tree with possible selected piece positions. It is also going to store the position of captured pieces
            - add_node: it adds a singular node to the tree but then also checks for every possibility in the next branches. So it is a recursion with two functions
            This function is different because every time it needs to look into 4 (first move) or 3 (every other move) directions 
            unlike the previous generate_valid_moves function which had 2 directions maximum.

            Runtime Complexity:
            - Average Case = Worst Case: O(possible_directions^depth)
            """
            king_root = KingTreeNode(coords=(self.selected_piece.row, self.selected_piece.column))
            max_depth = 12
            def add_moves_to_tree(node: KingTreeNode, row, col, jumped, capturing, directions):
                for dx, dy in directions:
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
                    if len(jumped) >= max_depth:
                        continue
                    if target != 0 and target.color != self.selected_piece.color:
                        jump_row, jump_col = new_row + dx, new_col + dy
                        if 0 <= jump_row < ROWS and 0 <= jump_col < COLUMNS and self.board[jump_row][jump_col] == 0:
                            updated_jump = node.jumped + [(new_row, new_col)]
                            add_node(node, jump_row, jump_col, dx, dy, updated_jump, capture=True)
                    elif target == 0 and not jumped and not capturing:
                        add_node(node, new_row, new_col, dx, dy, [], capture=False)
                        

            def add_node(king_node, row, column, dx, dy, jumped, capture):
                updated_directions = ALL_DIRECTIONS.copy()
                current_direction = (dx, dy)
                if current_direction == (-1, 1):
                    king_node.insert_right_up(coords=(row, column), jumped=jumped)
                    if capture:
                        updated_directions.remove((1, -1))
                        add_moves_to_tree(king_node.right_up, row, column, jumped, capture, directions=updated_directions)
                elif current_direction == (1, 1):
                    king_node.insert_right_down(coords=(row, column), jumped=jumped)
                    if capture:
                        updated_directions.remove((-1, -1))
                        add_moves_to_tree(king_node.right_down, row, column, jumped, capture, directions=updated_directions)
                elif current_direction == (-1, -1):
                    king_node.insert_left_up(coords=(row, column), jumped=jumped)
                    if capture:
                        updated_directions.remove((1, 1))
                        add_moves_to_tree(king_node.left_up, row, column, jumped, capture, directions=updated_directions)
                else:
                    king_node.insert_left_down(coords=(row, column), jumped=jumped)
                    if capture:
                        updated_directions.remove((-1, 1))
                        add_moves_to_tree(king_node.left_down, row, column, jumped, capture, directions=updated_directions)

                
            # Executing everything and returning the root of the created tree        
            add_moves_to_tree(king_root, self.selected_piece.row, self.selected_piece.column, [], False, ALL_DIRECTIONS)
            return king_root





