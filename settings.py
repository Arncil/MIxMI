class Settings:
    """A class to store all settings for mi X mi."""
    def __init__(self):
        """Initialize the game's settings."""

        # Scaling settings
        self.scale_factor = 25

        # Screen settings
        self.screen_width = self.scale_factor * 40 # 1000
        self.screen_height = self.scale_factor * 32 # 800
        self.background_color = (70, 130, 70)

        # Bubble settings
        self.bubble_radius = self.scale_factor / 2 #12.5

        # Game settings
        self.game_width = self.scale_factor * 20 # 500
        self.game_height = self.scale_factor * 30 # 750
        self.game_x_pos = self.scale_factor * 1 # 25
        self.game_y_pos = self.scale_factor * 1 # 25
        self.corner_radius = self.scale_factor * 1 # 25
        self.game_color = (70, 70, 130)

        self.color_number = 3

        # Grid settings
        self.grid_color = (70, 130, 70)