import pygame, platform, ctypes, math
from random import randint, shuffle
from tkinter import Tk
if platform.system() == 'Windows':
    from ctypes import wintypes

class Settings:
    "Representation of the settings of the game."

    def __init__(self):
        """Initialize the game's settings."""
        
        # Screen setttings
        self.screen_size = (864, 900)
        self.screen_fps = 90

        # Bubble settings
        self.bubble_size = (36, 36)
        self.bubble_speed = 24
        self.saved_color = "red"

        # Game area settings
        self.game_pos = (36, 108)
        self.game_size = None

        # Level settings
        self.level_colors = [
            "red", "yellow", "green", "blue", "pink", "cyan", "orange", "clear"]
        self.level_original_colors = self.level_colors.copy()
        self.level_max_colors = 3
        self.level_current = 1
        self.level_diff = 1
        self.level_luck = 5

    def setter(self, attribute, value):
        """Set the value of an attribute."""
        
        setattr(self, attribute, value)

    def image(self, file_name):
        """Load an image, acting on current screen size."""

        if self.screen_size == (864, 900):
            return pygame.image.load(
                f"../images/2x/{file_name}.png").convert_alpha()
        else:
            return pygame.image.load(
                f"../images/1x/{file_name}.png").convert_alpha()

    def adjust(self, pos):
        """Adjust the position after resizing the screen."""

        if self.screen_size == (864, 900):
            return pos[0] * 2, pos[1] * 2
        else:
            return pos[0] // 2, pos[1] // 2

    def resize(self):
        """Resize the screen."""

        if self.screen_size == (864, 900):
            self.screen_size = self.screen_size[0]//2, self.screen_size[1]//2
            self.bubble_size = self.bubble_size[0]//2, self.bubble_size[1]//2
            self.bubble_speed = self.bubble_speed//2
        else:
            self.screen_size = self.screen_size[0]*2, self.screen_size[1]*2
            self.bubble_size = self.bubble_size[0]*2, self.bubble_size[1]*2
            self.bubble_speed = self.bubble_speed*2

    def colorize(self, id_color=None):
        """Return a color from the list of level colors."""

        if len(self.level_colors) > 0:
            if id_color is not None:
                return self.level_colors[id_color]
            else:
                return self.level_colors[randint(0, len(self.level_colors) - 1)]

    def prepare_level(self):
        """Prepare the level for the next game."""

        self.level_colors = self.level_original_colors.copy()
        shuffle(self.level_colors)
        self.level_colors = self.level_colors[:self.level_max_colors]

class Cursor:
    """Representation of the cursor."""

    def __init__(self, mixmi):
        """Initialize the game's cursor."""

        self.sett = mixmi.sett
        self.image = self.sett.image("cursor")
        self.size = self.image.get_size()
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.cursor = pygame.cursors.Cursor((0, 0), self.surface)
        pygame.mouse.set_cursor(self.cursor)

    def adjust(self):
        """Adjust the cursor's position after resizing."""

        self.size = self.sett.adjust(self.size)
        self.image = self.sett.image("cursor")
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.cursor = pygame.cursors.Cursor((0, 0), self.surface)
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
