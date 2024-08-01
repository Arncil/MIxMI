import pygame
from settings import Settings

class Bubble(pygame.sprite.Sprite):
    """A representation of a single bubble."""
    
    def __init__(self, mixmi_game, x_pos, y_pos):
        """Initialize the bubble and set its starting position."""

        # Call the parent class's __init__() method
        super().__init__()

        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Set the bubble's starting position
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Initialize the bubble's area
        self.position = (self.x_pos, self.y_pos)
        self.dimensions = (self.settings.bubble_radius * 2, 
                           self.settings.bubble_radius * 2)
        self.rect = pygame.Rect(self.position, self.dimensions)

        # Set the bubble's rotation
        self.rotation = 0

        # Colorize the bubble
        self.color = self.settings.get_random_color()
        self.set_image()

        # Create placeholder for bubble's grid element ID
        self.grid_element_id = None

    def draw(self):
        """Draw the bubble on the screen."""

        # Blit the scaled image at the position of the original Rect
        self.screen.blit(self.image, self.rect.topleft)



    def set_image(self, specified_color=None):
        """Set the color of the bubble."""

        # Set the color of the bubble if specified
        if specified_color: self.color = specified_color

        # Load the image based on the color
        if self.color == "red":
            self.image = pygame.image.load(
                'images/bubble_red.png').convert_alpha()
        elif self.color == "yellow":
            self.image = pygame.image.load(
                'images/bubble_yellow.png').convert_alpha()
        elif self.color == "green":
            self.image = pygame.image.load(
                'images/bubble_green.png').convert_alpha()
        elif self.color == "blue":
            self.image = pygame.image.load(
                'images/bubble_blue.png').convert_alpha()
        elif self.color == "pink":
            self.image = pygame.image.load(
                'images/bubble_pink.png').convert_alpha()
        elif self.color == "cyan":
            self.image = pygame.image.load(
                'images/bubble_cyan.png').convert_alpha()
        elif self.color == "orange":
            self.image = pygame.image.load(
                'images/bubble_orange.png').convert_alpha()
        elif self.color == "grey":
            self.image = pygame.image.load(
                'images/bubble_grey.png').convert_alpha()
        
        # Set transparency
        self.image.set_alpha(200)

    def set_grid_element_id(self, grid_element_id):
        """Set the grid element ID of the bubble."""

        self.grid_element_id = grid_element_id

class PlayerBubble(Bubble):
    """A representation of a controllable bubble."""

    def __init__(self, mixmi_game):
        """Initialize the player bubble and set its starting position."""

        # Define the fixed starting position
        x_pos = mixmi_game.settings.bubble_radius * 21
        y_pos = mixmi_game.settings.bubble_radius * 60

        # Call the parent class's __init__() method
        super().__init__(mixmi_game, x_pos, y_pos)

        # Set the target position for current position before shooting
        self.target_x_pos = self.x_pos
        self.target_y_pos = self.y_pos

        # Set movement flags
        self.moving_left = False
        self.moving_right = False
        self.shooting = False

    def update(self):
            """Update the player bubble's position based on movement flags."""
            
            # Update position when sliding left or right
            if not self.shooting and (self.moving_left or self.moving_right):
                self.update_position_on_sliding()

            # Update position when shooting
            if self.shooting:
                self.update_position_on_shooting()

    def set_target_position(self, new_target_position):
        """Set the target position for the player bubble."""

        self.target_x_pos = new_target_position[0]
        self.target_y_pos = new_target_position[1]

    def update_position_on_sliding(self):
        """Update the player bubble's position as it slides left or right."""

        # Update position as it slides left
        if self.moving_left and self.rect.left > self.settings.game_x_pos + ( 
                                             self.settings.bubble_radius * 2):
            self.x_pos -= self.settings.bubble_speed
            self.target_x_pos -= self.settings.bubble_speed

        # Update position as it slides right
        if self.moving_right and self.rect.right < self.settings.game_x_pos + (
                    self.settings.game_width - self.settings.bubble_radius * 2):
            self.x_pos += self.settings.bubble_speed
            self.target_x_pos += self.settings.bubble_speed

        # Move the bubble's area
        self.rect.x = int(self.x_pos)

    def update_position_on_shooting(self):
        """Update the player bubble's position after player takes a shot."""
    
        """Shooting makes the bubble travel in a straight line to the target,
        and continue moving in that direction, until it hits a wall. On hitting
        a wall, the bubble will bounce off and change its direction."""
        
        # Get the normalized direction vector
        direction = self._get_direction_vector(
            [self.x_pos, self.y_pos], [self.target_x_pos, self.target_y_pos])

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

        self.x_pos += direction_vector[0] * self.settings.bubble_speed
        self.y_pos += direction_vector[1] * self.settings.bubble_speed

    def _handle_wall_collision(self, direction_vector):
        """Return the new direction of the bubble after hitting a wall."""

        # Get the direction vector components
        vector_x = direction_vector[0]
        vector_y = direction_vector[1]

        # Get game's area edges
        top_edge = self.settings.game_y_pos
        left_edge = self.settings.game_x_pos
        right_edge = self.settings.game_x_pos + self.settings.game_width - (
                                            self.settings.bubble_radius * 2)

        # On horizontal collision, change the x of the direction vector
        if self.x_pos < left_edge or self.x_pos > right_edge:
            vector_x = -vector_x
            self.x_pos += vector_x * self.settings.bubble_speed

        # On vertical collision, change the y of the direction vector
        if self.y_pos < top_edge:
            vector_y = -vector_y
            self.y_pos += vector_y * self.settings.bubble_speed

        return (vector_x, vector_y)

    def _update_target_position_with_direction(self, vector):
        """Update the target position to reflect the new direction."""

        speed = self.settings.bubble_speed
        self.target_x_pos = self.x_pos + vector[0] * speed
        self.target_y_pos = self.y_pos + vector[1] * speed

    def _update_rect(self):
        """Update the player bubble's area based on its position."""
        self.rect.x = round(self.x_pos)
        self.rect.y = round(self.y_pos)