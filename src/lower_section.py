import pygame
from constants import *

class LowerSection():
    def __init__(self, window, color):
        self.window = window
        self.color = color

    def initialize_lower_section(self):
        pygame.draw.rect(self.window, self.color, (0, HEIGHT-BUTTON_HUD_HEIGHT, WIDTH, BUTTON_HUD_HEIGHT))