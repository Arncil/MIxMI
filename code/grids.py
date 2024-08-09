import pygame as pg

class GridPart(pg.sprite.Sprite):
    """Representation of a part of a grid."""

    # Class attribute for unique gird part IDs
    _id_counter = 0

    def __init__(self, mixmi, pos):
        """Initialize the game's grid parts."""
        
        # Set up the basics
        super().__init__()
        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.id = GridPart._id_counter
        GridPart._id_counter += 1
        self.pos = pos
        self.rect = pg.Rect(self.pos, self.sett.bubble_size)

    def update(self):
        """Update the grid part on the screen."""

        pg.draw.rect(self.screen, (237, 60, 200), self.rect, 1)

    def adjust(self):
        """Redraw the grid part after resizing the screen."""

        self.pos = self.sett.adjust(self.pos)
        self.rect = pg.Rect(self.pos, self.sett.bubble_size)

    def get_pos_by_id(self, id):
        """Return the position of a grid part by its ID."""
        
        return self.pos