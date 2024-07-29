import pygame
import numpy
from random import randint
from pygame.sprite import Sprite
from settings import Settings

class Bubble(Sprite):
    """A representation of a single bubble."""
    
    def __init__(self, mixmi_game, x_pos, y_pos):
        """Initialize the bubble and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()

        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Set the bubble's starting position
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Initialize the bubble's area
        self.position = (self.x_pos, self.y_pos)
        self.dimensions = (self.settings.bubble_radius * 2, 
                           self.settings.bubble_radius * 2)
        self.area = pygame.Rect(self.position, self.dimensions)

        # Colorize the bubble
        self.color = self.get_random_color()
        self.set_image()

        # Create placeholder for bubble's grid element ID
        self.grid_element_id = None

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
        
        # Set transparency
        self.image.set_alpha(200)

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

    def set_grid_element_id(self, grid_element_id):
        """Set the grid element ID of the bubble."""

        self.grid_element_id = grid_element_id


class PlayerBubble(Bubble):
    """A representation of a controllable bubble."""

    def __init__(self, mixmi_game):
        """Initialize the player bubble and set its starting position."""

        # Define the fixed starting position
        x_pos = mixmi_game.settings.bubble_radius * 21
        y_pos = mixmi_game.settings.bubble_radius * 60

        # Call the parent class's __init__() method
        super().__init__(mixmi_game, x_pos, y_pos)

        # Set the target position for current position before shooting
        self.target_x_pos = self.x_pos
        self.target_y_pos = self.y_pos

        # Set movement flags
        self.moving_left = False
        self.moving_right = False

    def set_target_position(self, new_target_position):
        """Set the target position for the player bubble."""

        self.target_x_pos = new_target_position[0]
        self.target_y_pos = new_target_position[1]

    def update_position_on_shooting(self):
        """Update the player bubble's position after player takes a shot."""

        """Shooting makes the bubble travel in a straight line to the target,
        and keeps traveling in that direction until it hits a wall."""
        
        # Move the bubble
        self.area.x = int(self.x_pos)
        self.area.y = int(self.y_pos)


    def update(self):
        """Update the player bubble's position as it moves."""
        
        if self.moving_left or self.moving_right:
            self.update_position_on_sliding()
        elif self.target_x_pos != self.x_pos or self.target_y_pos != self.y_pos:
            self.update_position_on_shooting()

    def update_position_on_sliding(self):
        """Update the player bubble's position as it slides left or right."""

        # Update position as it slides left
        if self.moving_left and self.area.left > self.settings.game_x_pos + ( 
                                             self.settings.bubble_radius * 2):
            self.area.x -= self.settings.bubble_speed
            self.target_x_pos -= self.settings.bubble_speed

        # Update position as it slides right
        if self.moving_right and self.area.right < self.settings.game_x_pos + (
                    self.settings.game_width - self.settings.bubble_radius * 2):
            self.area.x += self.settings.bubble_speed
            self.target_x_pos += self.settings.bubble_speed

