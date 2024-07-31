import pygame, sys, time
from settings import Settings
from areas import GameArea, LogoArea
from grids import GridElement
from stages import Stage
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

        # Set up the cursor
        self.cursor = pygame.image.load('images/cursor.png').convert_alpha()
        self.cursor_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.cursor_surface.blit(self.cursor, (0, 0))
        self.cursor_data = pygame.cursors.Cursor((0, 0), self.cursor_surface)
        pygame.mouse.set_cursor(self.cursor_data)

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
        self._create_bubble(1)
        self._create_bubble(19)
        self._create_bubble(20)
        self._create_bubble(37)
        self._create_bubble(38)

        # Create a player bubble
        self.player_bubble = PlayerBubble(self)

    def run_game(self):
        """Start the main game loop."""

        while True:
            # Handle events
            self._handle_events()

            # Set the background color
            self.screen.fill(self.settings.background_color)

            # Update 
            self._update_player_bubble()
            self.bubbles.update()

            # Draw
            self.game_area.draw_game_area()
            self.logo_area.draw_logo_area()
            self.bubbles.draw(self.screen)
            self.player_bubble.draw()
            if self.grid_is_visible:
                for element in self.grid.sprites():
                    element.draw_grid_element()

            # Make the most recently drawn screen visible
            pygame.display.flip()   

            self.clock.tick(90)

    def _update_player_bubble(self):
        """Control the player bubble's behavior."""

        # Update player bubble when it is in the game area
        if self.game_area.rect.collidepoint(self.player_bubble.rect.center):
            self.player_bubble.update()

            # Check for collisions with other bubbles
            if pygame.sprite.spritecollideany(self.player_bubble, self.bubbles):
    
                # Get the color of current player's bubble
                player_color = self.player_bubble.color

                # Get the ID of the grid element nearest to the player bubble
                grid_element_id = self._snap_bubble_to_grid()

                # Create a bubble at the grid element with the same color
                self._create_bubble(grid_element_id, player_color)

                # Pause the game for a moment
                time.sleep(0.1)

                # Destroy a bubble cluster or multiply bubbles
                self._burst_or_multiply(player_color, grid_element_id)

                # Destroy bubbles that have nothing next to them
                self._burst_unattached_bubbles()

                # Reset the player bubble
                self.player_bubble.kill()
                self.player_bubble = PlayerBubble(self)

        # Otherwise, reset the player bubble
        else:
            self.player_bubble.kill()
            self.player_bubble = PlayerBubble(self)

    def _burst_unattached_bubbles(self):
        """Remove bubbles that have nothing next to them."""

        # Add to the list of suspects bubbles with more than 4 neighbors
        suspects = []
        for bubble in self.bubbles.sprites():
            if len(self._get_grid_ids_around(bubble.grid_element_id)) > 4:
                suspects.append(bubble.grid_element_id)

        # Kill bubble if it has no neighbors (or walls next to them) :c
        for bubble in self.bubbles.sprites():
            if bubble.grid_element_id in suspects:
                if not self._is_bubble_around_grid_element(
                                                    bubble.grid_element_id):
                    bubble.kill()
                    self.bubbles.update()
    
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

    def _is_bubble_around_grid_element(self, grid_element_id):
        """Return True if there is a bubble around the grid element."""

        # Get the IDs of elements around the grid element
        elements_around = self._get_grid_ids_around(grid_element_id)

        # Check if there is a bubble around the grid element
        for element in elements_around:
            for bubble in self.bubbles.sprites():
                if bubble.grid_element_id == element:
                    return True

    def _is_bubble_at_grid_element(self, grid_element_id):
        """Return True if the grid element is occupied by a bubble."""

        # Check if the grid element is occupied by a bubble
        for bubble in self.bubbles.sprites():
            if bubble.grid_element_id == grid_element_id:
                return True

    def _snap_bubble_to_grid(self):
        """Return ID of the nearest empty grid element to the player bubble."""

        # Make a list of potential nearest grid elements
        potential_nearest = []

        # Get all grid elements that collide with the player bubble
        grid_elements = pygame.sprite.spritecollide(self.player_bubble, 
                                                    self.grid, False)

        # Check which of them are empty
        for element in grid_elements:
            if not self._is_bubble_at_grid_element(element.id):
                potential_nearest.append(element.id)

        if len(potential_nearest) > 1:
            # Find the nearest grid element
            nearest_id = self._find_nearest_grid_element(potential_nearest)
            return nearest_id

        elif len(potential_nearest) == 1:
            return potential_nearest[0]

    def _find_nearest_grid_element(self, potential_nearest):
        """Return the ID of the nearest grid element to the player bubble."""

        # Get the center of the player bubble
        player_center = self.player_bubble.rect.center

        # Find the nearest grid element
        nearest_id = None
        nearest_distance = float('inf')
        for element in potential_nearest:
            distance = self._calculate_distance_bubble_grid(
                                     player_center, element)
            if distance < nearest_distance:
                nearest_id = element
                nearest_distance = distance

        return nearest_id

    def _calculate_distance_bubble_grid(self, player_center, element_id):
        """Return the distance between the player bubble and the grid element."""

        # Find the center of the grid element
        for element in self.grid.sprites():
            if element.id == element_id:
                element_center = element.rect.center
                break

        # Calculate the distance between the player bubble and the grid element
        distance = ((player_center[0] - element_center[0]) ** 2 + 
                    (player_center[1] - element_center[1]) ** 2) ** 0.5

        return distance

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
                self._handle_mousedown_events(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouseup_events(event)

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

    def _handle_mousedown_events(self, event):
        """Respond to mousedown events."""

        # Set bubble's target position to the mouse position (left click)
        if event.button == 1:
            # But only if mouse is within the game area 
            if self.game_area.rect.collidepoint(event.pos) and event.pos[1] < (
                self.settings.game_height - self.settings.bubble_radius) and (
                 self.player_bubble.shooting == False):
                self.player_bubble.set_target_position(event.pos)
                self.player_bubble.shooting = True
        # Move player bubble to the left (scroll up)
        if event.button == 4:
            self.player_bubble.moving_right = False
            self.player_bubble.moving_left = True
        # Move player bubble to the right (scroll down)
        if event.button == 5:
            self.player_bubble.moving_left = False
            self.player_bubble.moving_right = True

    def _handle_mouseup_events(self, event):
        """Respond to mouseup events."""

        # Stop moving player bubble left (scroll up release)
        if event.button == 4:
            self.player_bubble.moving_left = False
            self.player_bubble.moving_right = True

        # Stop moving player bubble right (scroll down release)
        if event.button == 5:
            self.player_bubble.moving_right = False
            self.player_bubble.moving_left = True

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

    def _get_grid_ids_around(self, el):
        """Return the list of IDs around a specified grid element."""

        # There are 30 rows in the grid, there are 585 elements in total
        # Every even row has 20 elements, every odd row has 19 elements

        # Corners of the grid
        if el == 0: return [1, 20]
        elif el == 19: return [18, 38]
        elif el == 566: return [546, 547, 567]
        elif el == 584: return [564, 565, 583]

        # Top row of the grid
        elif el > 0 and el < 19:
            return [el - 1, el + 1, el + 19, el + 20]

        # Bottom row of the grid
        elif el > 566 and el < 584:
            return [el - 20, el - 19, el - 1, el + 1]

        # Leftmost column of the grid
        elif el > 0 and el % 39 == 0:
            return [el - 19, el + 1, el + 20]
        elif el < 566 and (el - 20) % 39 == 0:
            return [el - 20, el - 19, el + 1, el + 19, el + 20]
        
        # Rightmost column of the grid
        elif el > 19 and (el - 19) % 39 == 0:
            return [el - 20, el - 1, el + 19]
        elif el < 584 and (el - 38) % 39 == 0:
            return [el - 20, el - 19, el - 1, el + 19, el + 20]

        # All other elements
        else:
            return [el - 20, el - 19, el - 1, el + 1, el + 19, el + 20]

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