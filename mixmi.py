import sys
import pygame
from settings import Settings
from bubble import Bubble

class Mixmi:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """ Initialize the game, and create game resources."""

        # Initialize the pygame module
        pygame.init()
        # Set up the clock
        self.clock = pygame.time.Clock()
        # Initialize the settings
        self.settings = Settings()

        # Set up the display
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Set up the caption
        pygame.display.set_caption("mi X mi")

        # Create a group of bubbles
        self.bubbles = pygame.sprite.Group()

        # Create a grid of bubbles
        self._create_full_bubble_grid(25)


    def run_game(self):
        """Start the main game loop."""
        while True:
            # Check for user input
            self._check_events()
            # Animate background color
            self._change_background_color()
            # Refresh images on the screen
            self._update_screen()
            # Set the frame rate to 60 frames per second
            self.clock.tick(60)

    def _update_screen(self):
        """Control what the screen displays."""
        
        # Set the background color
        self.screen.fill(self.settings.background_color)

        # Draw all bubbles in the bubble group
        for bubble in self.bubbles.sprites():
            bubble.draw_bubble()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _change_background_color(self):
        """Change the background color of the screen."""

        # Get the current background colors
        red = self.settings.background_color[0]
        green = self.settings.background_color[1]
        blue = self.settings.background_color[2]

        # Animate the background color
        if green <= 130 and red == 70:
            green += 1
            blue -= 1
        else: red = 71
        if green >= 70 and red == 71:
            green -= 1
            blue += 1
        else: red = 70

        # Update the background color
        self.settings.background_color = (red, green, blue)

    def _check_events(self):
        """Respond to keypresses and mouse events."""

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            # Enable the quit game option
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_bubble(self, x_pos, y_pos):
        """Create a bubble at a specific position."""

        new_bubble = Bubble(self, x_pos, y_pos)
        self.bubbles.add(new_bubble)

    def _create_full_bubble_row(self, y_pos, row_is_even=True):
        """Create a full row of bubbles."""

        # Get necessary values
        screen_width = self.settings.screen_width
        margin = self.settings.screen_margin
        bubble_diameter = self.settings.bubble_radius * 2

        # Calculate the maximum number of bubbles that can fit in a row
        max_bubbles_per_row = int((screen_width - 2 * margin) / (bubble_diameter))

        if row_is_even:
            # Fill the row using the leftmost bubble as a reference
            for i in range(max_bubbles_per_row):
                x_pos = margin + i * bubble_diameter
                new_bubble = Bubble(self, x_pos, y_pos)
                self.bubbles.add(new_bubble)
        
        else:
            # Fill the row using the leftmost bubble as a reference
            # and shift the bubbles by half a bubble diameter
            for i in range(max_bubbles_per_row - 1):
                x_pos = margin + self.settings.bubble_radius + i * bubble_diameter
                new_bubble = Bubble(self, x_pos, y_pos)
                self.bubbles.add(new_bubble)

    def _create_full_bubble_grid(self, row_number):
        """Create a full grid of bubbles."""

        # Get necessary settings
        margin = self.settings.screen_margin
        bubble_diameter = self.settings.bubble_radius * 2

        # Create first row of bubbles
        self._create_full_bubble_row(margin, True)

        # Create the rest of the rows (without the margin):
        for i in range(1, row_number):
            y_pos = margin + i * bubble_diameter
            if i % 2 == 0:
                self._create_full_bubble_row(y_pos, True)
            else:
                self._create_full_bubble_row(y_pos, False)


# Run the game
if __name__ == '__main__':
    mxm = Mixmi()
    mxm.run_game()