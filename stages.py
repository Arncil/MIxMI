from random import randint

class Stage:
    """A class to represent a level in the game."""

    def __init__(self, mixmi_game, color_number):
        """Initialize the stage and set its starting settings."""

        # Get the main window and settings
        self.screen = mixmi_game.screen
        self.settings = mixmi_game.settings

        # Initialize the stage attributes
        self.color_number = color_number
        self.color_list = _get_colors_list()

    def get_unique_bubble_colors(self):
        """Return the list of unique bubble colors in the game area."""
            
        # Create a set to store unique colors
        unique_colors = set()

        # Check the color of each bubble in the game area
        for bubble in mixmi_game.bubbles.sprites():
            unique_colors.add(bubble.color)

        # Return the set of unique colors
        return unique_colors

    def _get_colors_list(self):
        """Return a list of colors for the stage based on the color number."""

        # Create a list to store the colors
        new_color_list = []

        # Get a copy of the potential bubble colors list
        potential_colors = self.settings.stage_potential_bubble_colors[:]

        # Add the colors to the list
        for color in range(self.color_number):
            # Randomly select a color from the potential colors
            random_color = potential_colors.pop(randint(0, len(potential_colors) - 1))
            new_color_list.append(random_color)

        # Return the list of colors
        return new_color_list
