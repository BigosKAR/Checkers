import pygame
from constants import *


# Class used for buttons in the lower section
class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Function for drawing the buttons
    def draw(self,win) -> None:
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        if self.text != '':
            font = pygame.font.SysFont('arial', 20)
            text_surface = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            win.blit(text_surface, text_rect)

    def b_clicked(self, pos):
        mouse_x, mouse_y = pos
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True
        return False


class LowerSection():
    def __init__(self, window, color):
        self.window = window
        self.color = color
        self.buttons = []
        self.initialize_lower_section(DIM_GRAY)


    # Draws the lower section with buttons
    def initialize_lower_section(self, button_color) -> None:
        pygame.draw.rect(self.window, self.color, (0, HEIGHT-BUTTON_HUD_HEIGHT, WIDTH, BUTTON_HUD_HEIGHT))
        button_names = ['QUIT', 'RESTART', 'UNDO']
        start_pos_x = 87.5

        for i in range(len(button_names)):
            button = Button(button_color, start_pos_x, 875, 150, 50, text=button_names[i])
            button.draw(self.window)
            self.buttons.append(button)
            start_pos_x += 237.5 # Specific value to make the buttons placed symmetrically
        

