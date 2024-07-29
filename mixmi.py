import sys
import pygame
from settings import Settings
from areas import GameArea, LogoArea
from grids import GridElement
from bubbles import Bubble, PlayerBubble

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
        pygame.display.set_caption("MI x MI")
        pygame.display.set_icon(pygame.image.load('images/bubble_icon.png'))

        # Create the areas of the game
        self.game_area = GameArea(self)
        self.logo_area = LogoArea(self)

        # Create a grid for the game area
        self.grid = pygame.sprite.Group()
        self._create_game_grid()
        self.grid_is_visible = False

        # Create a bubble group
        self.bubbles = pygame.sprite.Group()

        # Create a bubble at a specific grid element
        self._create_bubble(0)
        self._create_bubble(37)


        # Create a player bubble
        self.player_bubble = PlayerBubble(self)


    def run_game(self):
        """Start the main game loop."""

        while True:
            # Check for user input
            self._check_events()

            # Update player bubble position
            self.player_bubble.update()

            # Refresh images on the screen
            self._update_screen()

            # Set the frame rate to 60 frames per second
            self.clock.tick(60)

    def _update_screen(self):
        """Control what the screen displays."""
        
        # Set the background color
        self.screen.fill(self.settings.background_color)

        # Draw the areas of the game
        self.game_area.draw_game_area()
        self.logo_area.draw_logo_area()

        # Draw the grid for the game area
        if self.grid_is_visible:
            for element in self.grid.sprites():
                element.draw_grid_element()
        
        # Draw the bubbles
        for bubble in self.bubbles.sprites():
            bubble.draw_bubble()

        # Draw the player bubble
        self.player_bubble.draw_bubble()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            # Enable the quit game option
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Enable the grid visibility option (press 'g')
                if event.key == pygame.K_g:
                    self.grid_is_visible = not self.grid_is_visible
                # Enable the bubble creation option (press 'space')
                if event.key == pygame.K_SPACE:
                    self._multiple_bubbles()
                # Enable player bubble move left (press 'left' or 'a')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player_bubble.moving_right = False
                    self.player_bubble.moving_left = True
                # Enable player bubble move right (press 'right' or 'd')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player_bubble.moving_left = False
                    self.player_bubble.moving_right = True
            
            elif event.type == pygame.KEYUP:
                # Disable player bubble move left (release 'left' or 'a')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player_bubble.moving_left = False
                # Disable player bubble move right (release 'right' or 'd')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player_bubble.moving_right = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set bubble's target position to the mouse position (left click)
                if event.button == 1:
                    self.player_bubble.set_target_position(event.pos)
                
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
        new_bubble.set_grid_element_id(grid_element_id)
        self.bubbles.add(new_bubble)

    def _get_grid_ids_around(self, el_id):
        """Return the list of IDs around a specified grid element."""

        # There are 30 rows in the grid
        # Every frist row has 20 elements
        # Every other row has 19 elements
        # There are 585 elements in total

        # Corners of the grid
        if el_id == 0: return [1, 20]
        elif el_id == 19: return [18, 38]
        elif el_id == 566: return [546, 547, 567]
        elif el_id == 584: return [564, 565, 583]

        # Top row of the grid
        elif el_id > 0 and el_id < 19:
            return [el_id - 1, el_id + 1, el_id + 19, el_id + 20]

        # Bottom row of the grid
        elif el_id > 566 and el_id < 584:
            return [el_id - 20, el_id - 19, el_id - 1, el_id + 1]

        # Leftmost column of the grid
        elif el_id > 0 and el_id % 39 == 0:
            return [el_id - 19, el_id + 1, el_id + 20]
        elif el_id < 566 and (el_id - 20) % 39 == 0:
            return [el_id - 20, el_id - 19, el_id + 1, el_id + 19, el_id + 20]
        
        # Rightmost column of the grid
        elif el_id > 19 and (el_id - 19) % 39 == 0:
            return [el_id - 20, el_id - 1, el_id + 19]
        elif el_id < 584 and (el_id - 38) % 39 == 0:
            return [el_id - 20, el_id - 19, el_id - 1, el_id + 19, el_id + 20]

        # All other elements
        else:
            return [el_id - 20, el_id - 19, el_id - 1, el_id + 1, el_id + 19, el_id + 20]

    def _create_bubbles_around_bubble(self, grid_element_id):
        """Create bubbles around the specified bubble."""

        # Check which places are occupied by bubbles
        places_occupied = []
        for bubble in self.bubbles.sprites():
            places_occupied.append(bubble.grid_element_id)

        # Check which places are around the bubble
        places_around = self._get_grid_ids_around(grid_element_id)

        # Remove occupied places from the list of places around
        for place in places_occupied:
            if place in places_around:
                places_around.remove(place)

        # Create bubbles at the places around the bubble
        for place in places_around:
            self._create_bubble(place)
        
    def _multiple_bubbles(self):
        """Create bubbles around each bubble in the grid."""
        
        # Create bubbles around each bubble in the grid
        for bubble in self.bubbles.sprites():
            self._create_bubbles_around_bubble(bubble.grid_element_id)

# Run the game
if __name__ == '__main__':
    mxm = Mixmi()
    mxm.run_game()