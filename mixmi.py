import sys
import pygame
from settings import Settings
from bubble import Bubble

class Mixmi:
    def __init__(self):
        """Initialize the game, and create game resources."""
        # Initialize all imported pygame modules.
        pygame.init()
        # Create an instance of Settings to store game settings.
        self.settings = Settings()
        # Set up the display window with the specified width and height.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Name a window.
        pygame.display.set_caption('mi X mi')
        # Create a clock object to manage the frame rate.
        self.clock = pygame.time.Clock()
        # Create an instance of a Bubble.
        self.bubble = Bubble(self)

    def run_game(self):
        """Start the main game loop."""
        while True:
            # Check for events like keypresses and mouse clicks.
            self._check_events()
            # Update the screen with the latest changes.
            self._update_screen()
            # Update the bubble's position.
            self.bubble.update()
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            # Set frames per second to 60.
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            # Enable exiting the game by closing the window.
            if event.type == pygame.QUIT:
                sys.exit()
            # Listen for mouse clicks.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # On left click set bubble's target position to mouse position.
                if event.button == 1:
                    self.bubble.set_target_position(event.pos[0], event.pos[1])

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Fill the screen with background color defined in settings.
        self.screen.fill(self.settings.background_color)
        # Draw the bubble at its current location.
        self.bubble.draw_bubble()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    mxm = Mixmi()
    mxm.run_game()