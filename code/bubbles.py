import pygame as pg

class Bubble(pg.sprite.Sprite):
    """Representation of a bubble."""

    def __init__(self, mixmi, pos, id_grid=None, id_color=None, name_color=None):
        """Initialize the bubble."""
        
        # Set up the basics
        super().__init__()
        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.pos = pos
        self.rect = pg.Rect(self.pos, self.sett.bubble_size)

        # Set up optional attributes
        if id_grid is not None: 
            self.id_grid = id_grid
        else: 
            self.id_grid = None
        if id_color is not None:
            self.color = self.sett.colorize(id_color)
        elif name_color is not None:
            self.color = name_color
        else: 
            self.color = self.sett.colorize()

        # Blow up the bubble
        self.image = self._get_image()

    def update(self):
        """Update the bubble."""
        
        self.screen.blit(self.image, self.pos)

    def recolor(self, color):
        """Recolor the bubble."""
        
        self.color = color
        self.image = self._get_image()

    def adjust(self):
        """Adjust the bubble's position after resizing."""
        
        self.pos = self.sett.adjust(self.pos)
        self.rect = pg.Rect(self.pos, self.sett.bubble_size)
        self.image = self._get_image()

    def _get_image(self):
        """Return the bubble's image."""
        
        return self.sett.image(f"bubble_{self.color}")

class Player(Bubble):
    """Representation of the player's bubble."""
    
    def __init__(self, mixmi):
        """Initialize the player's bubble."""
        
        # Define fixed starting position
        x = (mixmi.sett.screen_size[0] - mixmi.sett.bubble_size[0]) // 2
        y = mixmi.sett.screen_size[1] - mixmi.sett.bubble_size[1] * 3
        super().__init__(mixmi, (x, y))

        # Set the target position to the starting position before shooting
        self.target_pos = self.pos

        # Set up the movement flags
        self.moving_left = False
        self.moving_right = False
        self.shooting = False

    def update(self):
        """Update the player's bubble, acting on movement flags."""

        # Update on sliding
        if self.moving_left or self.moving_right: self._slide()

        # Update on shooting
        elif self.shooting: self._shoot()

        # Update the image
        self.screen.blit(self.image, self.pos)

    def move(self, action):
        """Handle the movement of the player's bubble, acting on the action."""
            
        if action == "left":
            self.moving_left = True
            self.moving_right = False
            self.shooting = False
        elif action == "right":
            self.moving_right = True
            self.moving_left = False
            self.shooting = False
        elif action == "shoot":
            self.shooting = True
            self.moving_left = False
            self.moving_right = False
        elif action == "stop":
            self.moving_left = False
            self.moving_right = False
            self.shooting = False

    def aim(self, target_pos):
        """Set the target position for the player's bubble."""
        
        self.target_pos = target_pos
        self.shooting = True

    def recolor(self, color):
        """Recolor the player's bubble."""
        
        self.color = color
        self.image = self._get_image()

    def _slide(self):
        """Update the player's bubble as it slides left or right."""

        # Move left
        if self.moving_left and self.pos[0] > self.sett.bubble_size[0] * 2:
            self.pos = self.pos[0] - self.sett.bubble_speed, self.pos[1]

        # Move right
        if self.moving_right and self.pos[0] < self.sett.screen_size[0] - (
                                              self.sett.bubble_size[0] * 3):
            self.pos = self.pos[0] + self.sett.bubble_speed, self.pos[1]

        self.rect = pg.Rect(self.pos, self.sett.bubble_size)

    def _shoot(self):
        """Update the player's bubble position after player takes a shot."""
    
        """Shooting makes the bubble travel in a straight line to the target,
        and continue moving in that direction, until it hits a wall. On hitting
        a wall, the bubble will bounce off and change its direction."""

        direction = self._get_direction_vector(self.pos, self.target_pos)
        self._update_position_with_direction(direction)
        new_direction = self._handle_wall_collision(direction)
        self._update_target_position_with_direction(new_direction)
        self._update_rect()

    def _get_direction_vector(self, starting_position, target_position):
        """Return the normalized direction vector from two positions."""

        # Calculate the direction vector (run, rise)
        run = target_position[0] - starting_position[0]
        rise = target_position[1] - starting_position[1]
    
        # Normalize the direction vector
        distance = (run ** 2 + rise ** 2) ** 0.5
        direction_x = run / distance
        direction_y = rise / distance

        direction = (direction_x, direction_y)

        return direction

    def _update_position_with_direction(self, direction_vector):
        """Update the player's bubble position based on direction vector."""

        x_pos, y_pos = self.pos
        x_pos += direction_vector[0] * self.sett.bubble_speed
        y_pos += direction_vector[1] * self.sett.bubble_speed
        self.pos = (x_pos, y_pos)

    def _handle_wall_collision(self, direction_vector):
        """Return the new direction of the bubble after hitting a wall."""

        # Get the direction vector components
        x = direction_vector[0]
        y = direction_vector[1]

        # Get game's area edges
        left = self.sett.game_pos[0]
        top = self.sett.game_pos[1]
        right = self.sett.game_pos[0] + self.sett.game_size[0] - (
                                         self.sett.bubble_size[0])

        # On horizontal collision, change the x of the direction vector
        if self.pos[0] < left or self.pos[0] > right:
            x = -x
            self.pos = (self.pos[0] + x * self.sett.bubble_speed, self.pos[1])

        # On vertical collision, change the y of the direction vector
        if self.pos[1] < top:
            y = -y
            self.pos = (self.pos[0], self.pos[1] + y * self.sett.bubble_speed)

        return (x, y)

    def _update_target_position_with_direction(self, vector):
        """Update the target position to reflect the new direction."""

        target_x_pos = self.pos[0] + vector[0] * self.sett.bubble_speed
        target_y_pos = self.pos[1] + vector[1] * self.sett.bubble_speed
        self.target_pos = (target_x_pos, target_y_pos)

    def _update_rect(self):
        """Update the player bubble's area based on its position."""

        self.rect.x = round(self.pos[0])
        self.rect.y = round(self.pos[1])