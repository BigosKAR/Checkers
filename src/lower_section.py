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
        self.turn_button = Button(WHITE, 350, HEIGHT-BUTTON_HUD_HEIGHT+ 150, 100, 50, text="WHITE - turn")
        self.initialize_lower_section(DIM_GRAY)


    # Draws the lower section with buttons
    def initialize_lower_section(self, button_color) -> None:
        pygame.draw.rect(self.window, self.color, (0, HEIGHT-BUTTON_HUD_HEIGHT, WIDTH, BUTTON_HUD_HEIGHT))
        button_names = ['QUIT', 'RESTART', 'UNDO', 'REDO']  # Add REDO button
        button_width = 150
        button_spacing = (WIDTH - (len(button_names) * button_width)) / (len(button_names) + 1)
        y_position = HEIGHT - BUTTON_HUD_HEIGHT + 75

        # Dynamically space buttons
        x_position = button_spacing
        for name in button_names:
            button = Button(button_color, x_position, y_position, button_width, 50, text=name)
            self.buttons.append(button)
            button.draw(self.window)
            x_position += button_width + button_spacing  # Space out buttons evenly
        
        self.turn_button.draw(self.window)

    def change_turn_text(self, turn_var):
        if turn_var is True:
            self.turn_button.text = "WHITE - turn"
            self.turn_button.color = WHITE
            self.turn_button.draw(self.window)
        else:
            self.turn_button.text = "RED - turn"
            self.turn_button.color = RED
            self.turn_button.draw(self.window)

