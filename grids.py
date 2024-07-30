import pygame
from pygame.sprite import Sprite

class GridElement(Sprite):
    """A class to represent an element of the grid."""

    # Class attribute for unique grid element IDs
    _id_counter = 0

    def __init__(self, mixmi_game, x_pos, y_pos):
        """Initialize the grid element and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()

        # Assign a unique ID and increment the counter
        self.id = GridElement._id_counter
        GridElement._id_counter += 1

        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Initialize the grid element's area
        self.position = (x_pos, y_pos)
        self.dimensions = (self.settings.bubble_radius * 2,
                           self.settings.bubble_radius * 2)
        self.rect = pygame.Rect(self.position, self.dimensions)

    def draw_grid_element(self):
        """Draw the grid element on the screen."""

        # Draw the grid element's outline 
        pygame.draw.rect(self.screen, self.settings.grid_color, self.rect, 1)

        