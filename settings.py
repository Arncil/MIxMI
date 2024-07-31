from random import randint

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
        self.bubble_radius = self.scale_factor * 0.5 # 12.5
        self.bubble_speed = self.scale_factor * 0.3 # 

        # Game area settings
        self.game_width = self.scale_factor * 20 # 500
        self.game_height = self.scale_factor * 30 # 750
        self.game_x_pos = self.scale_factor * 1 # 25
        self.game_y_pos = self.scale_factor * 1 # 25
        self.corner_radius = self.scale_factor * 0.5 # 25
        self.game_color = (70, 70, 130)

        # Stage settings
        self.stage_color_number = 3
        self.stage_color_list = []
        self.stage_potential_bubble_colors = ("red", "yellow", "green", "blue",
                                              "pink", "cyan", "orange", "grey")

        # Logo area settings
        self.logo_width = self.scale_factor * 22 # 450
        self.logo_height = self.scale_factor * 11 # 275
        self.logo_x_pos = self.scale_factor * 21.5 # 550
        self.logo_y_pos = self.scale_factor * 1 # 25

        # Grid settings
        self.grid_color = (70, 130, 70)

    def get_random_color(self):
        """Return a random color for the bubbles."""

        if self.stage_color_number >= 1:
            # Get a random number between 0 and the color number
            random_number = randint(0, self.stage_color_number - 1)
            # Get the color based on the random number
            if random_number == 0: return "red"
            elif random_number == 1: return "yellow"
            elif random_number == 2: return "green"
            elif random_number == 3: return "blue"
            elif random_number == 4: return "pink"
            elif random_number == 5: return "cyan"
            elif random_number == 6: return "orange"
            elif random_number == 7: return "grey"

    def update_stage_color_selection(self):
        """Set stage color settings based on the stage color number."""

        # 

    def set_stage_color_list(self):
        """Set the list of colors for the stage."""
        
        self.stage_color_list = []
        for i in range(self.stage_color_number):
            self.stage_color_list.append(self.get_random_color())

    def set_stage_color_number(self, new_stage_color_number):
        """Set the number of colors for the stage."""
        
        self.stage_color_number = new_stage_color_number