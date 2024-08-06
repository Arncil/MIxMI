import pygame, sys, time
from random import randint
from settings import Settings, Cursor
from settings import get_window_pos, set_window_pos, calculate_distance
from areas import StartArea, BarArea, GameArea, LevelArea, ControlArea
from bubbles import Bubble, PlayerBubble

class Mixmi:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game with the default settings."""

        # Set up the basics
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Set up the screen
        self.screen = (
            pygame.display.set_mode(self.settings.screen_size, pygame.NOFRAME))
        self.screen.blit(pygame.image.load(
                        self.settings.get_image('background.png')), (0,0))
        pygame.display.set_caption(self.settings.screen_title)
        pygame.display.set_icon(
            pygame.image.load('../images/fixed/bubble_icon.png'))

        # Set up the cursor
        self.cursor = Cursor(self)

        # Set up areas
        self.start_area = StartArea(self)
        self.bar_area = BarArea(self)
        self.control_area = ControlArea(self)
        self.game_area = GameArea(self)
        self.level_area = LevelArea(self)

        # Set up levels
        self.game_over = False
        self.current_level = 1
        self.level_area.level_buttons[0].unlock()

        # Set up the bubbles
        self.player_bubble = PlayerBubble(self)
        self.bubbles = pygame.sprite.Group()

        # TEMPORARY (testing purposes)
        self.level_area.level_buttons[1].unlock()
        #self._create_bubble(5, color_id=0)

        # Set up variables for window dragging
        self.drag = False
        self.drag_offset = (0, 0)
        self.window_start_pos = (0, 0)

    def run_game(self):
        while True:
            self._handle_events()
            self._update()
            self.clock.tick(self.settings.screen_fps)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCREEN METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update(self):
        """Update images on the screen and flip to the new screen."""

        # Clear the screen
        self.screen.blit(pygame.image.load(
                         self.settings.get_image('background.png')), (0,0))

        # Update active areas
        self.bar_area.update()
        if self.start_area.is_active:
            self.start_area.update()
            
        if self.game_area.is_active:
            self.control_area.update(self.game_area.is_active,
                                     self.level_area.is_active)
            self.game_area.update()
            self._finish_game_when_game_over()
            self._update_player_bubble()
            self.bubbles.update()

        if self.level_area.is_active:
            self.control_area.update(self.game_area.is_active,
                                     self.level_area.is_active)
            self.level_area.update()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_player_bubble(self):
        """Control the player bubble behavior."""

        # Update player bubble when it's in the game area
        if self.game_area.rect.collidepoint(self.player_bubble.position):
            self.player_bubble.update()
            # Check for collisions with other bubbles
            if pygame.sprite.spritecollideany(self.player_bubble, self.bubbles):
                self._handle_collision()
        # Otherwise, reset the player bubble
        else:
            self._reset_player_bubble()

    def _adjust(self):
        """Set the correct positions after resizing the screen."""

        self.bar_area.adjust()
        self.start_area.adjust()
        self.control_area.adjust()
        self.level_area.adjust()
        self.game_area.adjust()
        self.player_bubble.adjust()
        for bubble in self.bubbles:
            bubble.adjust()

    def _switch_sizes(self):
        """Switch all elements after resizing the screen."""

        self.settings.switch_screen_size()
        self.screen = pygame.display.set_mode(self.settings.screen_size,
                                                         pygame.NOFRAME)
        self.cursor.resize()
        self._adjust()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUBBLE LOGIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _create_bubble(self, grid_element_id, color=None, color_id=None):
        """Create a bubble at specified position on the grid."""

        # Refuse to create a bubble if the grid element is out of bounds
        if grid_element_id == None:
            return
        if grid_element_id >= self.settings.game_area_grid_size:
            return

        # Find the grid element by its ID
        for element in self.game_area.grid:
            if element.id == grid_element_id:
                position = element.position
                break

        # Create the bubble
        if color_id is not None:
            bubble = Bubble(self, position, grid_element_id, 
                            self.settings.bubble_colors[color_id])
        elif color is not None:
            bubble = Bubble(self, position, grid_element_id, color)
        else:
            bubble = Bubble(self, position, grid_element_id)

        # Add the bubble to the group
        self.bubbles.add(bubble)

    def _get_ids_around(self, grid_element_id):
        """Return the list of IDs around the specified grid element."""

        """This algorithm is based on the hexagonal grid system. It calculates
        the IDs of the elements around the specified element. The grid is
        divided into two types of rows: longer and shorter. The longer rows
        have one more element than the shorter ones. The algorithm checks the
        position of the specified element and returns the IDs of the elements
        around it. BEWARE: This specific implementation works only if the number
        of rows is even, and grid starts with the longer row."""

        # Refuse to get ids if the grid element is out of bounds
        if grid_element_id == None:
            return
        if grid_element_id >= self.settings.game_area_grid_size:
            return

        # Set up necessary values
        I = grid_element_id
        # Number of rows
        R = self.game_area.image.get_height() // self.settings.bubble_size[1] * 6 // 5
        # Number of elements in a longer row
        L = self.game_area.image.get_width() // self.settings.bubble_size[0]
        # Number of elements in a shorter row
        S = self.game_area.image.get_width() // self.settings.bubble_size[0] - 1
        # Total number of elements
        T = R//2*(L+S) # Total number of elements

        if I == 0: return [I+1, I+L] # Top left corner
        elif I == L-1: return [I-1, I+S] # Top right corner
        elif I == T-S: return [I-L, I-S, I+1] # Bottom left corner
        elif I == T-1: return [I-L, I-S, I-1] # Bottom right corner
        elif 0 < I and I < L-1: return [I-1, I+1, I+S, I+S+1] # Top row
        elif T-S < I and I < T-1: return [I-L, I-S, I-1, I+1] # Bottom row
        elif I%(L+S) == 0: return [I-S, I+1, I+L] # Leftmost, longer
        elif (I-S)%(L+S) == 0: return [I-L, I-1, I+S] # Rightmost, longer
        elif (I-L)%(L+S) == 0: return [I-L, I-S, I+1, I+S, I+L] # Leftmost, shorter
        elif (I+1)%(L+S) == 0: return [I-L, I-S, I-1, I+S, I+L] # Rightmost, shorter
        else: return [I-L, I-S, I-1, I+1, I+S, I+L] # Any other element

    def _create_bubbles_around(self, grid_element_id):
        """Create bubbles around the specified grid element."""

        # Find places around the specified grid element
        ids_around = self._get_ids_around(grid_element_id)

        # Remove occupied places
        occupied = []
        for bubble in self.bubbles:
            occupied.append(bubble.grid_element_id)
        for place in occupied: 
            if place in ids_around: ids_around.remove(place)

        # Remove places based on the difficulty
        # When the difficulty is 1, remove 4 random places
        if self.settings.level_difficulty == 1:
            if len(ids_around) > 4:
                for _ in range(4): 
                    ids_around.pop(randint(0, len(ids_around)-1))
        # When the difficulty is 2, remove 3 random places
        elif self.settings.level_difficulty == 2:
            if len(ids_around) > 3:
                for _ in range(3): 
                    ids_around.pop(randint(0, len(ids_around)-1))
        # When the difficulty is 3, remove 2 random places
        elif self.settings.level_difficulty == 3:
            if len(ids_around) > 2:
                for _ in range(2): 
                    ids_around.pop(randint(0, len(ids_around)-1))
        # When the difficulty is 4, remove 1 random place
        elif self.settings.level_difficulty == 4:
            if len(ids_around) > 1:
                ids_around.pop(randint(0, len(ids_around)-1))

        # Get the color of the bubble at the specified grid element
        for bubble in self.bubbles:
            if bubble.grid_element_id == grid_element_id:
                color = bubble.color
                break

        # Create bubbles at remaining places
        # Base the color of new bubbles on self.settings.level_luck
        # At level luck = 5 bubbles have 80% chance of being the same color
        if self.settings.level_luck == 5:
            for place in ids_around:
                if randint(1, 10) <= 8:
                    self._create_bubble(place, color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 4 bubbles have 60% chance of being the same color
        elif self.settings.level_luck == 4:
            for place in ids_around:
                if randint(1, 10) <= 6:
                    self._create_bubble(place, color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 3 bubbles have 40% chance of being the same color
        elif self.settings.level_luck == 3:
            for place in ids_around:
                if randint(1, 10) <= 4:
                    self._create_bubble(place, color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 2 bubbles have 20% chance of being the same color
        elif self.settings.level_luck == 2:
            for place in ids_around:
                if randint(1, 10) <= 2:
                    self._create_bubble(place, color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 1 bubbles have 10% chance of being the same color
        elif self.settings.level_luck == 1:
            for place in ids_around:
                if randint(1, 10) == 1:
                    self._create_bubble(place, color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)

    def _multiply_bubbles(self):
        """Create bubbles at all grid elements."""

        for bubble in self.bubbles.sprites():
            self._create_bubbles_around(bubble.grid_element_id)

    def _is_occupied(self, grid_element_id):
        """Return True if the specified grid element is occupied."""

        for bubble in self.bubbles.sprites():
            if bubble.grid_element_id == grid_element_id:
                return True
        return False

    def _find_bubble_cluster(self, first_id, bubble_cluster=None):
        """Return the set of IDs of connected bubbles of the same color."""

        # Create a set to avoid duplicates
        if bubble_cluster is None:
            bubble_cluster = set()

        # Add first ID and elements around it to the set
        bubble_cluster.add(first_id)
        ids_around = self._get_ids_around(first_id)

        # Add same colored bubbles to the cluster, and repeat recursively
        color = self.player_bubble.color
        for id_ in ids_around:
            if id_ not in bubble_cluster:
                for bubble in self.bubbles.sprites():
                    if bubble.grid_element_id == id_ and bubble.color == color:
                        self._find_bubble_cluster(id_, bubble_cluster)

        return bubble_cluster

    def _burst_bubble_cluster(self, bubble_cluster):
        """Remove connected bubbles of the same color from the game."""

        # At least 3 bubbles need to be connected to form a cluster
        if len(bubble_cluster) > 2:
            for bubble in self.bubbles.sprites():
                if bubble.grid_element_id in bubble_cluster:
                    bubble.kill()

    def _burst_or_multiply(self, grid_element_id):
        """Burts or multiplies bubbles based on the conditions."""

        """Bubbles burst then, and only then, when there are at least three 
        bubbles of the same color connected to each other, and they have just
        collided with player's bubble of the same color. Otherwise, every
        bubble in the game area will multiply all around."""

        bubble_cluster = self._find_bubble_cluster(grid_element_id)
        if len(bubble_cluster) > 2:self._burst_bubble_cluster(bubble_cluster)
        else: self._multiply_bubbles()

    def _is_bubble_lonely(self, grid_element_id):
        """Return True if the specified bubble is not connected to any other."""

        ids_around = self._get_ids_around(grid_element_id)
        for id_ in ids_around:
            if self._is_occupied(id_):
                return False
        return True

    def _burst_lonely_bubbles(self):
        """Remove bubbles that are not connected to any other bubble."""

        for bubble in self.bubbles.sprites():
            if self._is_bubble_lonely(bubble.grid_element_id):
                bubble.kill()

    def _get_unique_colors(self):
        """Return a list of unique colors of bubbles on the screen."""

        unique_colors = []
        for bubble in self.bubbles.sprites():
            if bubble.color not in unique_colors:
                unique_colors.append(bubble.color)
        return unique_colors

    def _lower_max_color(self):
        """Lower the maximum number of colors for the bubbles."""

        unique_colors = self._get_unique_colors()
        self.settings.set_bubble_colors(unique_colors)
        self.settings.set_max_color(len(unique_colors))

    def _is_grid_empty(self):
        """Return True if the game area is empty."""

        if len(self.bubbles.sprites()) == 0:
            return True

    # ~~~~~~~~~~~~~~~~~~~~~~~ PLAYER BUBBLE LOGIC ~~~~~~~~~~~~~~~~~~~~~~~

    def _reset_player_bubble(self):
        """Reset the player bubble to the starting position."""

        self.player_bubble = PlayerBubble(self, color=self.settings.bubble_saved)
        self.settings.reroll_bubble_saved()

    def _switch_bubble(self):
        """Switch the player bubble to the saved one."""

        new_color = self.settings.bubble_saved
        self.settings.set_bubble_saved(self.player_bubble.color)
        self.player_bubble.set_color(new_color)

    def _find_snapping_point(self):
        """Return ID of empty grid element closest to the player bubble."""
    
        # Make a list of possible snapping points
        snapping_points = []
        grid_elements = pygame.sprite.spritecollide(
            self.player_bubble, self.game_area.grid, False)
        for element in grid_elements:
            if not self._is_occupied(element.id):
                snapping_points.append(element.id)
        
        # When there are more than one snapping point return the closest one
        if len(snapping_points) > 1:
            closest_id = self._choose_closest_id(snapping_points)
            return closest_id

        # And when there is only one snapping point return it
        elif len(snapping_points) == 1:
            return snapping_points[0]

    def _choose_closest_id(self, list_of_ids):
        """Return the ID of the closest grid element to the player bubble."""

        closest_id = None
        player_center = self.player_bubble.rect.center
        shortest_distance = float('inf')
        for id_ in list_of_ids:
            distance = self._calculate_distance_to_element(player_center, id_)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_id = id_
        return closest_id
                
    def _calculate_distance_to_element(self, starting_point, grid_element_id):
        """Return the distance between given point and grid element's center."""

        for element in self.game_area.grid.sprites():
            if element.id == grid_element_id:
                element_center = element.rect.center
                break
        return calculate_distance(starting_point, element_center)

    def _handle_collision(self):
        """Handle the collision between the player bubble and other bubbles."""

        color = self.player_bubble.color
        snapping_point = self._find_snapping_point()
        self._create_bubble(snapping_point, color=color)
        time.sleep(0.08)
        if not self.game_over:
            self._burst_or_multiply(snapping_point)
            self._burst_lonely_bubbles()
            self._lower_max_color()
            self._reset_player_bubble()
        else:
            self.player_bubble.kill()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LEVELS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_for_game_over(self):
        """Return True if the game is over."""

        """Game is over when player bubble collides with bubbles before
        being shot."""

        if not self.player_bubble.is_shooting:
            for bubble in self.bubbles.sprites():
                if pygame.sprite.collide_rect(self.player_bubble, bubble):
                    return True

    def _finish_game_when_game_over(self):
        """Handle the game over event."""

        if self._check_for_game_over():
            self.game_over = True
            #time.sleep(1)
            #self._switch_areas(self.game_area, self.level_area)

    def _reset_level(self):
        """Reset the level to the beginning."""

        self._create_level(self.current_level)

    def _create_level(self, level_id):
        """Create a level based on the specified ID."""

        # Set the current level
        self.game_over = False
        self.current_level = level_id

        # Clear the bubbles
        self.bubbles.empty()

        # Reset settings
        self.settings.bubble_max_color = 8
        self.settings.bubble_colors = self.settings.bubble_original_colors.copy()
        
        # Make the order of the bubble colors random
        self.settings.shuffle_bubble_colors()

        # Dynamically get the method name
        method_name = f"_create_level_{level_id}"
        method = getattr(self, method_name)

        # Call the method if it exists
        if method: method()

    def _set_level_settings(self, level, max_color, difficulty, luck):
        """Set the level settings based on the specified parameters."""

        # Set the settings
        self.current_level = level
        self.control_area.set_level(level)
        self.control_area.set_difficulty(difficulty)
        self.control_area.set_luck(luck)
        self.settings.set_max_color(max_color)
        self.settings.set_difficulty_and_luck(difficulty, luck)

        # Reset the player bubble after changing the settings
        self.settings.reroll_bubble_saved()
        self._reset_player_bubble()

    #TODO make some better algorithm for those bubbles
    def _create_level_1(self):
        """Create the first level of the game."""

        self._set_level_settings(1, 3, 1, 5)

        # Create the bubbles
        self._create_bubble(5, color_id=0)
        self._create_bubble(5+43, color_id=0)
        self._create_bubble(5+43*2, color_id=0)
        self._create_bubble(5+43*3, color_id=0)
        self._create_bubble(5+43*4, color_id=1)
        self._create_bubble(5+43*5, color_id=2)
        self._create_bubble(11, color_id=0)
        self._create_bubble(11+43, color_id=1)
        self._create_bubble(11+43*2, color_id=2)
        self._create_bubble(11+43*3, color_id=0)
        self._create_bubble(11+43*4, color_id=1)
        self._create_bubble(11+43*5, color_id=2)
        self._create_bubble(16, color_id=0)
        self._create_bubble(16+43, color_id=1)
        self._create_bubble(16+43*2, color_id=2)
        self._create_bubble(16+43*3, color_id=0)
        self._create_bubble(16+43*4, color_id=1)
        self._create_bubble(16+43*5, color_id=2)
        self._create_bubble(5+21, color_id=0)
        self._create_bubble(5+22, color_id=0)
        self._create_bubble(5+21+43, color_id=1)
        self._create_bubble(5+22+43, color_id=1)
        self._create_bubble(5+21+43*2, color_id=2)
        self._create_bubble(5+22+43*2, color_id=2)
        self._create_bubble(5+21+43*3, color_id=0)
        self._create_bubble(5+22+43*3, color_id=0)
        self._create_bubble(5+21+43*4, color_id=1)
        self._create_bubble(5+22+43*4, color_id=1)
        self._create_bubble(11+21, color_id=0)
        self._create_bubble(11+22, color_id=0)
        self._create_bubble(11+21+43, color_id=1)
        self._create_bubble(11+22+43, color_id=1)
        self._create_bubble(11+21+43*2, color_id=2)
        self._create_bubble(11+22+43*2, color_id=2)
        self._create_bubble(11+21+43*3, color_id=0)
        self._create_bubble(11+22+43*3, color_id=0)
        self._create_bubble(11+21+43*4, color_id=1)
        self._create_bubble(11+22+43*4, color_id=1)
        self._create_bubble(16+21, color_id=0)
        self._create_bubble(16+22, color_id=0)
        self._create_bubble(16+21+43, color_id=1)
        self._create_bubble(16+22+43, color_id=1)
        self._create_bubble(16+21+43*2, color_id=2)
        self._create_bubble(16+22+43*2, color_id=2)
        self._create_bubble(16+21+43*3, color_id=0)
        self._create_bubble(16+22+43*3, color_id=0)
        self._create_bubble(16+21+43*4, color_id=1)
        self._create_bubble(16+22+43*4, color_id=1)
        self._create_bubble(6+43*2, color_id=0)
        self._create_bubble(7+43*2, color_id=0)
        self._create_bubble(8+43*2, color_id=2)
        self._create_bubble(9+43*2, color_id=0)
        self._create_bubble(10+43*2, color_id=0)
        self._create_bubble(6+22+43*2, color_id=0)
        self._create_bubble(7+22+43*2, color_id=2)
        self._create_bubble(8+22+43*2, color_id=2)
        self._create_bubble(9+22+43*2, color_id=0)
    #TODO 
    def _create_level_2(self):
        """Create the second level of the game."""

        self._set_level_settings(2, 3, 1, 5)

        # Create the bubbles
        self._create_bubble(5, color_id=0)
        self._create_bubble(5+43, color_id=1)
        self._create_bubble(5+43*2, color_id=2)
        

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ EVENT HANDLING ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _switch_areas(self, area_on, area_off):
        """Turn on one area and turn off another."""

        area_on.toggle()
        area_off.toggle()

    def _handle_events(self):
        """Handle mouse and keyboard events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_events_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_events_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_events_mousedown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_events_mouseup(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_events_mousemotion(event)

    def _handle_events_keydown(self, event):
        """Part of _handle_events method focused on keydown events."""

        # Enable closing with 'q' key
        if event.key == pygame.K_q:
            sys.exit()
        # Enable resizing with 'f' key
        if event.key == pygame.K_f:
            self._switch_sizes()

        if self.game_area.is_active:
            # Switch grid visibility with 'g' key
            if event.key == pygame.K_g:
                self.game_area.show_grid = not self.game_area.show_grid
            # Reset the level with 'r' key
            if event.key == pygame.K_r:
                self._reset_level()
            if not self.player_bubble.is_shooting:
                # Move player bubble to the left (press 'left' or 'a')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player_bubble.handle_movement('left')
                # Move player bubble to the right (press 'right' or 'd')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player_bubble.handle_movement('right')
                # Enable switching the player bubble with 's' key
                if event.key == pygame.K_s:
                    self._switch_bubble()

    def _handle_events_keyup(self, event):
        """Part of _handle_events method focused on keyup events."""

        if self.game_area.is_active:
            # Stop moving player bubble to the left (release 'left' or 'a')
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player_bubble.handle_movement('stop')
            # Stop moving player bubble to the right (release 'right' or 'd')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player_bubble.handle_movement('stop')

    def _handle_events_mousedown(self, event):
        """Part of _handle_events method focused on mousebuttondown events."""

        # On mouse left click
        if event.button == 1:
            # Enable minimizing
            if self.bar_area.minimize.is_in_button_area(event.pos):
                pygame.display.iconify()
            # Enable resizing
            if self.bar_area.resize.is_in_button_area(event.pos):
                self._switch_sizes()
            # Enable closing
            if self.bar_area.close.is_in_button_area(event.pos):
                sys.exit()

            if self.control_area.is_active:
                # Make back button clickable
                if self.control_area.back.is_in_button_area(event.pos):
                    self.control_area.back.click()
                # Make reset button clickable
                if self.control_area.reset.is_in_button_area(event.pos):
                    self.control_area.reset.click()

            if self.start_area.is_active:
                # Make play button clickable
                if self.start_area.play.is_in_button_area(event.pos):
                    self.start_area.play.click()
                # Make rules button clickable
                if self.start_area.rules.is_in_button_area(event.pos):
                    self.start_area.rules.click()
                # Make options button clickable
                if self.start_area.options.is_in_button_area(event.pos):
                    self.start_area.options.click()
                
            if self.level_area.is_active:
                # Make level buttons clickable
                for button in self.level_area.level_buttons:
                    if button.is_in_button_area(event.pos):
                        if not button.is_locked:
                            button.click()

            if self.game_area.is_active:
                if not self.player_bubble.is_shooting:
                    # Enable shooting
                    if  self.game_area.is_in_game_area(event.pos) and (
                            not (self.player_bubble.is_moving_left or (
                                 self.player_bubble.is_moving_right))):
                        self.player_bubble.set_target_position(event.pos)
                        self.player_bubble.handle_movement('shoot')
                    # Make left button clickable
                    if self.game_area.left.is_in_button_area(event.pos):
                        self.game_area.left.click()
                        self.player_bubble.handle_movement('left')
                    # Make right button clickable
                    if self.game_area.right.is_in_button_area(event.pos):
                        self.game_area.right.click()
                        self.player_bubble.handle_movement('right')
                    # Make switch button clickable
                    if self.game_area.switch.is_in_button_area(event.pos):
                        self.game_area.switch.click()
                    
            # Enable dragging
            elif self.bar_area.is_in_bar_area(event.pos):
                self.drag = True
                self.drag_start = event.pos
                self.window_start_pos = get_window_pos()

        # On mouse right click
        if event.button == 3:
            if self.game_area.is_active:
                if not self.player_bubble.is_shooting:
                    # Switch the player bubble with the saved one
                    self._switch_bubble()

    def _handle_events_mouseup(self, event):
        """Part of _handle_events method focused on mousebuttonup events."""

        if event.button == 1:
            # Disable dragging
            self.drag = False

            if self.start_area.is_active:
                # Handle play button
                if self.start_area.play.is_clicked:
                    self.start_area.play.click()
                    self.control_area.toggle()
                    self.start_area.toggle()
                    self.level_area.toggle()
                # Handle rules button
                if self.start_area.rules.is_clicked:
                    self.start_area.rules.click()
                # Handle options button
                if self.start_area.options.is_clicked:
                    self.start_area.options.click()
            
            if self.control_area.is_active:
                # Handle back button
                if self.control_area.back.is_in_button_area(event.pos):
                    self.control_area.back.click()
                    if self.level_area.is_active:
                        self.level_area.toggle()
                        self.start_area.toggle()
                        self.control_area.toggle()
                    if self.game_area.is_active:
                        self.game_area.toggle()
                        self.level_area.toggle()
                # Handle reset button
                if self.control_area.reset.is_in_button_area(event.pos):
                    self.control_area.reset.click()
                    self._reset_level()

            if self.level_area.is_active:
                # Handle level buttons
                for button in self.level_area.level_buttons:
                    if not button.is_locked:
                        if button.is_clicked:
                            button.click()
                            self._create_level(button.level)
                            self.level_area.toggle()
                            self.game_area.toggle()

            if self.game_area.is_active:
                if not self.player_bubble.is_shooting:
                    # Handle left button
                    if self.game_area.left.is_clicked:
                        self.game_area.left.click()
                        self.player_bubble.handle_movement('stop')
                    # Handle right button
                    if self.game_area.right.is_clicked:
                        self.game_area.right.click()
                        self.player_bubble.handle_movement('stop')
                    # Handle switch button
                    if self.game_area.switch.is_clicked:
                        self.game_area.switch.click()
                        self._switch_bubble()

    def _handle_events_mousemotion(self, event):
        """Part of _handle_events method focused on mousemotion events."""

        if self.drag:
            new_x = self.window_start_pos[0] + (
                (event.pos[0] - self.drag_start[0]))
            new_y = self.window_start_pos[1] + (
                (event.pos[1] - self.drag_start[1]))
            set_window_pos(new_x, new_y)

# Run the game
if __name__ == '__main__':
    mixmi = Mixmi()
    mixmi.run_game()