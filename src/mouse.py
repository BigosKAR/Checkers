import pygame

class Mouse():
    def __init__(self, board):
        self.board = board

    def check_if_piece_clicked(self):
        # TO DO: transform this function into a select_piece function to show the player possible moves
        pos = pygame.mouse.get_pos()
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.clicked(pos)
    