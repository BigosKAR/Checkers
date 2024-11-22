import pygame
from constants import *


# Class used for buttons in the lower section
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Function for drawing the buttons
    def draw(self, win) -> None:
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('arial', 20)
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            win.blit(text_surface, text_rect)

    def b_clicked(self, pos):
        mouse_x, mouse_y = pos
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True
        return False


class LowerSection:
    def __init__(self, window, color):
        self.window = window
        self.color = color
        self.buttons = []
        self.button_color = DIM_GRAY
        self.create_buttons()

    # Create the buttons
    def create_buttons(self):
        button_names = ['QUIT', 'RESTART', 'UNDO', 'REDO']
        button_width = 150
        button_spacing = (WIDTH - (len(button_names) * button_width)) / (len(button_names) + 1)
        y_position = HEIGHT - BUTTON_HUD_HEIGHT + 25

        x_position = button_spacing
        for name in button_names:
            button = Button(self.button_color, x_position, y_position, button_width, 50, text=name)
            self.buttons.append(button)
            x_position += button_width + button_spacing

    # Draws the lower section with buttons
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.color, (0, HEIGHT - BUTTON_HUD_HEIGHT, WIDTH, BUTTON_HUD_HEIGHT))
        for button in self.buttons:
            button.draw(self.window)
