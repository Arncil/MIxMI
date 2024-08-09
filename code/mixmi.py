import pygame as pg
import sys, time
from random import randint
from settings import Settings, Cursor
from settings import get_window_pos, set_window_pos, calculate_distance
from areas import Bar, Start, Control, Levels, Game, Lost, Won
from bubbles import Bubble, Player

class Mixmi:
    """Representation a mixmi game."""

    def __init__(self):
        """Initialize the game."""

        # Set up the basics
        pg.init()
        self.clock = pg.time.Clock()
        self.sett = Settings()

        # Set up the window
        self.screen = pg.display.set_mode(self.sett.screen_size, pg.NOFRAME)
        pg.display.set_icon(pg.image.load("../images/fixed/bubble_icon.png"))
        pg.display.set_caption("MI x MI")
        self.cursor = Cursor(self)

        # Set up the areas
        self.bar = Bar(self)
        self.start = Start(self)
        self.control = Control(self)
        self.levels = Levels(self)
        self.game = Game(self)
        self.lost = Lost(self)
        self.won = Won(self)

        # Set up the bubbles
        self.bubbles = pg.sprite.Group()
        self.player = Player(self)

        # Set up game related states
        self.game_on = False
        self.game_lost = False
        self.game_won = False

        # TEMPORARY: testing
        self.levels.buttons[0].unlock()
        # unclock every level
        for button in self.levels.buttons:
            button.unlock()

        # Set up states for window dragging
        self.drag = False
        self.drag_start_pos = (0, 0)
        self.window_start_pos = (0, 0)

    def run_game(self):
        """Run the game."""

        print("Running the game...")
        while True:
            self._handle_events()
            if self.drag == False:
                self._update_screen()
            self.clock.tick(self.sett.screen_fps)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCREEN METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update_screen(self):
        """Update the elements of the screen each frame."""

        # Clear the screen
        self.screen.blit(self.sett.image("background"), (0, 0))

        # Update the areas
        if self.bar.visible: self.bar.update()
        if self.start.visible: self.start.update()
        if self.control.visible: self.control.update(self.game)
        if self.levels.visible: self.levels.update()
        if self.game.visible: 
            self.game.update()
            self.bubbles.update()
            self._game_status()
            if self.game_on:
                self._update_player()
            elif self.game_lost:
                self.lost.update()
            elif self.game_won:
                self.won.update()

        # Make the most recently drawn screen visible
        pg.display.flip()

    def _adjust(self):
        """Adjust the screen elements' positions after resizing."""

        # Adjust the settings
        self.sett.resize()
        self.screen = pg.display.set_mode(self.sett.screen_size, pg.NOFRAME)
        self.cursor.adjust()

        # Adjust the areas
        self.bar.adjust()
        self.start.adjust()
        self.control.adjust()
        self.levels.adjust()
        self.game.adjust()
        self.lost.adjust()
        self.won.adjust()

        # Adjust the bubbles
        for bubble in self.bubbles: bubble.adjust()
        self.player.adjust()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PLAYER LOGIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update_player(self):
        """Control the player's bubble behavior each frame."""

        if self.game_on:
            if self.game.rect.collidepoint(self.player.pos):
                self.player.update()
                if pg.sprite.spritecollideany(self.player, self.bubbles):
                    self._handle_collision()
            else:
                self._restart_player(switzerland=True)

    def _restart_player(self, switzerland=False ):
        """Restart the player's bubble at the starting position."""

        self.player = Player(self)
        self.player.recolor(self.sett.saved_color)
        self.sett.setter("saved_color", self.sett.colorize())
        self.game.switch.reload_image(f"switch_{self.sett.saved_color}")
        if switzerland: self._multiply_bubbles()

    def _switch_bubbles(self):
        """Switch the player's bubble with the saved one."""

        helper = self.player.color
        self.player.recolor(self.sett.saved_color)
        self.sett.setter("saved_color", helper)
        self.game.switch.reload_image(f"switch_{self.sett.saved_color}")

    def _handle_collision(self):
        """Handle the collisions between the bubbles and player's bubble."""

        current_color = self.player.color
        snapping_point = self._find_snapping_point()
        self._create_bubble(snapping_point, name_color=current_color)
        time.sleep(0.1)
        if self.game_on:
            self._burst_or_multiply(snapping_point)
            self._burst_lonely_bubbles()
            self._lower_max_colors()
            self._restart_player()
        else:
            self.player.kill()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUBBLE LOGIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _create_bubble(self, id_grid, id_color=None, name_color=None):
        """Create a bubble at a specified grid part."""

        # Find the bubble's position on the grid
        pos = (0, 0)
        for part in self.game.grid:
            if part.id == id_grid:
                pos = part.get_pos_by_id(id_grid)
                break
        
        # Blow up the bubble
        if id_color is not None: 
            bubble = Bubble(self, pos, id_grid, id_color=id_color)
        elif name_color is not None:
            bubble = Bubble(self, pos, id_grid, name_color=name_color)
        else:
            bubble = Bubble(self, pos, id_grid)

        # Add the bubble to the group
        self.bubbles.add(bubble)

    def _get_ids_around(self, id_grid):
        """Return the list of IDs around the specified grid element."""

        """This algorithm is based on the hexagonal grid system. It calculates
        the IDs of the elements around the specified element. The grid is
        divided into two types of rows: longer and shorter. The longer rows
        have one more element than the shorter ones. The algorithm checks the
        position of the specified element and returns the IDs of the elements
        around it. BEWARE: This specific implementation works only if the number
        of rows is even, and grid starts with the longer row."""

        # Return empty list if the grid element is out of bounds
        if id_grid == None or id_grid > len(self.game.grid) - 1 : return []

        # Set up necessary values
        I = id_grid
        # Number of rows
        R = self.game.image.get_height() // self.sett.bubble_size[1] * 6 // 5
        # Number of elements in a longer row
        L = self.game.image.get_width() // self.sett.bubble_size[0]
        # Number of elements in a shorter row
        S = self.game.image.get_width() // self.sett.bubble_size[0] - 1
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

    def _create_bubbles_around(self, id_grid):
        """Create bubbles around the specified grid element."""

        """This algorithm creates bubbles around the specified grid part.
        The bigger difficulty, the less bubbles are created around the
        specified element. The bigger luck, the bigger chance that the
        created bubbles will have the same color as the specified one."""

        # Find places around the specified grid element
        ids_around = self._get_ids_around(id_grid)

        # Remove occupied places
        occupied = []
        for bubble in self.bubbles:
            occupied.append(bubble.id_grid)
        for place in occupied: 
            if place in ids_around: ids_around.remove(place)

        # Remove places based on the difficulty
        # When the difficulty is 1, remove 4 random places
        if self.sett.level_diff == 1:
            if len(ids_around) > 4:
                for _ in range(4): 
                    ids_around.pop(randint(0, len(ids_around) - 1))
        # When the difficulty is 2, remove 3 random places
        elif self.sett.level_diff == 2:
            if len(ids_around) > 3:
                for _ in range(3): 
                    ids_around.pop(randint(0, len(ids_around) - 1))
        # When the difficulty is 3, remove 2 random places
        elif self.sett.level_diff == 3:
            if len(ids_around) > 2:
                for _ in range(2): 
                    ids_around.pop(randint(0, len(ids_around) - 1))
        # When the difficulty is 4, remove 1 random place
        elif self.sett.level_diff == 4:
            if len(ids_around) > 1:
                ids_around.pop(randint(0, len(ids_around) - 1))

        # Get the color of the bubble at the specified grid element
        for bubble in self.bubbles:
            if bubble.id_grid == id_grid:
                color = bubble.color
                break

        # Create bubbles at remaining places
        # At level luck = 5 bubbles have 80% chance of being the same color
        if self.sett.level_luck == 5:
            for place in ids_around:
                if randint(1, 10) <= 8:
                    self._create_bubble(place, name_color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 4 bubbles have 60% chance of being the same color
        elif self.sett.level_luck == 4:
            for place in ids_around:
                if randint(1, 10) <= 6:
                    self._create_bubble(place, name_color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 3 bubbles have 40% chance of being the same color
        elif self.sett.level_luck == 3:
            for place in ids_around:
                if randint(1, 10) <= 4:
                    self._create_bubble(place, name_color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 2 bubbles have 20% chance of being the same color
        elif self.sett.level_luck == 2:
            for place in ids_around:
                if randint(1, 10) <= 2:
                    self._create_bubble(place, name_color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)
        # At level luck = 1 bubbles have 10% chance of being the same color
        elif self.sett.level_luck == 1:
            for place in ids_around:
                if randint(1, 10) == 1:
                    self._create_bubble(place, name_color=color)
                    ids_around.remove(place)
                else:
                    self._create_bubble(place)

    def _multiply_bubbles(self):
        "Creates bubble around every bubble in the game."

        for bubble in self.bubbles.sprites():
            self._create_bubbles_around(bubble.id_grid)

    def _find_snapping_point(self):
        """Return ID of empty part of the grid closest to the player bubble."""
    
        # Make a list of possible snapping points
        snapping_points = []
        grid_parts = pg.sprite.spritecollide(
            self.player, self.game.grid, False)
        for part in grid_parts:
            if not self._is_occupied(part.id):
                snapping_points.append(part.id)
        
        # When there are more than one snapping point return the closest one
        if len(snapping_points) > 1:
            closest_id = self._choose_closest_id(snapping_points)
            return closest_id

        # And when there is only one snapping point return it
        elif len(snapping_points) == 1:
            return snapping_points[0]

    def _choose_closest_id(self, list_of_ids):
        """Return the ID of the closest grid part to the player bubble."""

        closest_id = None
        center = self.player.rect.center
        shortest_distance = float('inf')
        for id_ in list_of_ids:
            distance = self._calculate_distance_to_part(center, id_)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_id = id_
        return closest_id

    def _calculate_distance_to_part(self, starting_point, id_grid):
        """Return the distance between given point and grid part's center."""

        for part in self.game.grid.sprites():
            if part.id == id_grid:
                part_center = part.rect.center
                break
        return calculate_distance(starting_point, part_center)

    def _burst_or_multiply(self, id_grid):
        """Burts or multiplies bubbles based on the conditions."""

        """Bubbles burst then, and only then, when there are at least three 
        bubbles of the same color connected to each other, and they have just
        collided with player's bubble of the same color. Otherwise, every
        bubble in the game area will multiply all around."""

        cluster = self._find_cluster(id_grid)
        if len(cluster) >= 3: self._burst_cluster(cluster)
        else: self._multiply_bubbles()

    def _find_cluster(self, id_first, cluster=None):
        """Return the set of IDs of connected bubbles of the same color."""

        # Create a set to avoid duplicates
        if cluster is None:
            cluster = set()

        # Add first ID and elements around it to the set
        cluster.add(id_first)
        ids_around = self._get_ids_around(id_first)

        # Return if there are no elements around
        if ids_around is None:
            return []

        # Add same colored bubbles to the cluster, and repeat recursively
        color = self.player.color
        for id_ in ids_around:
            if id_ not in cluster:
                for bubble in self.bubbles.sprites():
                    if bubble.id_grid == id_ and bubble.color == color:
                        self._find_cluster(id_, cluster)

        
        return cluster

    def _burst_cluster(self, cluster):
        """Remove connected bubbles of the same color from the game."""

        # At least 3 bubbles need to be connected to form a cluster
        if len(cluster) > 2:
            for bubble in self.bubbles.sprites():
                if bubble.id_grid in cluster:
                    bubble.kill()

    def _burst_lonely_bubbles(self):
        """Remove bubbles that are not connected to any other bubble."""

        for bubble in self.bubbles.sprites():
            if self._is_bubble_lonely(bubble.id_grid):
                bubble.kill()

    def _is_bubble_lonely(self, id_grid):
        """Return True if the specified bubble is not connected to any other."""

        ids_around = self._get_ids_around(id_grid)
        for id_ in ids_around:
            if self._is_occupied(id_):
                return False
        return True

    def _is_occupied(self, id_grid):
        """Return True if the specified grid element is occupied."""

        for bubble in self.bubbles.sprites():
            if bubble.id_grid == id_grid:
                return True
        return False

    # ~~~~~~~~~~~~~~~~~~~~~~ EVENT HANDLING: MAIN LOGIC ~~~~~~~~~~~~~~~~~~~~~~

    def _handle_events(self):
        """Handle the events of the game."""

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
            if event.type == pg.KEYDOWN: self._handle_keydown(event)
            if event.type == pg.KEYUP: self._handle_keyup(event)
            if event.type == pg.MOUSEBUTTONDOWN: self._handle_mousedown(event)
            if event.type == pg.MOUSEBUTTONUP: self._handle_mouseup(event)
            if event.type == pg.MOUSEMOTION: self._handle_mousemotion(event)

    def _handle_mousedown(self, event):
        """Handle the mousedown events of the game."""

        if event.button == 1: # Left click

            if self.bar.visible:
                self._handle_minimize(event, "mousedown")
                self._handle_resize(event, "mousedown")
                self._handle_close(event, "mousedown")

            if self.start.visible:
                self._handle_play(event, "mousedown")
                self._handle_rules(event, "mousedown")
                self._handle_options(event, "mousedown")

            if self.control.visible:
                self._handle_back(event, "mousedown")
                self._handle_reset(event, "mousedown")     
            
            if self.levels.visible:
                self._handle_levels(event, "mousedown")

            if self.game.visible:
                if not self.player.shooting:
                    self._handle_move_left(event, "mousedown")
                    self._handle_move_right(event, "mousedown")
                    self._handle_switch(event, "mousedown")
                    if self.game.active(event.pos):
                        self._handle_shoot(event, "mousedown")

            if self.bar.active(event.pos):
                self._handle_dragging(event, "mousedown")

    def _handle_mousemotion(self, event):
        """Handle the mousemotion events of the game."""

        if self.bar.visible:
            self._handle_dragging(event, "mousemotion")

        if self.start.visible:
            self._handle_play(event, "mousemotion")
            self._handle_rules(event, "mousemotion")
            self._handle_options(event, "mousemotion")

        if self.control.visible:
            self._handle_back(event, "mousemotion")
            self._handle_reset(event, "mousemotion")

        if self.levels.visible:
            self._handle_levels(event, "mousemotion")

        if self.game.visible:
            if not self.player.shooting:
                self._handle_move_left(event, "mousemotion")
                self._handle_move_right(event, "mousemotion")
                self._handle_switch(event, "mousemotion")

    def _handle_mouseup(self, event):
        """Handle the mouseup events of the game."""

        if event.button == 1: # Left click
            self._handle_dragging(event, "mouseup")

            if self.control.visible:
                self._handle_back(event, "mouseup")
                self._handle_reset(event, "mouseup")

            if self.levels.visible:
                self._handle_levels(event, "mouseup")
            
            if self.game.visible:
                if not self.player.shooting:
                    self._handle_move_left(event, "mouseup")
                    self._handle_move_right(event, "mouseup")
                    self._handle_switch(event, "mouseup")

            if self.start.visible:
                self._handle_play(event, "mouseup")
                self._handle_rules(event, "mouseup")
                self._handle_options(event, "mouseup")

        if event.button == 3: # Right click
            if self.game.visible:
                if not self.player.shooting:
                    self._handle_switch(event, "mouseup")

    def _handle_keydown(self, event):
        """Handle the keydown events of the game."""

        if self.bar.visible:
            self._handle_close(event, "keydown")
            self._handle_resize(event, "keydown")
        
        if self.game.visible:
            self._handle_grid(event, "keydown")
            if not self.player.shooting:
                self._handle_move_left(event, "keydown")
                self._handle_move_right(event, "keydown")
                self._handle_switch(event, "keydown")


        if self.control.visible:
            self._handle_reset(event, "keydown")

    def _handle_keyup(self, event):
        """Handle the keyup events of the game."""

        if self.control.visible:
            self._handle_reset(event, "keyup")

        if self.game.visible:
            if not self.player.shooting:
                self._handle_move_left(event, "keyup")
                self._handle_move_right(event, "keyup")

    # ~~~~~~~~~~~~~~~~~~~ EVENT HANDLING: BUTTONS' METHODS ~~~~~~~~~~~~~~~~~~~
    
    def _handle_dragging(self, event, e_type):
        """Handle the dragging events of the game."""

        if e_type == "mousedown":
            # Enable dragging
            self.drag = True
            self.drag_start = event.pos
            self.window_start_pos = get_window_pos()

        if e_type == "mousemotion":
            # Handle dragging
            if self.drag:
                new_x = self.window_start_pos[0] + (
                    (event.pos[0] - self.drag_start[0]))
                new_y = self.window_start_pos[1] + (
                    (event.pos[1] - self.drag_start[1]))
                set_window_pos(new_x, new_y)

        if e_type == "mouseup":
            # Disable dragging
            self.drag = False
        
    def _handle_minimize(self, event, e_type):
        """Handle the minimize button events of the game."""

        if e_type == "mousedown":
            # Enable minimizing
            if self.bar.minimize.active(event.pos):
                pg.display.iconify()
            
    def _handle_resize(self, event, e_type):
        """Handle the resize button events of the game."""

        if e_type == "keydown":
            # Enable resizing the screen with 'f'
            if event.key == pg.K_f:
                self._adjust()

        if e_type == "mousedown":
            # Enable resizing
            if self.bar.resize.active(event.pos):
                self._adjust()

    def _handle_close(self, event, e_type):
        """Handle the close button events of the game."""

        if e_type == "keydown":
            # Enable quitting the game with 'q'
            if event.key == pg.K_q:
                sys.exit()

        if e_type == "mousedown":
            # Enable closing
            if self.bar.close.active(event.pos):
                sys.exit()

    def _handle_back(self, event, e_type):
        """Handle the back button events of the game."""

        if e_type == "mousedown":
            # Make the back button clickable
            if self.control.back.active(event.pos):
                self.control.back.click(True)

        if e_type == "mousemotion":
            # Unclick the back button if the mouse is not on it
            if not self.control.back.active(event.pos):
                self.control.back.click(False)

        if e_type == "mouseup":
            if self.control.back.active(event.pos):
                # Handle the back button in levels area
                if self.levels.visible:
                    self.control.back.click(False)
                    self.start.setter("visible", True)
                    self.control.setter("visible", False)
                    self.levels.setter("visible", False)
                # Handle the back button in game area
                elif self.game.visible:
                    self.control.back.click(False)
                    self.levels.setter("visible", True)
                    self.game.setter("visible", False)

    def _handle_play(self, event, e_type):
        """Handle the play button events of the game."""

        if e_type == "mousedown":
            # Make the play button clickable
            if self.start.play.active(event.pos):
                self.start.play.click(True)

        if e_type == "mousemotion":
            # Unclick the play button if the mouse is not on it
            if not self.start.play.active(event.pos):
                self.start.play.click(False)

        if e_type == "mouseup":

            # Handle the play button
            if self.start.play.active(event.pos):
                self.start.play.click(False)
                self.start.setter("visible", False)
                self.control.setter("visible", True)
                self.levels.setter("visible", True)

    def _handle_rules(self, event, e_type):
        """Handle the rules button events of the game."""

        if e_type == "mousedown":
            # Make the rules button clickable
            if self.start.rules.active(event.pos):
                self.start.rules.click(True)

        if e_type == "mousemotion":
            # Unclick the rules button if the mouse is not on it
            if not self.start.rules.active(event.pos):
                self.start.rules.click(False)

        if e_type == "mouseup":
            # Handle the rules button
            if self.start.rules.active(event.pos):
                self.start.rules.click(False)

    def _handle_options(self, event, e_type):
        """Handle the options button events of the game."""

        if e_type == "mousedown":
            # Make the options button clickable
            if self.start.options.active(event.pos):
                self.start.options.click(True)

        if e_type == "mousemotion":
            # Unclick the options button if the mouse is not on it
            if not self.start.options.active(event.pos):
                self.start.options.click(False)

        if e_type == "mouseup":
            # Handle the options button
            if self.start.options.active(event.pos):
                self.start.options.click(False)

    def _handle_levels(self, event, e_type):
        """Handle the levels buttons events of the game."""

        if e_type == "mousedown":
            # Make the level buttons clickable when unlocked
            for button in self.levels.buttons:
                if button.active(event.pos):
                    if not button.locked:
                        button.click(True)

        if e_type == "mousemotion":
            # Unclick the level buttons if the mouse is not on them
            for button in self.levels.buttons:
                if not button.active(event.pos):
                    button.click(False)

        if e_type == "mouseup":
            # Handle the level buttons
            for button in self.levels.buttons:
                if button.active(event.pos):
                    button.click(False)
                    self._create_level(button.level)
                    self.levels.setter("visible", False)
                    self.game.setter("visible", True)

    def _handle_grid(self, event, e_type):
        """Handle the grid visibility events of the game."""

        if e_type == "keydown":
            # Enable toggling the grid with 'ctrl + g'
            if event.key == pg.K_g and pg.key.get_mods() & pg.KMOD_CTRL:
                self.game.toggle_grid()

    def _handle_reset(self, event, e_type):
        """Handle the reset button events of the game."""

        if e_type == "keydown":
            # Enable resetting the level with 'r'
            if event.key == pg.K_r:
                self.control.reset.click(True)
                self._create_level(self.sett.level_current)

        if e_type == "keyup":
            # Unclick the reset button
            if event.key == pg.K_r:
                self.control.reset.click(False)

        if e_type == "mousedown":
            # Make the reset button clickable
            if self.control.reset.active(event.pos):
                self.control.reset.click(True)

        if e_type == "mousemotion":
            # Unclick the reset button if the mouse is not on it
            if not self.control.reset.active(event.pos):
                self.control.reset.click(False)

        if e_type == "mouseup":
            # Handle the reset button
            if self.control.reset.active(event.pos):
                self.control.reset.click(False)
                self._create_level(self.sett.level_current)

    def _handle_switch(self, event, e_type):
        """Handle the switch button events of the game."""

        if e_type == "keydown":
            # Enable switching the bubbles with 's'
            if event.key == pg.K_s:
                self._switch_bubbles()

        if e_type == "mousedown":
            # Make the switch button clickable
            if self.game.switch.active(event.pos):
                self.game.switch.click(True)

        if e_type == "mousemotion":
            # Unclick the switch button if the mouse is not on it
            if not self.game.switch.active(event.pos):
                self.game.switch.click(False)

        if e_type == "mouseup":
            # Handle the switch button
            self.game.switch.click(False)
            self._switch_bubbles()

    def _handle_move_left(self, event, e_type):
        """Handle the left movement events of the game."""

        if e_type == "keydown":
            # Enable moving left with 'left arrow' or 'a'
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.game.left.click(True)
                self.player.move("left")

        if e_type == "keyup":
            # Stop moving left
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.game.left.click(False)
                self.player.move("stop")

        if e_type == "mousedown":
            # Make the moving left button clickable
            if self.game.left.active(event.pos):
                self.game.left.click(True)
                self.player.move("left")

        if e_type == "mousemotion":
            # Unclick the moving left button if the mouse is not on it
            if not self.game.left.active(event.pos):
                self.game.left.click(False)

        if e_type == "mouseup":
            # Stop moving left
            if self.game.left.active(event.pos):
                self.game.left.click(False)
                self.player.move("stop")

    def _handle_move_right(self, event, e_type):
        """Handle the right movement events of the game."""

        if e_type == "keydown":
            # Enable moving right with 'right arrow' or 'd'
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.game.right.click(True)
                self.player.move("right")

        if e_type == "keyup":
            # Stop moving right
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.game.right.click(False)
                self.player.move("stop")

        if e_type == "mousedown":
            # Make the moving right button clickable
            if self.game.right.active(event.pos):
                self.game.right.click(True)
                self.player.move("right")

        if e_type == "mousemotion":
            # Unclick the moving right button if the mouse is not on it
            if not self.game.right.active(event.pos):
                self.game.right.click(False)

        if e_type == "mouseup":
            # Stop moving right
            if self.game.right.active(event.pos):
                self.game.right.click(False)
                self.player.move("stop")
            
    def _handle_shoot(self, event, e_type):
        """Handle the shooting events of the game."""

        if e_type == "mousedown":
            # Shoot the bubble
            if not self.player.moving_left and not self.player.moving_right:
                self.player.aim(event.pos)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LEVELS RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _game_status(self):
        """Check the game status each frame."""

        if len(self.bubbles) == 0:
            self.game_on = False
            self.game_won = True
        elif not self.player.shooting:
            for bubble in self.bubbles.sprites():
                if pg.sprite.collide_rect(self.player, bubble):
                    self.game_on = False
                    self.game_lost = True

    def _lower_max_colors(self):
        """Lower the maximum number of colors for the bubbles."""

        previous_max = self.sett.level_max_colors
        unique_colors = self._get_unique_colors()
        self.sett.setter("level_colors", unique_colors)
        self.sett.setter("level_max_colors", len(unique_colors))
        if previous_max != len(unique_colors) and self.game_on:
            self.player.recolor(self.sett.colorize())
            self.sett.setter("saved_color", self.sett.colorize())
            self.game.switch.reload_image(f"switch_{self.sett.saved_color}")

    def _get_unique_colors(self):
        """Return a list of unique colors of bubbles on the screen."""

        unique_colors = []
        for bubble in self.bubbles.sprites():
            if bubble.color not in unique_colors:
                unique_colors.append(bubble.color)
        return unique_colors

    def _set_level(self, level):
        """Change level settings for the current level."""

        self.sett.setter("level_current", level)
        self.control.level.reload_image("level")

    def _set_diff(self, level):
        """Change difficulty settings for the current level."""

        if level <= 20:
            self.sett.setter("level_diff", 1)
            self.control.diffs[0].reload_image("diff_on")
            for i in range(1, 5): self.control.diffs[i].reload_image("diff_off")
        elif level <= 40:
            self.sett.setter("level_diff", 2)
            for i in range(0, 2): self.control.diffs[i].reload_image("diff_on")
            for i in range(2, 5): self.control.diffs[i].reload_image("diff_off")
        elif level <= 60:
            self.sett.setter("level_diff", 3)
            for i in range(0, 3): self.control.diffs[i].reload_image("diff_on")
            for i in range(3, 5): self.control.diffs[i].reload_image("diff_off")
        elif level <= 80:
            self.sett.setter("level_diff", 4)
            for i in range(0, 4): self.control.diffs[i].reload_image("diff_on")
            self.control.diffs[4].reload_image("diff_off")
        else:
            self.sett.setter("level_diff", 5)
            for i in range(0, 5): self.control.diffs[i].reload_image("diff_on")

    def _set_luck(self, level):
        """Change luck settings for the current level."""

        if 5 - ((level - 1) % 20) // 4 == 5:
            self.sett.setter("level_luck", 5)
            for i in range(0, 5): self.control.lucks[i].reload_image("luck_on")
        elif 5 - ((level - 1) % 20) // 4 == 4:
            self.sett.setter("level_luck", 4)
            for i in range(0, 4): self.control.lucks[i].reload_image("luck_on")
            self.control.lucks[4].reload_image("luck_off")
        elif 5 - ((level - 1) % 20) // 4 == 3:
            self.sett.setter("level_luck", 3)
            for i in range(0, 3): self.control.lucks[i].reload_image("luck_on")
            for i in range(3, 5): self.control.lucks[i].reload_image("luck_off")
        elif 5 - ((level - 1) % 20) // 4 == 2:
            self.sett.setter("level_luck", 2)
            for i in range(0, 2): self.control.lucks[i].reload_image("luck_on")
            for i in range(2, 5): self.control.lucks[i].reload_image("luck_off")
        else:
            self.sett.setter("level_luck", 1)
            self.control.lucks[0].reload_image("luck_on")
            for i in range(1, 5): self.control.lucks[i].reload_image("luck_off")

    def _set_max_color(self, level):
        """Change the maximum number of colors for the current level."""
        
        max_colors = min(8, 3 + (level - 1) // 20)
        self.sett.setter("level_max_colors", max_colors)

    def _create_level(self, level):
        """Create a level for the game."""

        # Set up level settings
        self._set_level(level)
        self._set_diff(level)
        self._set_luck(level)
        self._set_max_color(level)
        self.sett.prepare_level()
     
        # Reset the bubbles
        self.bubbles.empty()
        self.player = Player(self)
        self.sett.setter("saved_color", self.sett.colorize())
        self.game.switch.reload_image(f"switch_{self.sett.saved_color}")

        # Dynamically create the level
        method_name = f"_create_level_{level}"
        method = getattr(self, method_name)
        if method: method()

        # Start the game
        self.game_won = False
        self.game_lost = False
        self.game_on = True

    def _create_level_1(self):
        """Create the first level of the game."""

        self._create_bubble(5, id_color=0)
        self._create_bubble(5+43, id_color=1)
        self._create_bubble(5+43*2, id_color=2)
        self._create_bubble(5+43*3, id_color=0)
        self._create_bubble(5+43*4, id_color=1)
        self._create_bubble(5+43*5, id_color=2)
        self._create_bubble(11, id_color=0)
        self._create_bubble(11+43, id_color=1)
        self._create_bubble(11+43*2, id_color=2)
        self._create_bubble(11+43*3, id_color=0)
        self._create_bubble(11+43*4, id_color=1)
        self._create_bubble(11+43*5, id_color=2)
        self._create_bubble(16, id_color=0)
        self._create_bubble(16+43, id_color=1)
        self._create_bubble(16+43*2, id_color=2)
        self._create_bubble(16+43*3, id_color=0)
        self._create_bubble(16+43*4, id_color=1)
        self._create_bubble(16+43*5, id_color=2)
        self._create_bubble(5+21, id_color=0)
        self._create_bubble(5+22, id_color=0)
        self._create_bubble(5+21+43, id_color=1)
        self._create_bubble(5+22+43, id_color=1)
        self._create_bubble(5+21+43*2, id_color=2)
        self._create_bubble(5+22+43*2, id_color=2)
        self._create_bubble(5+21+43*3, id_color=0)
        self._create_bubble(5+22+43*3, id_color=0)
        self._create_bubble(5+21+43*4, id_color=1)
        self._create_bubble(5+22+43*4, id_color=1)
        self._create_bubble(11+21, id_color=0)
        self._create_bubble(11+22, id_color=0)
        self._create_bubble(11+21+43, id_color=1)
        self._create_bubble(11+22+43, id_color=1)
        self._create_bubble(11+21+43*2, id_color=2)
        self._create_bubble(11+22+43*2, id_color=2)
        self._create_bubble(11+21+43*3, id_color=0)
        self._create_bubble(11+22+43*3, id_color=0)
        self._create_bubble(11+21+43*4, id_color=1)
        self._create_bubble(11+22+43*4, id_color=1)
        self._create_bubble(16+21, id_color=0)
        self._create_bubble(16+22, id_color=0)
        self._create_bubble(16+21+43, id_color=1)
        self._create_bubble(16+22+43, id_color=1)
        self._create_bubble(16+21+43*2, id_color=2)
        self._create_bubble(16+22+43*2, id_color=2)
        self._create_bubble(16+21+43*3, id_color=0)
        self._create_bubble(16+22+43*3, id_color=0)
        self._create_bubble(16+21+43*4, id_color=1)
        self._create_bubble(16+22+43*4, id_color=1)
        self._create_bubble(6+43*2, id_color=0)
        self._create_bubble(7+43*2, id_color=0)
        self._create_bubble(8+43*2, id_color=2)
        self._create_bubble(9+43*2, id_color=0)
        self._create_bubble(10+43*2, id_color=0)
        self._create_bubble(6+22+43*2, id_color=0)
        self._create_bubble(7+22+43*2, id_color=2)
        self._create_bubble(8+22+43*2, id_color=2)
        self._create_bubble(9+22+43*2, id_color=0)

    def _create_level_2(self):
        """Create the second level of the game."""

        self._create_bubble(0, id_color=0)

    def _create_level_3(self):
        """Create the third level of the game."""

        self._create_bubble(0, id_color=0)

    def _create_level_4(self):
        """Create the fourth level of the game."""

        self._create_bubble(0, id_color=0)

    def _create_level_5(self):
        """Create the fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_6(self):
        """Create the sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_7(self):
        """Create the seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_8(self):
        """Create the eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_9(self):
        """Create the ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_10(self):
        """Create the tenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_11(self):
        """Create the eleventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_12(self):
        """Create the twelfth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_13(self):
        """Create the thirteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_14(self):
        """Create the fourteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_15(self):
        """Create the fifteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_16(self):
        """Create the sixteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_17(self):
        """Create the seventeenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_18(self):
        """Create the eighteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_19(self):
        """Create the nineteenth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_20(self):
        """Create the twentieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_21(self):
        """Create the twenty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_22(self):
        """Create the twenty-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_23(self):
        """Create the twenty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_24(self):
        """Create the twenty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_25(self):
        """Create the twenty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_26(self):
        """Create the twenty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_27(self):
        """Create the twenty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_28(self):
        """Create the twenty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_29(self):
        """Create the twenty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_30(self):
        """Create the thirtieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_31(self):
        """Create the thirty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_32(self):
        """Create the thirty-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_33(self):
        """Create the thirty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_34(self):
        """Create the thirty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_35(self):
        """Create the thirty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_36(self):
        """Create the thirty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_37(self):
        """Create the thirty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_38(self):
        """Create the thirty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_39(self):
        """Create the thirty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_40(self):
        """Create the fortieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_41(self):
        """Create the forty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_42(self):
        """Create the forty-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_43(self):
        """Create the forty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_44(self):
        """Create the forty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_45(self):
        """Create the forty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_46(self):
        """Create the forty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_47(self):
        """Create the forty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_48(self):
        """Create the forty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_49(self):
        """Create the forty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_50(self):
        """Create the fiftieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_51(self):
        """Create the fifty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_52(self):
        """Create the fifty-second level of the game."""
        
        self._create_bubble(0, id_color=0)
        
    def _create_level_53(self):
        """Create the fifty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_54(self):
        """Create the fifty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_55(self):
        """Create the fifty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_56(self):
        """Create the fifty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_57(self):
        """Create the fifty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_58(self):
        """Create the fifty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_59(self):
        """Create the fifty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_60(self):
        """Create the sixtieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_61(self):
        """Create the sixty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_62(self):
        """Create the sixty-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_63(self):
        """Create the sixty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_64(self):
        """Create the sixty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_65(self):
        """Create the sixty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_66(self):
        """Create the sixty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_67(self):
        """Create the sixty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_68(self):
        """Create the sixty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_69(self):
        """Create the sixty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_70(self):
        """Create the seventieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_71(self):
        """Create the seventy-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_72(self):
        """Create the seventy-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_73(self):
        """Create the seventy-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_74(self):
        """Create the seventy-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_75(self):
        """Create the seventy-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_76(self):
        """Create the seventy-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_77(self):
        """Create the seventy-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_78(self):
        """Create the seventy-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_79(self):
        """Create the seventy-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_80(self):
        """Create the eightieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_81(self):
        """Create the eighty-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_82(self):
        """Create the eighty-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_83(self):
        """Create the eighty-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_84(self):
        """Create the eighty-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_85(self):
        """Create the eighty-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_86(self):
        """Create the eighty-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_87(self):
        """Create the eighty-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_88(self):
        """Create the eighty-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_89(self):
        """Create the eighty-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_90(self):
        """Create the ninetieth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_91(self):
        """Create the ninety-first level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_92(self):
        """Create the ninety-second level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_93(self):
        """Create the ninety-third level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_94(self):
        """Create the ninety-fourth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_95(self):
        """Create the ninety-fifth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_96(self):
        """Create the ninety-sixth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_97(self):
        """Create the ninety-seventh level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_98(self):
        """Create the ninety-eighth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_99(self):
        """Create the ninety-ninth level of the game."""
        
        self._create_bubble(0, id_color=0)

    def _create_level_100(self):
        """Create the one hundredth level of the game."""
        
        self._create_bubble(0, id_color=0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUN THE GAME ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    mixmi = Mixmi()
    mixmi.run_game()