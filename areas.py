import pygame

def draw_rounded_rect(surface, color, rect, corner_radius):
    """Draw a rectangle with rounded corners."""

    if corner_radius > 0:
        # Draw the four corners
        pygame.draw.circle(surface, color, (rect.left + corner_radius,
                             rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius,
                              rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.left + corner_radius,
                          rect.bottom - corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius,
                           rect.bottom - corner_radius), corner_radius)

        # Draw the four edges
        pygame.draw.rect(surface, color, (rect.left + corner_radius,
              rect.top, rect.width - 2 * corner_radius, rect.height))
        pygame.draw.rect(surface, color, (rect.left,rect.top + corner_radius,
                                rect.width, rect.height - 2 * corner_radius))
    else:
        # If corner_radius is 0, just draw a rectangle
        pygame.draw.rect(surface, color, rect)

class GameArea:
    """A class to represent the game_area of the game."""

    def __init__(self, mixmi_game):
        """Initialize the game_area and set its starting position."""
        
        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Initialize the game_area's area
        self.position = (self.settings.game_x_pos, 
                         self.settings.game_y_pos)
        self.dimensions = (self.settings.game_width, 
                           self.settings.game_height)
        self.area = pygame.Rect(self.position, self.dimensions)

        # Get window's parameters from settings
        self.color = self.settings.game_color
        self.corner_radius = self.settings.corner_radius

    def draw_game_area(self):
        """Draw the game_area on the screen."""

        draw_rounded_rect(self.screen, self.color, 
                    self.area, self.corner_radius)

class LogoArea:
    """A class to represent the logo_area of the game."""

    def __init__(self, mixmi_game):
        """Initialize the logo_area and set its starting position."""
        
        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Initialize the logo_area's area
        self.position = (self.settings.logo_x_pos, 
                         self.settings.logo_y_pos)
        self.dimensions = (self.settings.logo_width, 
                           self.settings.logo_height)
        self.area = pygame.Rect(self.position, self.dimensions)

        # Load the logo from images
        self.logo = pygame.image.load('images/logo.png').convert_alpha()
        self.logo.set_alpha(240)

    def draw_logo_area(self):
        """Draw the logo_area on the screen."""

        self.screen.blit(self.logo, self.area.topleft)