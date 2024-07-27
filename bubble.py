import pygame
import math

class Bubble:
    """A representation of a bubble."""

    def __init__(self, mxm_game):
        """Initialize the bubble and its starting position."""
        # Reference to the game screen and settings.
        self.screen = mxm_game.screen
        self.settings = mxm_game.settings

        # Load the bubble image and get its rect.
        self.original_image = pygame.image.load_extended('images/bubble_red.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Set the starting position for the bubble.
        self.screen_rect = mxm_game.screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # Initialize the target position to the starting position.
        self.target_x = self.rect.x
        self.target_y = self.rect.y

        # Initialize the bubble's current position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Initialize the rotation angle.
        self.angle = 0

    def set_target_position(self, x, y):
        """Set the target position for the bubble."""
        self.target_x = x
        self.target_y = y

    def rotate(self):
        """Rotate the bubble image."""
        # Increment the angle and keep it within 0-359 degrees.
        self.angle = (self.angle + self.settings.bubble_rotation_speed) % 360 
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = new_rect

    def update(self):
        """Update the bubble's position."""
        # Calculate the direction vector from the current position to the target position.
        direction_x = self.target_x - self.x
        direction_y = self.target_y - self.y
        distance = math.hypot(direction_x, direction_y)  # Calculate the distance to the target.

        if distance > self.settings.bubble_speed:
            # Normalize the direction vector.
            direction_x /= distance
            direction_y /= distance

            # Move the bubble incrementally.
            self.x += direction_x * self.settings.bubble_speed
            self.y += direction_y * self.settings.bubble_speed

            # Update the rect position.
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            # Rotate the bubble.
            self.rotate()

        else:
            # If the bubble is close enough to the target, snap to the target.
            self.x = self.target_x
            self.y = self.target_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def draw_bubble(self):
        """Draw the bubble at its current location."""
        self.screen.blit(self.image, self.rect)