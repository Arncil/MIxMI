class Settings:
    """A class to store all settings for mi X mi."""
    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 1000
        self.screen_height = 800
        self.background_color = (70, 130, 70)

        # Bubble settings
        self.bubble_radius = 12.5

        # Game settings
        self.game_width = 500
        self.game_height = 750
        self.game_x_pos = 25
        self.game_y_pos = 25
        self.game_color = (70, 70, 130)
        self.corner_radius = 25

        self.color_number = 6

        # Grid settings
        self.grid_color = (70, 130, 70)