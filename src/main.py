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
        game_state = game.board.check_game_over()
        if game_state:
            game = Game(window)
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
                    elif button.text == "UNDO" and game.board.selected_piece is None:
                        game.undo_move()
                    elif button.text == "REDO" and game.board.selected_piece is None:
                        game.redo_move()

        game.board.draw(window)
        if game.board.selected_piece is not None:
            game.board.highlight_moves()
        pygame.display.set_caption(f"WHITE: {game.board.pieces['WHITE']}, RED: {game.board.pieces['RED']}")
        pygame.display.update()  # updating the display

    pygame.quit()


if __name__ == "__main__":
    main()
