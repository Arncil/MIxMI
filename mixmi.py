import sys
import pygame
from settings import Settings
from areas import GameArea
from grids import GridElement
from bubble import Bubble

class Mixmi:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """ Initialize the game, and create game resources."""

        # Initialize basic functionality
        pygame.init() # Initialize pygame modules
        self.clock = pygame.time.Clock() # Create a clock object
        self.settings = Settings() # Get the game settings

        # Set up the display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("mi X mi")

        # Create the game_area
        self.game_area = GameArea(self)

        # Create a grid for the game area
        self.grid = pygame.sprite.Group()
        self._create_game_grid()
        self.grid_is_visible = True

        # Create a bubble group
        self.bubbles = pygame.sprite.Group()

        # Create a bubble at a specific grid element
        self._create_bubble(0)
        self._create_bubble(20)
        self._create_bubble(37)
        self._create_bubble(13)

    def run_game(self):
        """Start the main game loop."""

        while True:
            # Check for user input
            self._check_events()

            # Refresh images on the screen
            self._update_screen()

            # Set the frame rate to 60 frames per second
            self.clock.tick(60)

    def _update_screen(self):
        """Control what the screen displays."""
        
        # Set the background color
        self.screen.fill(self.settings.background_color)

        # Draw the game_area
        self.game_area.draw_game_area()

        # Draw the grid for the game area
        if self.grid_is_visible:
            for element in self.grid.sprites():
                element.draw_grid_element()
        
        # Draw the bubbles
        for bubble in self.bubbles.sprites():
            bubble.draw_bubble()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_game_grid(self):
        """Create a grid (of grid elements) for the game area."""

        # Determine necessary parameters
        width = self.settings.bubble_radius * 2
        height = self.settings.bubble_radius * 2
        number_per_row = int(self.settings.game_width / width)
        number_per_column = int(self.settings.game_height / height)
        x_pos = self.settings.game_x_pos
        y_pos = self.settings.game_y_pos

        # Create a full grid for the game area
        for row in range(number_per_column):
            # Create a row of grid elements
            if row % 2 == 0:
                for element in range(number_per_row):
                    new_element = GridElement(self, 
                    x_pos + element * width, y_pos)
                    self.grid.add(new_element)
            # Every other row is shifted by half a bubble
            else:
                for element in range(number_per_row - 1):
                    new_element = GridElement(self, 
                    x_pos + element * width + int(width / 2), y_pos)
                    self.grid.add(new_element)
            y_pos += height

        # Print all IDs of the grid elements
        #for element in self.grid.sprites():
        #    print(element.id)
        
    def _check_events(self):
        """Respond to keypresses and mouse events."""

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            # Enable the quit game option
            if event.type == pygame.QUIT:
                sys.exit()
            # Enable the grid visibility option (press 'g')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.grid_is_visible = not self.grid_is_visible

    def _create_bubble(self, grid_element_id):
        """Create a bubble at specified position on a grid."""

        # Find the grid element with the specified ID
        for element in self.grid.sprites():
            if element.id == grid_element_id:
                x_pos = element.area.topleft[0]
                y_pos = element.area.topleft[1]
                break
        
        # Create a bubble at the specified position
        new_bubble = Bubble(self, x_pos, y_pos)
        self.bubbles.add(new_bubble)

        



    


        

# Run the game
if __name__ == '__main__':
    mxm = Mixmi()
    mxm.run_game()