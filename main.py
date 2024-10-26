import pygame
from board import WIDTH, HEIGHT, Board

window = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    board = Board()
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