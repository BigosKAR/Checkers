# constants.py

# Constants for the board
ROWS = 8
COLUMNS = 8
CELL_SIZE = 100  # Size of each cell in pixels

BOARD_WIDTH = CELL_SIZE * COLUMNS  # Width of the board area (800 pixels)
MARGIN = 150  # Space on each side for displaying taken pieces

WIDTH = BOARD_WIDTH + 2 * MARGIN  # Total window width (1100 pixels)
HEIGHT = 1000  # Total window height

# Colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
DIM_GRAY = (105, 105, 105)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)

# Constants for the lower section (buttons and HUD)
BUTTON_HUD_HEIGHT = 200  # Height of the lower HUD area

# Other constants
FPS = 60  # Frames per second
