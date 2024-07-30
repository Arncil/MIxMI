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
            self._handle_events()
            self._update_player_bubble()
            self._update_screen()
            self.clock.tick(80)

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

    def _update_player_bubble(self):
        """Control the player bubble's movement."""

        # Check for collisions with other bubbles
        if pygame.sprite.spritecollideany(self.player_bubble, self.bubbles):
  
            # Get the color of current player bubble
            player_color = self.player_bubble.color

            # Check for collisions player's bubble and grid elements
            grid_element_id = self._check_collisions_player_grid()

            # Create a bubble at the grid element with the same color
            self._create_bubble(grid_element_id, player_color)

            # Check if there are any bubbles to remove
            self._burst_or_multiply(player_color, grid_element_id)

            # Reset the player bubble
            self.player_bubble.kill()
            self.player_bubble = PlayerBubble(self)

        # Update player bubble when it is in the game area
        if self.game_area.rect.collidepoint(self.player_bubble.rect.center):
            self.player_bubble.update()
    
        else:
            # Reset the player bubble
            self.player_bubble.kill()
            self.player_bubble = PlayerBubble(self)

    def _get_connected_bubbles(self, color, first_id, connected_bubbles=None):
        """Return the set of IDs of connected bubbles of the same color."""
        
        if connected_bubbles is None:
            # Use a set to avoid duplicates
            connected_bubbles = set() 

        # Add the current element to the set of connected bubbles
        connected_bubbles.add(first_id)

        # Get elements around the grid element
        elements_around = self._get_grid_ids_around(first_id)

        # Check if the elements around are of the same color
        for element in elements_around:
            if element not in connected_bubbles:  # Avoid re-checking elements
                for bubble in self.bubbles.sprites():
                    if bubble.grid_element_id == element and bubble.color == color:
                        self._get_connected_bubbles(color, element, (
                                                    connected_bubbles))

        return connected_bubbles

    def _burst_or_multiply(self, player_color, grid_element_id):
        """Burts or multiplies bubbles based on the conditions."""

        """Bubbles burst then, and only then, when there are at least three 
        bubbles of the same color connected to each other, and they have just
        collided with player's bubble of the same color. Otherwise, every
        bubble at game area will multiply by creating bubbles around itself."""

        # Check how many bubbles of the same color are connected
        connected_bubbles = self._get_connected_bubbles(
                                    player_color, grid_element_id)

        if len(connected_bubbles) >= 3:
            # Remove bubbles if there are at least three connected
            self._burst_bubbles(connected_bubbles)
        
        else:
            # Multiply bubbles if there are less than three connected
            self._multiply_all_bubbles()
        
    def _burst_bubbles(self, connected_bubbles):
        """Remove bubbles from the grid."""

        if len(connected_bubbles) >= 3:
            for bubble in self.bubbles.sprites():
                if bubble.grid_element_id in connected_bubbles:
                    bubble.kill()

    def _check_if_grid_element_is_occupied(self, grid_element_id):
        """Return True if the grid element is occupied by a bubble."""

        # Check if the grid element is occupied by a bubble
        for bubble in self.bubbles.sprites():
            if bubble.grid_element_id == grid_element_id:
                return True

    def _check_collisions_player_grid(self):
        """Return the ID at nearest empty grid element."""

        # Check for collisions player's bubble and grid elements
        for element in self.grid.sprites():
            if self.player_bubble.rect.colliderect(element.rect):
                # Get element's ID
                element_id = element.id
                # Check if the element is occupied
                if not self._check_if_grid_element_is_occupied(element_id):
                    return element_id

    def _handle_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            # Enable the quit game option
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_events(event)

    def _handle_keydown_events(self, event):
        """Respond to keypresses."""

        # Enable / Disable the grid visibility option (press 'g')
        if event.key == pygame.K_g:
            self.grid_is_visible = not self.grid_is_visible
        # Multiply bubbles (temporary function) (press 'space')
        if event.key == pygame.K_SPACE:
            self._multiply_all_bubbles()
        # Move player bubble to the left (press 'left' or 'a')
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player_bubble.moving_right = False
            self.player_bubble.moving_left = True
        # Move player bubble to the right (press 'right' or 'd')
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player_bubble.moving_left = False
            self.player_bubble.moving_right = True
        
    def _handle_keyup_events(self, event):
        """Respond to key releases."""

        # Disable player bubble move left (release 'left' or 'a')
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player_bubble.moving_left = False
        # Disable player bubble move right (release 'right' or 'd')
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player_bubble.moving_right = False

    def _handle_mouse_events(self, event):
        """Respond to mouse events."""

        # Set bubble's target position to the mouse position (left click)
        if event.button == 1:
            # But only if mouse is within the game area 
            if self.game_area.rect.collidepoint(event.pos) and event.pos[1] < (
                self.settings.game_height - self.settings.bubble_radius):
                self.player_bubble.set_target_position(event.pos)
                self.player_bubble.shooting = True

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
        
    def _create_bubble(self, grid_element_id, color=None):
        """Create a bubble at specified position on a grid."""

        # Find the grid element with the specified ID
        for element in self.grid.sprites():
            if element.id == grid_element_id:
                x_pos = element.rect.topleft[0]
                y_pos = element.rect.topleft[1]
                break
        
        # Create a bubble at the specified position
        new_bubble = Bubble(self, x_pos, y_pos)

        # Set the bubble's attributes
        new_bubble.set_grid_element_id(grid_element_id)
        if color: new_bubble.set_image(color)
        
        # Add the bubble to the group of bubbles
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
        
    def _multiply_all_bubbles(self):
        """Create bubbles around each bubble in the grid."""
        
        # Create bubbles around each bubble in the grid
        for bubble in self.bubbles.sprites():
            self._create_bubbles_around_bubble(bubble.grid_element_id)

# Run the game
if __name__ == '__main__':
    mxm = Mixmi()
    mxm.run_game()