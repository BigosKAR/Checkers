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


class LowerSection():
    def __init__(self, window, color):
        self.window = window
        self.color = color
        self.buttons = []


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
        
