import pygame
from random import randint
from pygame.sprite import Sprite
from settings import Settings

class Bubble(Sprite):
    """A representation of a single bubble."""
    
    def __init__(self, mixmi_game, x_pos=0, y_pos=0):
        """Initialize the bubble and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()
        # Set the screen to the screen attribute of the Mixmi class
        self.screen = mixmi_game.screen
        # Set bubble settings to the settings attribute of the Mixmi class
        self.settings = mixmi_game.settings

        # Initialize the bubble's area
        self.position = (x_pos, y_pos)
        self.dimensions = (self.settings.bubble_radius * 2, 
                           self.settings.bubble_radius * 2)
        self.area = pygame.Rect(self.position, self.dimensions)

        # Get a random color for the bubble
        self.color = self.get_random_color()
        # Load the image of the bubble
        self.set_image()

    def draw_bubble(self):
        """Draw the bubble on the screen."""
        # Blit the scaled image at the position of the original Rect
        self.screen.blit(self.image, self.area.topleft)

    def set_image(self):
        """Set the color of the bubble."""
        if self.color == "red":
            self.image = pygame.image.load('images/bubble_red.png').convert_alpha()
        elif self.color == "yellow":
            self.image = pygame.image.load('images/bubble_yellow.png').convert_alpha()
        elif self.color == "green":
            self.image = pygame.image.load('images/bubble_green.png').convert_alpha()
        elif self.color == "blue":
            self.image = pygame.image.load('images/bubble_blue.png').convert_alpha()
        elif self.color == "pink":
            self.image = pygame.image.load('images/bubble_pink.png').convert_alpha()
        elif self.color == "cyan":
            self.image = pygame.image.load('images/bubble_cyan.png').convert_alpha()
        elif self.color == "orange":
            self.image = pygame.image.load('images/bubble_orange.png').convert_alpha()
        elif self.color == "grey":
            self.image = pygame.image.load('images/bubble_grey.png').convert_alpha()

    def get_random_color(self):
        """Return a random color for the bubbles."""

        # Get a random number between 0 and the color number
        random_number = randint(0, self.settings.color_number - 1)

        # Get the color based on the random number
        if random_number == 0: return "red"
        elif random_number == 1: return "yellow"
        elif random_number == 2: return "green"
        elif random_number == 3: return "blue"
        elif random_number == 4: return "pink"
        elif random_number == 5: return "cyan"
        elif random_number == 6: return "orange"
        elif random_number == 7: return "grey"