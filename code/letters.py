class LogoLetter:
    """Representation of a logo letter."""

    def __init__(self, mixmi, id_, position):
        """Initialize the game's logo letters."""

        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.pos = position
        self.id_ = id_
        self.image = self._load_image()

    def update(self):
        """Update the logo letter on the screen."""

        self.screen.blit(self.image, self.pos)

    def adjust(self):
        """Adjust the logo letter's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self._load_image()

    def _load_image(self):
        """Load an image, acting on current click status."""

        return self.sett.image(f"logo_{self.id_}")