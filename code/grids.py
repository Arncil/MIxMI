import pygame

class GridElement(pygame.sprite.Sprite):
    """A class to represent an element of the grid."""

    # Class attribute for unique grid element IDs
    _id_counter = 0

    def __init__(self, mixmi_game, position):
        """Initialize the grid element and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()

        # Assign a unique ID and increment the counter
        self.id = GridElement._id_counter
        GridElement._id_counter += 1

        # Set up the basics
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Set up the rectangle
        self.position = position
        self.rect = pygame.Rect(self.position, self.settings.bubble_size)

    def update(self):
        """Draw the grid element on the screen."""

        # Draw the grid element's outline 
        pygame.draw.rect(self.screen, (237, 60, 200), self.rect, 1)

    def adjust(self):
        """Adjust the position after resizing the screen."""

        self.position = self.settings.adjust_position(self.position)
        self.rect = pygame.Rect(self.position, self.settings.bubble_size)