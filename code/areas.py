import pygame as pg
from buttons import Button, LevelButton, Label
from letters import LogoLetter
from grids import GridPart

class Area:
    """Representation of an area of the screen."""

    def __init__(self, mixmi, visible=False):
        """Initialize the game's areas."""

        # Set up the basics
        self.screen = mixmi.screen
        self.sett = mixmi.sett
        self.visible = visible

    def setter(self, attribute, value):
        """Set the value of an attribute."""
        
        setattr(self, attribute, value)

class Bar(Area):
    """Representation of a title bar."""

    def __init__(self, mixmi):
        """Initialize the game's title bar."""

        # Set up the basics
        super().__init__(mixmi, True)
        self.image = self.sett.image("bar")

        # Set up the positions
        self.pos = (0, 0)
        self.minimize_pos = (self.pos[0] + 768, self.pos[1] + 6)
        self.resize_pos = (self.pos[0] + 800, self.pos[1] + 6)
        self.close_pos = (self.pos[0] + 832, self.pos[1] + 6)

        # Set up the buttons
        self.minimize = Button(mixmi, self.minimize_pos, "minimize")
        self.resize = Button(mixmi, self.resize_pos, "resize")
        self.close = Button(mixmi, self.close_pos, "close")

    def update(self):
        """Update the title bar on the screen."""

        self.screen.blit(self.image, self.pos)
        self.minimize.update()
        self.resize.update()
        self.close.update()

    def adjust(self):
        """Adjust the title bar's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.sett.image("bar")
        self.minimize.adjust()
        self.resize.adjust()
        self.close.adjust()

    def active(self, pos):
        """Return True if the mouse is on the title bar."""
    
        x_0, y_0 = self.pos
        x_1, y_1 = self.image.get_size()

        return x_0 <= pos[0] <= x_0 + x_1 and y_0 <= pos[1] <= y_0 + y_1

class Start(Area):
    """Representation of the start screen area."""

    def __init__(self, mixmi):
        """Initialize the game's start screen area."""

        # Set up the basics
        super().__init__(mixmi, True)
        
        # Set up the positions
        self.pos = (0, 18)
        self.m_0_pos = (self.pos[0] + 8, self.pos[1] + 60)
        self.i_0_pos = (self.pos[0] + 228, self.pos[1] + 60)
        self.x_0_pos = (self.pos[0] + 372, self.pos[1] + 120)
        self.m_1_pos = (self.pos[0] + 490, self.pos[1] + 60)
        self.i_1_pos = (self.pos[0] + 704, self.pos[1] + 60)
        self.play_pos = (self.pos[0] + 252, self.pos[1] + 360)
        self.rules_pos = (self.pos[0] + 252, self.pos[1] + 528)
        self.options_pos = (self.pos[0] + 252, self.pos[1] + 696)

        # Set up the logo letters
        self.m_0 = LogoLetter(mixmi, 0, self.m_0_pos)
        self.i_0 = LogoLetter(mixmi, 1, self.i_0_pos)
        self.x_0 = LogoLetter(mixmi, 2, self.x_0_pos)
        self.m_1 = LogoLetter(mixmi, 0, self.m_1_pos)
        self.i_1 = LogoLetter(mixmi, 1, self.i_1_pos)

        # Set up the buttons
        self.play = Button(mixmi, self.play_pos, "play")
        self.rules = Button(mixmi, self.rules_pos, "rules")
        self.options = Button(mixmi, self.options_pos, "options")

    def update(self):
        """Update the start screen area on the screen."""

        self.m_0.update()
        self.i_0.update()
        self.x_0.update()
        self.m_1.update()
        self.i_1.update()
        self.play.update()
        self.rules.update()
        self.options.update()

    def adjust(self):
        """Adjust the start screen area's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.m_0.adjust()
        self.i_0.adjust()
        self.x_0.adjust()
        self.m_1.adjust()
        self.i_1.adjust()
        self.play.adjust()
        self.rules.adjust()
        self.options.adjust()

class Control(Area):
    """Representation of the control screen area."""

    def __init__(self, mixmi):
        """Initialize the game's control screen area."""

        # Set up the basics
        super().__init__(mixmi, False)
        self.sett = mixmi.sett

        # Set up the positions
        self.pos = (0, 36)
        self.back_pos = (self.pos[0] + 8, self.pos[1] + 6)
        self.level_pos = (396, self.pos[1] + 2)
        self.reset_pos = (796, self.pos[1] + 6)
        self.diffs_pos = [(100, self.pos[1] + 12),
                          (156, self.pos[1] + 12),
                          (212, self.pos[1] + 12),
                          (268, self.pos[1] + 12),
                          (324, self.pos[1] + 12)]
        self.lucks = [(494, self.pos[1] + 12),
                      (550, self.pos[1] + 12),
                      (606, self.pos[1] + 12),
                      (662, self.pos[1] + 12),
                      (718, self.pos[1] + 12)]

        # Set up the buttons and labels
        self.back = Button(mixmi, self.back_pos, "back")
        self.reset = Button(mixmi, self.reset_pos, "reset")
        self.diffs = self._get_labels('diff')
        self.level = self._get_labels('level')
        self.lucks = self._get_labels('luck')

    def update(self, game):
        """Update the control screen area on the screen."""

        self.back.update()
        if game.visible:
            self.level.update()
            self.reset.update()
            for diff in self.diffs: diff.update()
            for luck in self.lucks: luck.update()

    def adjust(self):
        """Adjust the control screen area's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.back.adjust()
        self.level.adjust()
        self.reset.adjust()
        for diff in self.diffs: diff.adjust()
        for luck in self.lucks: luck.adjust()

    def _get_labels(self, l_type):
        """Return the labels representing the specified type."""

        if l_type == 'level':
            return Label(self.screen, self.sett, self.level_pos, l_type)
            
        labels = []
        label_attr = 'level_diff' if l_type == 'diff' else 'level_luck'
        pos_attr = 'diffs_pos' if l_type == 'diff' else 'lucks'
        label_value = getattr(self.sett, label_attr)
        pos = getattr(self, pos_attr)

        for label in range(5):
            if label <= label_value - 1:
                labels.append(Label(self.screen, self.sett, pos[label], f"{l_type}_on"))
            else:
                labels.append(Label(self.screen, self.sett, pos[label], f"{l_type}_off"))
        return labels

class Levels(Area):
    """Representation of the level screen area."""

    def __init__(self, mixmi):
        """Initialize the game's level screen area."""

        # Set up the basics
        super().__init__(mixmi, False)

        # Set up the positions
        self.pos = (72, 108)

        # Set up the buttons
        self.buttons = self._create_buttons(mixmi)

    def update(self):
        """Update the level screen area on the screen."""

        for button in self.buttons: button.update()

    def adjust(self):
        """Adjust the level screen area's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        for button in self.buttons: button.adjust()

    def _create_buttons(self, mixmi):
        """Return the list of buttons representing the levels."""

        buttons = []
        level_id = 1
        for row in range(10):
            for column in range(10):
                pos = (self.pos[0] + column * 72, self.pos[1] + row * 72)
                buttons.append(LevelButton(mixmi, pos, level_id))
                level_id += 1
        
        return buttons

class Game(Area):
    """Representation of the game screen area."""

    def __init__(self, mixmi):
        """Initialize the game's game screen area."""

        # Set up the basics
        super().__init__(mixmi, False)
        self.pos = self.sett.game_pos
        self.image = self.sett.image("game_area")
        self.rect = pg.Rect(self.pos, self.image.get_size())

        # Set the game size in the settings
        self.sett.setter("game_size", self.image.get_size())

        # Set up the grid
        self.grid = self._create_grid()
        self.grid_visible = False

        # Set up the buttons' positions
        self.left_pos = (self.pos[0] + 288, self.pos[1] + 722)
        self.switch_pos = (self.left_pos[0] + 78, self.pos[1] + 722)
        self.right_pos = (self.left_pos[0] + 144, self.pos[1] + 722)

        # Set up the buttons
        self.left = Button(mixmi, self.left_pos, "left")
        self.right = Button(mixmi, self.right_pos, "right")
        self.switch = Button(mixmi, self.switch_pos,
                            f"switch_{self.sett.saved_color}")

    def update(self):
        """Update the game area, and its elements, on the screen."""

        self.screen.blit(self.image, self.pos)
        self.left.update()
        self.switch.update()
        self.right.update()
        if self.grid_visible:
            self.grid.update()

    def adjust(self):
        """Adjust the game area's position after resizing."""

        # Adjust the game area
        self.pos = self.sett.adjust(self.pos)
        self.image = self.sett.image("game_area")
        self.rect = pg.Rect(self.pos, self.image.get_size())

        # Send info to the settings after adjusting
        self.sett.setter("game_pos", self.pos)
        self.sett.setter("game_size", self.image.get_size())

        # Adjust the buttons
        self.left.adjust()
        self.switch.adjust()
        self.right.adjust()

        # Adjust the grid
        for grid_part in self.grid:
            grid_part.adjust()

    def active(self, pos):
        """Return True if the mouse is on the game screen area."""
    
        x_0, y_0 = self.pos
        x_1, y_1 = self.image.get_size()

        return x_0 <= pos[0] <= x_0 + x_1 and y_0 <= pos[1] <= y_0 + y_1

    def colorize_switch(self):
        """Return switch button's name, acting on color."""

        return f"switch_{self.sett.color}"

        

    def toggle_grid(self):
        """Toggle the grid's visibility."""

        self.grid_visible = not self.grid_visible

    def _create_grid(self):
        """Return the Group of grid parts covering the game area."""

        grid = pg.sprite.Group()
        size = self.sett.bubble_size[0]
        row_parts = self.image.get_width() // size
        column_parts = self.image.get_height() // size * 6 // 5
        x = self.pos[0]
        y = self.pos[1]

        for row in range(column_parts):
            if row % 2 == 0:
                for part in range(row_parts):
                    grid.add(GridPart(self, (part * size + x, y)))
            else:
                for part in range(row_parts - 1):
                    grid.add(GridPart(self, (part * size + x + size // 2, y)))
            y += size * 5 // 6

        return grid 

class Lost(Area):
    """Representation of the game over screen area."""

    def __init__(self, mixmi):
        """Initialize the game's game over screen area."""
        
        super().__init__(mixmi, False)

        # Set up basics
        self.pos = (52, 252)
        self.image = self.sett.image("game_over_area")

        # Set up the buttons
        self.try_again_pos = (self.pos[0] + 30, self.pos[1] + 168)
        self.try_again = Button(mixmi, self.try_again_pos, "try_again")

    def update(self):
        """Update the game over screen area on the screen."""

        self.screen.blit(self.image, self.pos)
        self.try_again.update()

    def adjust(self):
        """Adjust the game over screen area's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.sett.image("game_over_area")
        self.try_again.adjust()

class Won(Area):
    """Representation of the winning screen area."""

    def __init__(self, mixmi):
        """Initialize the game's winning screen area."""
        
        super().__init__(mixmi, False)

        # Set up basics
        self.pos = (52, 252)
        self.image = self.sett.image("game_won_area")

        # Set up the buttons
        self.next_level_pos = (self.pos[0] + 30, self.pos[1] + 168)
        self.next_level = Button(mixmi, self.next_level_pos, "next_level")

    def update(self):
        """Update the winning screen area on the screen."""

        self.screen.blit(self.image, self.pos)
        self.next_level.update()

    def adjust(self):
        """Adjust the winning screen area's position after resizing."""

        self.pos = self.sett.adjust(self.pos)
        self.image = self.sett.image("game_won_area")
        self.next_level.adjust()