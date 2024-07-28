class Settings:
    """A class to store all settings for mi X mi."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 600
        self.screen_height = 800
        self.screen_margin = 12.5
        self.background_color = (70, 130, 70)

        # Bubble settings
        self.bubble_radius = 12.5

        # Game settings
        self.color_number = 3