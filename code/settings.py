import pygame, platform, ctypes, math
from random import randint, shuffle
from tkinter import Tk
if platform.system() == 'Windows':
    from ctypes import wintypes

class Settings:
    """A class to store all settings for MI x MI."""

    def __init__(self):
        """Initialize the game's default settings."""

        # Screen settings
        self.screen_size = (864,900)
        self.screen_title = "MI x MI"
        self.screen_fps = 90

        # Bubble settings
        self.bubble_size = (36, 36)
        self.bubble_speed = 24
        self.bubble_max_color = 3
        self.bubble_colors = ["red", "yellow", "green", "blue",
                              "pink", "cyan", "orange", "clear"]
        self.bubble_original_colors = self.bubble_colors.copy()
        self.bubble_saved = self.get_random_color()

        # Game area settings
        self.game_area_position = (36, 108)
        self.game_area_size = None
        self.game_area_grid_max = 0

        # Helpers
        self.help_resizing = True

    def adjust_position(self, position):
        """Return the position depending on the screen size."""

        if self.screen_size == (432,450):
            x = position[0] // 2
            y = position[1] // 2
        else:
            x = position[0] * 2
            y = position[1] * 2

        return (x, y)

    def switch_screen_size(self):
        "Change current screen size to the next one from possible sizes."

        if self.screen_size == (432, 450):
            self.screen_size = (864, 900)
            self.bubble_size = (36, 36)
            self.bubble_speed = 24
        else:
            self.screen_size = (432, 450)
            self.bubble_size = (18, 18)
            self.bubble_speed = 12

    def refresh_bubble_saved(self):
        """Refresh the bubble saved color."""

        self.bubble_saved = self.get_random_color()

    def get_random_color(self):
        """Return a random color for the bubbles."""

        if self.bubble_max_color > 0:
            return self.bubble_colors[randint(0, self.bubble_max_color - 1)]

    def get_image(self, file_name):
        """Return the image path depending on the screen size."""

        if self.screen_size == (432,450):
            return f"../images/1x/{file_name}"
        else: return f"../images/2x/{file_name}"

    def set_game_area_grid_max(self, max_number):
        """Set the max number of bubbles in the game area."""

        self.game_area_grid_max = max_number

    def set_max_color(self, max_color):
        """Set the max number of colors for the bubbles."""

        self.bubble_max_color = max_color

    def set_bubble_colors(self, list_of_colors):
        """Set the bubble colors to the given list."""

        self.bubble_colors = list_of_colors

    def shuffle_bubble_colors(self):
        """Randomize the order of the bubble colors."""
    
        shuffle(self.bubble_colors)

class Cursor:
    """Class to manage the cursor."""

    def __init__(self, mixmi):
        """Initialize the cursor and its attributes."""

        self.settings = mixmi.settings
        self.image = pygame.image.load(
            self.settings.get_image('cursor.png')).convert_alpha()
        self.size = (48,48)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.image, (0,0))
        self.cursor = pygame.cursors.Cursor((0,0), self.surface)
        pygame.mouse.set_cursor(self.cursor)

    def resize(self):
        """Set the correct position after resizing the screen."""

        self.size = self.settings.adjust_position(self.size)
        self.image = pygame.image.load(
            self.settings.get_image('cursor.png')).convert_alpha()
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.image, (0,0))
        self.cursor = pygame.cursors.Cursor((0,0), self.surface)
        pygame.mouse.set_cursor(self.cursor)

def get_window_pos():
    """Return the window position."""

    if platform.system() == 'Windows':
        hwnd = pygame.display.get_wm_info()['window']
        rect = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return rect.left, rect.top
    else:
        root = Tk()
        root.withdraw()
        x = root.winfo_x()
        y = root.winfo_y()
        root.destroy()
        return x, y

def set_window_pos(x, y):
    """Set the window position."""

    if platform.system() == 'Windows':
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, None, x, y, 0, 0, 0x0001)
    else:
        root = Tk()
        root.withdraw()
        root.geometry(f'+{x}+{y}')
        root.update_idletasks()
        root.destroy()  
    
def calculate_distance(pos1, pos2):
    """Return the distance between two points."""

    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

