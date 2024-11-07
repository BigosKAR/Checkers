import pygame
from constants import *
from game import Game

# creating the window of the application
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

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
                if pos[1] < (HEIGHT - BUTTON_HUD_HEIGHT):
                    game.select(pos)
                else:
                    # Functionality of buttons for the lower section
                    button = game.select_button(pos)
                    if not button:
                        continue
                    if button.text == "QUIT":
                        active = False
                    elif button.text == "RESTART":
                        game = Game(window)
                    elif button.text == "UNDO":
                        # IMPLEMENT UNDO FEATURE HERE
                        pass
        game.board.draw(window)  # drawing the board
        
        pygame.display.update() # updating the display

    pygame.quit()
    

if __name__ == "__main__":
    main()