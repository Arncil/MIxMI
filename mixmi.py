import sys
import pygame
from settings import Settings

class Mixmi:
    """Main class for managing game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        # Ensure that pygame works properly. 
        pygame.init()
        # Introduce frame counter.
        self.clock = pygame.time.Clock()
        # Create settings.
        self.settings = Settings()
        # Create display window.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Name display window.
        pygame.display.set_caption("mi X mi")

    def run_game(self):
        """Start the main game loop."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.background_color)

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            # Set frames per second to 60.
            self.clock.tick(60)
        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    mxm = Mixmi()
    mxm.run_game()