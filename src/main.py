import pygame
from constants import *
from game import Game

# creating the window of the application
window = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    # Initializing parts of the game (board and the section below it)
    game = Game(window)
    clock = pygame.time.Clock()
    active = True
    while active:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # DOES THIS IF THE PLAYER CLICKS
                # GETS POSITION, CHECKS FOR PIECE SELECTION/MOVE
                pos = pygame.mouse.get_pos()
                game.select(pos)
        game.board.draw(window)  # drawing the board
        
        pygame.display.update() # updating the display

    pygame.quit()
    

if __name__ == "__main__":
    main()