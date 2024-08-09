class Button:
    """Representation of a button."""

    def __init__(self, mixmi, position, name):
        """Initialize the game's buttons."""

        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.pos = position
        self.status = False
        self.name = name
        self.image = self.load_image()

    def update(self):
        """Update the button on the screen."""

        self.screen.blit(self.image, self.pos)

    def adjust(self):
        """Adjust the button's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.load_image()

    def reload_image(self, name):
        """Reload the image after changing the button name."""

        self.name = name
        self.image = self.load_image()

    def load_image(self):
        """Load an image, acting on current click status."""

        if self.status:
            return self.sett.image(f"button_{self.name}_clicked")
        else:
            return self.sett.image(f"button_{self.name}")

    def click(self, status):
        """Change the click status of the button."""

        self.status = status
        self.image = self.load_image()

    def active(self, pos):
        """Return True if the mouse is on the button."""
    
        x_0, y_0 = self.pos
        x_1, y_1 = self.image.get_size()

        return x_0 <= pos[0] <= x_0 + x_1 and y_0 <= pos[1] <= y_0 + y_1

class LevelButton():
    """Representation of a level button."""

    def __init__(self, mixmi, position, level):
        """Initialize the game's level buttons."""
        
        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.pos = position
        self.level = level
        self.status = False
        self.locked = True
        self.image = self.load_image()

    def update(self):
        """Update the level button on the screen."""

        self.screen.blit(self.image, self.pos)

    def adjust(self):
        """Adjust the level button's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.load_image()

    def unlock(self):
        """Unlock the button."""

        self.locked = False
        self.image = self.load_image()

    def click(self, status):
        """Change the click status of the button."""

        self.status = status
        self.image = self.load_image()

    def active(self, pos):
        """Return True if the mouse is on the button."""
    
        x_0, y_0 = self.pos
        x_1, y_1 = self.image.get_size()

        return x_0 <= pos[0] <= x_0 + x_1 and y_0 <= pos[1] <= y_0 + y_1

    def load_image(self):
        """Load an image, acting on current click and locked statuses."""
            
        if self.locked:
            return self.sett.image(f"button_level_{self.level}_locked")
        elif self.status:
            return self.sett.image(f"button_level_{self.level}_clicked")
        else:
            return self.sett.image(f"button_level_{self.level}")

class Label():
    """Representation of a label."""

    def __init__(self, screen, sett, position, l_type):
        """Initialize the labels' attributes."""

        self.screen = screen
        self.sett = sett
        self.pos = position
        self.type = l_type
        self.image = self.load_image()

    def update(self):
        """Update the label on the screen."""

        self.screen.blit(self.image, self.pos)

    def adjust(self):
        """Adjust the label's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.load_image()

    def reload_image(self, l_type):
        """Reload the image after changing the label type."""

        self.type = l_type
        self.image = self.load_image()

    def load_image(self):
        """Return an image, acting on label type and value."""

        if self.type == "level":
            return self.sett.image(f"label_level_{self.sett.level_current}")
        elif self.type == "luck_on":
            return self.sett.image("label_luck")
        elif self.type == "luck_off":
            return self.sett.image("label_luck_off")
        elif self.type == "diff_on":
            return self.sett.image("label_diff")
        elif self.type == "diff_off":
            return self.sett.image("label_diff_off")
            