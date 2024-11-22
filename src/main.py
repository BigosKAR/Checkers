import pygame
from constants import *
from game import Game

# Creating the window of the application
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")
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
                # Does this if the player clicks
                pos = pygame.mouse.get_pos()
                if pos[1] < (HEIGHT - BUTTON_HUD_HEIGHT):
                    result = game.select(pos)
                    if result:
                        print(result)
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
                        game.undo_move()
                    elif button.text == "REDO":
                        game.redo_move()

        # Draw everything
        game.draw(window)

        pygame.display.update()  # Updating the display

    pygame.quit()


if __name__ == "__main__":
    main()
