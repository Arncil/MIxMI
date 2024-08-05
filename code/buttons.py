import pygame

class Button:
    """A class to manage buttons."""

    def __init__(self, mixmi, position, image_name):
        """Initialize the button and its attributes."""

        self.screen = mixmi.screen
        self.settings = mixmi.settings
        self.position = position
        self.image_name = image_name
        self.is_clicked = False
        self.image = None

    def is_in_button_area(self, event_pos):
        """Return True if the event is in the button area."""
        if not self.image:
            return False

        start_x, start_y = self.position
        end_x = start_x + self.image.get_width()
        end_y = start_y + self.image.get_height()

        return start_x <= event_pos[0] <= end_x and start_y <= event_pos[1] <= end_y

    def update(self):
        """Update the button's position on the screen."""

        self.load_image()
        self.screen.blit(self.image, self.position)

    def adjust(self):
        """Set the correct position after resizing the screen."""

        self.position = self.settings.adjust_position(self.position)

    def load_image(self, specified_name=None):
        """Load the button's image."""

        if specified_name:
            self.image_name = specified_name

        if self.is_clicked:
            self.image = pygame.image.load(self.settings.get_image(
                        f"{self.image_name}_clicked.png")).convert_alpha()
        else:
            self.image = pygame.image.load(self.settings.get_image(
                        f"{self.image_name}.png")).convert_alpha()
        
    def click(self):
        """Switch the button's is_clicked attribute."""

        self.is_clicked = not self.is_clicked

class ButtonLevel(Button):
    """A class to manage level buttons."""

    def __init__(self, mixmi, position, image_name, level):
        """Initialize the level button and its attributes."""

        # Call the parent class constructor
        super().__init__(mixmi, position, "button_level")

        # Set up the basics
        self.level = level
        self.is_locked = True

    def update(self):
        """Update the level button's position on the screen."""

        if self.is_locked:
            self.load_image(f"button_level_{self.level}_locked")
        else:
            self.load_image(f"button_level_{self.level}")

        self.load_image()
        self.screen.blit(self.image, self.position)

    def unlock(self):
        """Unlock the level button."""

        self.is_locked = False