import pygame

class Bubble(pygame.sprite.Sprite):
    """A representation of a single bubble."""

    def __init__(self, mixmi, position, grid_element_id=None, color=None):
        """Initialize the bubble and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()

        # Set up the basics
        self.screen = mixmi.screen
        self.settings = mixmi.settings

        # Set up the rectangle
        self.position = position
        self.size = self.settings.bubble_size
        self.rect = pygame.Rect(self.position, self.size)

        # Create placeholder for bubble's grid element ID
        self.grid_element_id = grid_element_id

        # Colorize the bubble
        if color is not None: self.color = color
        else: self.color = self.settings.get_random_color()
        self.set_image()

    def adjust(self):
        """Adjust the position after resizing the screen."""

        self.position = self.settings.adjust_position(self.position)
        self.size = self.settings.bubble_size
        self.rect = pygame.Rect(self.position, self.size)
        self.set_image()

    def update(self):
        """Update the bubble on the screen."""

        # Blit image at the position of the original Rect
        self.screen.blit(self.image, self.position)

    def set_image(self, specified_color=None):
        """Set the image of the bubble based on its color."""

        # Set the color of the bubble if specified
        if specified_color: self.color = specified_color

        # Load the image based on the color
        if self.color == "red":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_red.png')).convert_alpha()
        elif self.color == "yellow":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_yellow.png')).convert_alpha()
        elif self.color == "green":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_green.png')).convert_alpha()
        elif self.color == "blue":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_blue.png')).convert_alpha()
        elif self.color == "pink":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_pink.png')).convert_alpha()
        elif self.color == "cyan":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_cyan.png')).convert_alpha()
        elif self.color == "orange":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_orange.png')).convert_alpha()
        elif self.color == "clear":
            self.image = pygame.image.load(
                self.settings.get_image('bubble_clear.png')).convert_alpha()

class PlayerBubble(Bubble):
    """A representation of a controllable bubble."""

    def __init__(self, mixmi):
        """Initialize the player bubble and set its starting position."""

        # Define the fixed starting position
        position = (
           (mixmi.settings.screen_size[0] - mixmi.settings.bubble_size[0]) // 2,
            mixmi.game_area.position[1] + mixmi.game_area.image.get_height() - ( 
            mixmi.settings.bubble_size[1]) - 4)

        # Call the parent class's __init__() method
        super().__init__(mixmi, position)
        
        # Set the target position for current one before shooting
        self.target_position = self.position

        # Set movement flags
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_shooting = False

    def update(self):
        """Update the player bubble position based on movement flags."""

        # Update position when sliding left or right
        if self.is_moving_left or self.is_moving_right:
            self._update_on_sliding()
        # Update position when shooting
        elif self.is_shooting:
            self._update_on_shooting()

        # Blit image at the position of the original Rect
        self.screen.blit(self.image, self.position)

    def set_target_position(self, target_position):
        """Set the target position for the player bubble."""

        self.target_position = target_position

    def handle_movement(self, action):
        """Handle the movement of the player bubble depending on given action."""

        if action == "left":
            self.is_moving_left = True
            self.is_moving_right = False
        elif action == "right":
            self.is_moving_right = True
            self.is_moving_left = False
        elif action == "stop":
            self.is_moving_left = False
            self.is_moving_right = False
        elif action == "shoot":
            self.is_shooting = True

    def _update_on_sliding(self):
        """Update the player bubble as it slides left or right."""

        # Move the bubble left
        if self.is_moving_left and self.position[0] > 0 + self.size[0] * 2:
            self.position = (self.position[0] - self.settings.bubble_speed,
                                self.position[1])

        # Move the bubble right
        if self.is_moving_right and (
            self.position[0] < self.settings.screen_size[0] - self.size[0] * 3):
            self.position = (self.position[0] + self.settings.bubble_speed,
                                self.position[1])

        # Update the rectangle
        self.rect = pygame.Rect(self.position, self.size)

    def _update_on_shooting(self):
        """Update the player bubble's position after player takes a shot."""
    
        """Shooting makes the bubble travel in a straight line to the target,
        and continue moving in that direction, until it hits a wall. On hitting
        a wall, the bubble will bounce off and change its direction."""
        
        # Get the normalized direction vector
        direction = self._get_direction_vector(
            self.position, self.target_position)

        # Update the bubble's position based on the direction vector
        self._update_position_with_direction(direction)

        # Handle wall collision and change direction accordingly
        new_direction = self._handle_wall_collision(direction)

        # Update the target position based on the new direction
        self._update_target_position_with_direction(new_direction)

        # Move bubble to the new position
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
        """Update the player bubble's position based on direction vector."""

        x_pos, y_pos = self.position
        x_pos += direction_vector[0] * self.settings.bubble_speed
        y_pos += direction_vector[1] * self.settings.bubble_speed
        self.position = (x_pos, y_pos)

    def _handle_wall_collision(self, direction_vector):
        """Return the new direction of the bubble after hitting a wall."""

        # Get the direction vector components
        vector_x = direction_vector[0]
        vector_y = direction_vector[1]

        # Get game's area edges
        left_edge = self.settings.game_area_position[0]
        top_edge = self.settings.game_area_position[1]
        right_edge = self.settings.game_area_position[0] + (
            self.settings.game_area_size[0] - (self.settings.bubble_size[0]))

        # On horizontal collision, change the x of the direction vector
        if self.position[0] < left_edge or self.position[0] > right_edge:
            vector_x = -vector_x
            self.position = (
                self.position[0] + vector_x * self.settings.bubble_speed,
                self.position[1])

        # On vertical collision, change the y of the direction vector
        if self.position[1] < top_edge:
            vector_y = -vector_y
            self.position = (self.position[0],
                self.position[1] + vector_y * self.settings.bubble_speed)

        return (vector_x, vector_y)

    def _update_target_position_with_direction(self, vector):
        """Update the target position to reflect the new direction."""

        target_x_pos = self.position[0] + vector[0] * self.settings.bubble_speed
        target_y_pos = self.position[1] + vector[1] * self.settings.bubble_speed
        self.target_position = (target_x_pos, target_y_pos)

    def _update_rect(self):
        """Update the player bubble's area based on its position."""
        self.rect.x = round(self.position[0])
        self.rect.y = round(self.position[1])