import pygame
from letters import LogoLetter
from buttons import Button, ButtonLevel, Label
from grids import GridElement

class Area:
    """A class to manage the screen areas."""

    def __init__(self, mixmi, status=False):
        """Initialize the areas and their attributes."""
        
        # Set up the basics
        self.screen = mixmi.screen
        self.settings = mixmi.settings
        self.is_active = status

    def toggle(self, choose=None):
        """Switch the active area."""
        
        if choose:
            self.is_active = choose
        else:
            self.is_active = not self.is_active

class BarArea(Area):
    "A class to manage the bar area of the screen."

    def __init__(self, mixmi):
        "Initialize the bar area and its attributes."

        # Call the parent class's __init__() method
        super().__init__(mixmi, True)

        # Set up the bar
        self.position = (0, 0)
        self.image = pygame.image.load(
            self.settings.get_image('bar.png')).convert_alpha()
        self.screen.blit(self.image, self.position)

        # Set up buttons' positions
        self.minimize_pos = (self.position[0] + 768, self.position[1] + 6)
        self.resize_pos = (self.position[0] + 800, self.position[1] + 6)
        self.close_pos = (self.position[0] + 832, self.position[1] + 6)

        # Set up the buttons
        self.minimize = Button(mixmi, self.minimize_pos, 'button_minimize')
        self.resize = Button(mixmi, self.resize_pos, 'button_resize')
        self.close = Button(mixmi, self.close_pos, 'button_close')

    def is_in_bar_area(self, event_pos):
        "Return True if the event is in the bar area."

        start = self.position
        end = (self.position[0] + self.image.get_width(),
               self.position[1] + self.image.get_height())

        if start[0] <= event_pos[0] <= end[0] and (
            start[1] <= event_pos[1] <= end[1]):
            return True

    def update(self):
        "Update the bar area's elements."

        # Update bar
        self.image = pygame.image.load(self.settings.get_image('bar.png'))
        self.screen.blit(self.image, self.position)
        # Update bur's elements
        self.minimize.update()
        self.resize.update()
        self.close.update()

    def adjust(self):
        "Set the correct positions after resizing the screen."

        self.position = self.settings.adjust_position(self.position)
        self.minimize.adjust()
        self.resize.adjust()
        self.close.adjust()

class ControlArea(Area):
    """A class to manage the control area of the screen."""

    def __init__(self, mixmi):
        """Initialize the control area and its attributes."""
        
        # Call the parent class's __init__() method
        super().__init__(mixmi)

        # Set up the basics
        self.settings = mixmi.settings
        self.position = (0, 36)
        self.current_level = 1
        self.difficulty = 1
        self.luck = 1

        # Set up the buttons' positions
        self.back_pos = (8, self.position[1] + 6)
        self.reset_pos = (
            self.settings.screen_size[0] - 68, self.position[1] + 6)
        self.level_pos = (
            self.settings.screen_size[0] // 2 - 34, self.position[1] + 2)
        self.diff_1_pos = (100, self.position[1] + 12)
        self.diff_2_pos = (156, self.position[1] + 12)
        self.diff_3_pos = (212, self.position[1] + 12)
        self.diff_4_pos = (268, self.position[1] + 12)
        self.diff_5_pos = (324, self.position[1] + 12)
        self.luck_1_pos = (494, self.position[1] + 12)
        self.luck_2_pos = (550, self.position[1] + 12)
        self.luck_3_pos = (606, self.position[1] + 12)
        self.luck_4_pos = (662, self.position[1] + 12)
        self.luck_5_pos = (718, self.position[1] + 12)

        # Set up the buttons
        self.back = Button(mixmi, self.back_pos, 'button_back')
        self.reset = Button(mixmi, self.reset_pos, 'button_reset')
        self.level = Label(mixmi, self.level_pos, 'level', self.current_level)
        self.diff_1 = Label(mixmi, self.diff_1_pos, "diff_on")
        self.diff_2 = Label(mixmi, self.diff_2_pos, "diff_on")
        self.diff_3 = Label(mixmi, self.diff_3_pos, "diff_on")
        self.diff_4 = Label(mixmi, self.diff_4_pos, "diff_on")
        self.diff_5 = Label(mixmi, self.diff_5_pos, "diff_on")
        self.luck_1 = Label(mixmi, self.luck_1_pos, "luck_on")
        self.luck_2 = Label(mixmi, self.luck_2_pos, "luck_on")
        self.luck_3 = Label(mixmi, self.luck_3_pos, "luck_on")
        self.luck_4 = Label(mixmi, self.luck_4_pos, "luck_on")
        self.luck_5 = Label(mixmi, self.luck_5_pos, "luck_on")

    def adjust(self):
        """Set the correct positions after resizing the screen."""
        
        # Adjust control area position
        self.position = self.settings.adjust_position(self.position)

        # Adjust buttons
        self.back.adjust()
        self.reset.adjust()
        self.level.adjust()
        self.diff_1.adjust()
        self.diff_2.adjust()
        self.diff_3.adjust()
        self.diff_4.adjust()
        self.diff_5.adjust()
        self.luck_1.adjust()
        self.luck_2.adjust()
        self.luck_3.adjust()
        self.luck_4.adjust()
        self.luck_5.adjust()

    def update(self, game_area_status, level_area_status):
        """Update the control area's elements."""
        
        # Update buttons
        self.back.update()
        if game_area_status:
            self.reset.update()
            self.level.update()
            self.diff_1.update()
            self.diff_2.update()
            self.diff_3.update()
            self.diff_4.update()
            self.diff_5.update()
            self.luck_1.update()
            self.luck_2.update()
            self.luck_3.update()
            self.luck_4.update()
            self.luck_5.update()

    def set_level(self, new_level):
        """Update the current level number."""

        self.current_level = new_level
        self.level.set_value(new_level)

    def set_difficulty(self, new_difficulty):
        """Update the current difficulty level."""

        self.difficulty = new_difficulty
        if new_difficulty == 1:
            self.diff_1.label_type = "diff_on"
            self.diff_2.label_type = "diff_off"
            self.diff_3.label_type = "diff_off"
            self.diff_4.label_type = "diff_off"
            self.diff_5.label_type = "diff_off"
        elif new_difficulty == 2:
            self.diff_1.label_type = "diff_on"
            self.diff_2.label_type = "diff_on"
            self.diff_3.label_type = "diff_off"
            self.diff_4.label_type = "diff_off"
            self.diff_5.label_type = "diff_off"
        elif new_difficulty == 3:
            self.diff_1.label_type = "diff_on"
            self.diff_2.label_type = "diff_on"
            self.diff_3.label_type = "diff_on"
            self.diff_4.label_type = "diff_off"
            self.diff_5.label_type = "diff_off"
        elif new_difficulty == 4:
            self.diff_1.label_type = "diff_on"
            self.diff_2.label_type = "diff_on"
            self.diff_3.label_type = "diff_on"
            self.diff_4.label_type = "diff_on"
            self.diff_5.label_type = "diff_off"
        elif new_difficulty == 5:
            self.diff_1.label_type = "diff_on"
            self.diff_2.label_type = "diff_on"
            self.diff_3.label_type = "diff_on"
            self.diff_4.label_type = "diff_on"
            self.diff_5.label_type = "diff_on"

    def set_luck(self, new_luck):
        """Update the current luck level."""

        self.luck = new_luck
        if new_luck == 1:
            self.luck_1.label_type = "luck_on"
            self.luck_2.label_type = "luck_off"
            self.luck_3.label_type = "luck_off"
            self.luck_4.label_type = "luck_off"
            self.luck_5.label_type = "luck_off"
        elif new_luck == 2:
            self.luck_1.label_type = "luck_on"
            self.luck_2.label_type = "luck_on"
            self.luck_3.label_type = "luck_off"
            self.luck_4.label_type = "luck_off"
            self.luck_5.label_type = "luck_off"
        elif new_luck == 3:
            self.luck_1.label_type = "luck_on"
            self.luck_2.label_type = "luck_on"
            self.luck_3.label_type = "luck_on"
            self.luck_4.label_type = "luck_off"
            self.luck_5.label_type = "luck_off"
        elif new_luck == 4:
            self.luck_1.label_type = "luck_on"
            self.luck_2.label_type = "luck_on"
            self.luck_3.label_type = "luck_on"
            self.luck_4.label_type = "luck_on"
            self.luck_5.label_type = "luck_off"
        elif new_luck == 5:
            self.luck_1.label_type = "luck_on"
            self.luck_2.label_type = "luck_on"
            self.luck_3.label_type = "luck_on"
            self.luck_4.label_type = "luck_on"
            self.luck_5.label_type = "luck_on"

class StartArea(Area):
    """A class to manage the start area of the screen."""

    def __init__(self, mixmi):
        """Initialize the start area and its attributes."""
        
        # Call the parent class's __init__() method
        super().__init__(mixmi, True)

        # Set up the basics
        self.position = (0, 18)

        # Set up logo letters
        self.m_0 = LogoLetter(mixmi, 0, (self.position[0] + 4,
                                         self.position[1] + 30))
        self.i_0 = LogoLetter(mixmi, 1, (self.position[0] + 114,
                                         self.position[1] + 30))
        self.x_0 = LogoLetter(mixmi, 2, (self.position[0] + 186,
                                         self.position[1] + 60))
        self.m_1 = LogoLetter(mixmi, 3, (self.position[0] + 249,
                                         self.position[1] + 30))
        self.i_1 = LogoLetter(mixmi, 4, (self.position[0] + 352,
                                         self.position[1] + 30))

        # Set up buttons' positions
        self.play_pos = (self.position[0] + 252, self.position[1] + 360)
        self.rules_pos = (self.position[0] + 252, self.position[1] + 528)
        self.options_pos = (self.position[0] + 252, self.position[1] + 696)

        # Set up menu buttons
        self.play = Button(mixmi, self.play_pos, 'button_play')
        self.rules = Button(mixmi, self.rules_pos, 'button_rules')
        self.options = Button(mixmi, self.options_pos, 'button_options')

    def adjust(self):
        """Set the correct positions after resizing the screen."""
        
        # Adjust bar position
        self.position = self.settings.adjust_position(self.position)

        # Adjust logo letters' positions
        self.m_0.adjust()
        self.i_0.adjust()
        self.x_0.adjust()
        self.m_1.adjust()
        self.i_1.adjust()

        # Adjust buttons' positions
        self.play.adjust()
        self.rules.adjust()
        self.options.adjust()

    def update(self):
        """Update the top area's elements."""
        
        # Update logo letters
        self.m_0.update()
        self.i_0.update()
        self.x_0.update()
        self.m_1.update()
        self.i_1.update()

        # Update buttons
        self.play.update()
        self.rules.update()
        self.options.update()

class GameArea(Area):
    """A class to manage the game area of the screen."""
    
    def __init__(self, mixmi):
        """Initialize the game area and its attributes."""
        
        # Call the parent class's __init__() method
        super().__init__(mixmi)

        # Set up the basics
        self.position = self.settings.game_area_position
        self.image = pygame.image.load(
            self.settings.get_image('game_area.png')).convert_alpha()
        self.settings.game_area_size = self.image.get_size()
        self.rect = pygame.Rect(self.position, self.settings.game_area_size)

        # Set up the grid
        self.grid = self._create_grid()
        self.show_grid = False

        # Set up the buttons' positions
        self.left_pos = (self.position[0] + 288, self.position[1] + 722)
        self.right_pos = (self.left_pos[0] + 144, self.position[1] + 722)
        self.switch_pos = (self.left_pos[0] + 78, self.position[1] + 722)

        # Set up the buttons
        self.left = Button(mixmi, self.left_pos, 'button_left')
        self.right = Button(mixmi, self.right_pos, 'button_right')
        self.switch = Button(
            mixmi, self.switch_pos, self.colorize_switch_button())

    def adjust(self):
        """Set the correct positions after resizing the screen."""
        
        # Adjust game area position and size
        self.position = self.settings.adjust_position(self.position)
        self.settings.game_area_position = self.position
        self.image = pygame.image.load(
            self.settings.get_image('game_area.png')).convert_alpha()
        self.settings.game_area_size = self.image.get_size()
        self.rect = pygame.Rect(self.position, self.settings.game_area_size)

        # Reset the grid
        self.grid = self._create_grid()

        # Adjust buttons
        self.left.adjust()
        self.right.adjust()
        self.switch.adjust()

    def update(self):
        """Update the game area's elements."""
        
        self.screen.blit(self.image, self.position)
        if self.show_grid:
            self.grid.update()
        self.left.update()
        self.right.update()
        self.switch.load_image(self.colorize_switch_button())
        self.switch.update()

    def colorize_switch_button(self):
        """Return the button name of specified bubble color."""

        if self.settings.bubble_saved == "red":
            return 'button_switch_red'
        elif self.settings.bubble_saved == "yellow":
            return 'button_switch_yellow'
        elif self.settings.bubble_saved == "green":
            return 'button_switch_green'
        elif self.settings.bubble_saved == "blue":
            return 'button_switch_blue'
        elif self.settings.bubble_saved == "pink":
            return 'button_switch_pink'
        elif self.settings.bubble_saved == "cyan":
            return 'button_switch_cyan'
        elif self.settings.bubble_saved == "orange":
            return 'button_switch_orange'
        elif self.settings.bubble_saved == "clear":
            return 'button_switch_clear'

    def is_in_game_area(self, event_pos):
        """Return True if the event is in the game area."""

        start = self.position
        end = (self.position[0] + self.image.get_width(),
               self.position[1] + self.image.get_height())

        if start[0] <= event_pos[0] <= end[0] and (
            start[1] <= event_pos[1] <= end[1]):
            return True

    def _create_grid(self):
        """Return the Group object with grid elements covering game area."""

        # Determine necessary values
        grid = pygame.sprite.Group()
        size = self.settings.bubble_size[0]
        number_per_row = self.image.get_width() // size
        number_per_column = (self.image.get_height() // size * 6 // 5)
        x = self.position[0]
        y = self.position[1]

        # Create the grid
        for row in range(number_per_column):
            # Create a row
            if row % 2 == 0:
                for element in range(number_per_row):
                    grid.add(GridElement(
                        self, (element * size + x, y)))
            # Every other row is shifted by a half of the bubble size
            else:
                for element in range(number_per_row - 1):
                    grid.add(GridElement(
                        self, (element * size + x + size // 2, y)))
            y += size * 5 // 6
        
        self.settings.set_game_area_grid_size(len(grid))
        return grid

class LevelArea(Area):
    """A class to manage the levels area of the screen."""

    def __init__(self, mixmi):
        """Initialize the levels area and its attributes."""
        
        # Call the parent class's __init__() method
        super().__init__(mixmi)

        # Set up the basics
        self.position = (self.settings.game_area_position[0] * 2,
                            self.settings.game_area_position[1])

        # Set up the buttons
        self.level_buttons = self.create_level_buttons(mixmi)

    def update(self):
        """Update the levels area's elements."""
        
        for button in self.level_buttons:
            button.update()

    def adjust(self):
        """Set the correct positions after resizing the screen."""
        
        # Adjust levels area position
        self.position = self.settings.adjust_position(self.position)

        # Adjust buttons
        for button in self.level_buttons:
            button.adjust()

    def create_level_buttons(self, mixmi):
        """Return the list of buttons representing the levels."""

        buttons = []
        level_id = 1
        for row in range(10):
            for column in range(10):
                position = (self.position[0] + column * 72,
                            self.position[1] + row * 72)
                buttons.append(ButtonLevel(mixmi, position,
                         f'button_level_{level_id}', level_id))
                level_id += 1
        
        return buttons

class GameOverArea(Area):
    """A class to manage the game over area of the screen."""

    def __init__(self, mixmi):
        """Initialize the game over area and its attributes."""
        
        # Call the parent class's __init__() method
        super().__init__(mixmi)

        # Set up the basics
        self.position = (52, 252)
        self.image = pygame.image.load(
            self.settings.get_image('game_over_area.png')).convert_alpha()

        # Set up the buttons' positions
        self.try_again_pos = (self.position[0] + 30, self.position[1] + 168)

        # Set up the buttons
        self.try_again = Button(mixmi, self.try_again_pos, 'button_try_again')
        
    def adjust(self):
        """Set the correct positions after resizing the screen."""
        
        # Adjust game over area position
        self.position = self.settings.adjust_position(self.position)

        # Adjust buttons
        self.try_again.adjust()

    def update(self):
        """Update the game over area's elements."""
        
        self.screen.blit(self.image, self.position)
        self.try_again.update()

    