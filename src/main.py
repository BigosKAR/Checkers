import pygame
from board import Board
from constants import *
from lower_section import LowerSection


window = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    board = Board()
    lower_section = LowerSection(window, LIGHT_BLUE)
    lower_section.initialize_lower_section()
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        
        board.draw(window)
        pygame.display.update()

    pygame.quit()
    

if __name__ == "__main__":
    main()