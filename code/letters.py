import pygame

class LogoLetter:
    """A class to manage the logo letters."""

    def __init__(self, mixmi, letter_id, position):
        """Initialize the letter and its attributes."""
        
        self.screen = mixmi.screen
        self.settings = mixmi.settings
        self.letter_id = letter_id
        self.position = self.settings.adjust_position(position)
        self.image = pygame.image.load(self.settings.get_image(
                                f'logo_{self.letter_id}.png')).convert_alpha()

    def adjust(self):
        """Set the correct position after resizing the screen."""
        
        self.position = self.settings.adjust_position(self.position)

    def update(self):
        """Update the letter's position on the screen."""

        self.image = pygame.image.load(self.settings.get_image(
                                f'logo_{self.letter_id}.png')).convert_alpha()
        self.screen.blit(self.image, self.position)
