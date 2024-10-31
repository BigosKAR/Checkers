import pygame
from board import Board
from constants import *
from lower_section import LowerSection, Button

# creating the window of the application
window = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    # Initializing parts of the game (board and the section below it)
    board = Board()
    lower_section = LowerSection(window, SILVER)
    lower_section.initialize_lower_section(DIM_GRAY)

    clock = pygame.time.Clock()
    active = True
    while active:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        
        board.draw(window)  # drawing the board
        pygame.display.update() # updating the display

    pygame.quit()
    

if __name__ == "__main__":
    main()