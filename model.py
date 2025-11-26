"""
This module contains the Model class for
the Pong game, which manages the game state,
including players and ball positions,
movements, and collision detection.

Classes:
    Model: Represents the game state,
    including players and ball.
    Player: Represents a player in the game.
    Circ: Represents the ball in the game.
"""

from random import choice, randint
from math import cos, sin, radians
from pygame import Rect
import settings


class Model:
    """
    Model class to represent the game state, including players and ball.
    Attributes:
        p1 (Player): Player 1 object.
        p2 (Player): Player 2 object.
        ball (Circ): Ball object.
    """

    def __init__(self):
        """
        Initialize the Model with two players and a ball.
        """
        self.p1 = Player(
            settings.PLAYER1_POS,
            settings.RECT_SIZE,
            settings.RECT_COLOR,
            settings.PLAYER_STEP,
            settings.PLAYER1_NAME
        )

        # player 2 may be auto or human
        self.p2 = Player(
            settings.PLAYER2_POS,
            settings.RECT_SIZE,
            settings.RECT_COLOR,
            settings.PLAYER_STEP,
            settings.PLAYER2_NAME,
            settings.AUTO,
            settings.DIFFICULTIES[settings.DIFFICULTY]
        )

        self.ball = Circ(
            settings.BALL_RADIUS,
            settings.BALL_START_POS,
            settings.BALL_COLOR,
            settings.BALL_STEP
        )

        self.menu_state = MenuState()

    def update(self):
        """
        Update the game state: move players and ball, check for collisions,
        and update scores and check win conditions.
        :return: winner Player object if there's a winner, else None.
        """
        # returns player object if there's a winner, else None
        # players were already moved in controller
        self.p1.prevent_exceed(settings.SIZE)
        self.p2.prevent_exceed(settings.SIZE)

        # move ball
        self.update_ball_pos()

        # collision detection
        if self.ball_horizontal_wall_collision(self.ball):
            self.ball.bounce("horizontal")
        if (self.player1_collision(self.ball, self.p1) or
                self.player2_collision(self.ball, self.p2)):
            self.ball.speed_up(settings.BALL_SPEED_INCREMENT)
            self.ball.bounce("vertical")

        vertical_collision = self.ball_vertical_wall_collision(self.ball)
        # if collision is for left wall, player 2 scores, and vice versa
        if vertical_collision != 0:
            if vertical_collision == -1:
                self.p2.append_score()
            else:
                self.p1.append_score()

            winner = self.check_winner()
            # do not move the ball if there's a winner
            if winner is None:
                self.ball.start_over()

            return winner
        return None

    def update_step(self):
        """
        Update player 2's step based on the current difficulty setting.
        :return: None
        """
        if settings.AUTO:
            self.p2.step = settings.DIFFICULTIES[settings.DIFFICULTY]
        else:
            self.p2.step = settings.PLAYER_STEP

    def check_winner(self):
        """
        Check if either player has reached the winning score.
        :return: Player object if there's a winner, else None.
        """
        if self.p1.get_score() >= settings.WINNING_SCORE:
            return self.p1
        if self.p2.get_score() >= settings.WINNING_SCORE:
            return self.p2
        return None

    def update_ball_pos(self):
        """
        Update the ball's position based on its current movement.
        :return: None
        """
        self.ball.pos = (
            self.ball.pos[0] + self.ball.get_x_movement(),
            self.ball.pos[1] + self.ball.get_y_movement()
        )

    def change_color_if_hover(self, buttons):
        """
        Change each button's color based on whether it is hovered over.
        :param buttons: Dictionary with button names as keys and
                        boolean values indicating hover state.
        :return: None
        """
        for key in buttons.keys():
            self.menu_state.buttons[key].set_hover_color(
                buttons[key]
            )

    def get_hovered_btns(self, mouse_pos):
        """
        Get a dictionary indicating which buttons are hovered over
        :param mouse_pos: Tuple representing the mouse position (x, y).
        :return: Dictionary with button names as keys and
                 boolean values indicating hover state.
        """
        buttons = {}
        for key in self.menu_state.buttons.keys():
            if self.mouse_over_btn(key, mouse_pos):
                buttons[key] = True
            else:
                buttons[key] = False
        return buttons

    def mouse_over_btn(self, name, mouse_pos):
        """
        Check if the mouse is over a specific button.
        :param name: Name of the button to check
        (buttons are stored in a dictionary).
        :param mouse_pos: Tuple representing the mouse position (x, y).
        :return: Boolean indicating if the mouse is over the button.
        """
        if self.menu_state.buttons[name].rect.collidepoint(mouse_pos):
            return True
        return False

    @staticmethod
    def player1_collision(ball_obj, player):
        """
        Check for collision between ball and player 1.
        :param ball_obj: Circ object representing the ball.
        :param player: Player object representing player 1.
        :return: boolean indicating if a collision occurred.
        """
        dimensions = player.get_dimensions()
        is_within = (dimensions[1] <=
                     ball_obj.pos[1] <=
                     dimensions[1] + dimensions[3])
        is_touching = (ball_obj.pos[0] - ball_obj.radius <=
                       dimensions[2])

        return is_within and is_touching

    @staticmethod
    def player2_collision(ball_obj, player):
        """
        Check for collision between ball and player 2.
        :param ball_obj: Circ object representing the ball.
        :param player: Player object representing player 2.
        :return: boolean indicating if a collision occurred.
        """
        dimensions = player.get_dimensions()
        is_within = (dimensions[1] <=
                     ball_obj.pos[1] <=
                     dimensions[1] + dimensions[3])
        is_touching = (ball_obj.pos[0] + ball_obj.radius >=
                       dimensions[0])
        return is_within and is_touching

    @staticmethod
    def ball_horizontal_wall_collision(ball_obj):
        """
        Check for collision between ball and horizontal walls (top and bottom).
        :param ball_obj: Circ object representing the ball.
        :return: boolean indicating if a collision occurred.
        """
        return (ball_obj.pos[1] - ball_obj.radius <= 0 or
                ball_obj.pos[1] + ball_obj.radius >= settings.SIZE[1])

    @staticmethod
    def ball_vertical_wall_collision(ball_obj):
        """
        Check for collision between ball and vertical walls (left and right).
        :param ball_obj: Circ object representing the ball.
        :return: Integer indicating which wall was hit:
                    -1 for left wall, 1 for right wall, 0 for no collision.
        """
        # returns -1 for left, 0 for none, 1 for right
        if ball_obj.pos[0] - ball_obj.radius <= 0:
            return -1
        if ball_obj.pos[0] + ball_obj.radius >= settings.SIZE[0]:
            return 1
        return 0


class Player:
    """
    Player class to represent a player in the game.
    Attributes:
        rect (Rect): The rectangle (object from pygame)
        representing the player's paddle.
        color (tuple): The color of the player's paddle.
        name (str): The name of the player.
        auto (bool): Flag indicating if the player
        is controlled by AI.
        step (int): The movement step size for the player.
        score (int): The player's score.
    """
    score = 0

    def __init__(self, starting_pos, rect_size, color,
                 step, name, auto=False, difficulty_step=0):
        """
        Initialize the Player with position, size, color,
        movement step, and name.
        :param starting_pos: Player's starting position (x, y).
        :param rect_size: Size of the player's paddle (width, height).
        :param color: Color of the player's paddle (R, G, B).
        :param step: Number of pixels the player moves per action.
        :param name: Player's name.
        :param auto: Flag indicating if the player is controlled by AI.
        :param difficulty_step: Difficulty step size for AI-controlled player.
        """
        self.rect = Rect(starting_pos[0], starting_pos[1],
                         rect_size[0], rect_size[1])
        self.color = color
        self.name = name
        self.auto = auto
        if auto:
            self.step = difficulty_step
        else:
            self.step = step

    def get_dimensions(self):
        """
        Get the dimensions of the player's paddle.
        :return: Tuple representing the rectangle (x, y, width, height).
        """
        return self.rect

    def get_color(self):
        """
        Get the color of the player's paddle.
        :return: Tuple representing the color (R, G, B).
        """
        return self.color

    def move_down(self):
        """
        Move the player's paddle down by the step size.
        :return: None
        """
        self.rect = self.rect.move(0, self.step)

    def move_up(self):
        """
        Move the player's paddle up by the step size.
        :return: None
        """
        self.rect = self.rect.move(0, -self.step)

    def prevent_exceed(self, size):
        """
        Prevent player from exceeding the game window boundaries
        by adjusting the paddle position if necessary.
        :param size: Tuple representing the game window size (width, height).
        :return: None
        """
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > size[1]:
            self.rect.bottom = size[1]

    def append_score(self):
        """
        Increment the player's score by 1.
        :return: None
        """
        self.score += 1

    def get_score(self):
        """
        Get the player's current score.
        :return: Player's score (int).
        """
        return self.score

    def auto_move(self, ball_pos, size):
        """
        Automatically move the player's paddle based on the ball's position.
        :param ball_pos: Position of the ball (x, y).
        :param size: Size of the game window (width, height).
        :return: None
        """
        # only move if ball is not within paddle
        ball_within_paddle = (
                self.rect.top <= ball_pos[1] <=
                self.rect.top + self.rect.height)
        if self.auto and not ball_within_paddle:
            rect_x1 = self.rect.top
            rect_x2 = self.rect.top + self.rect.height

            is_too_low = ball_pos[1] < (rect_x1 + rect_x2) / 2
            is_too_high = ball_pos[1] > (rect_x1 + rect_x2) / 2

            next_top = self.rect.top - self.step
            next_bottom = self.rect.top + self.rect.height + self.step

            not_out_of_bounds_up = next_top >= 0
            not_out_of_bounds_down = next_bottom <= size[1]

            if is_too_low and not_out_of_bounds_up:
                self.move_up()
            elif is_too_high and not_out_of_bounds_down:
                self.move_down()


class Circ:
    """
    Circ class to represent the ball in the game.
    Attributes:
        radius (int): The radius of the ball.
        pos (tuple): The position of the ball (x, y).
        color (tuple): The color of the ball (R, G, B).
        step (int): The movement step size for the ball.
        movement (tuple): The current movement vector of the ball
        (x_movement, y_movement).
    """
    radius = color = step = 0
    pos = movement = (0, 0)

    def __init__(self, radius, pos, color, step):
        """
        Initialize the Circ with radius, position, color, and movement step.
        :param radius: Radius of the ball.
        :param pos: Starting position of the ball (x, y).
        :param color: Color of the ball (R, G, B).
        :param step: Number of pixels the ball moves per action.
        """
        self.radius = radius
        self.pos = pos
        self.color = color
        self.step = step
        self.randomize_movement()

    def bounce(self, which_wall):
        """
        Bounce the ball off a wall by inverting
        the appropriate movement component.
        :param which_wall: String indicating which
        wall was hit ("vertical" or "horizontal").
        :return: None
        """
        if which_wall == "vertical":
            self.movement = ((-1) * self.movement[0], self.movement[1])
        if which_wall == "horizontal":
            self.movement = (self.movement[0], (-1) * self.movement[1])

    def randomize_movement(self):
        """
        Randomize the ball's movement direction while avoiding steep angles
        (indicated by slope variable).
        :return: None
        """
        slope = 20

        # pick an angle that is no steeper than the slope
        ranges = [(0, 90 - slope),
                  (90 + slope, 270 - slope),
                  (270 + slope, 360)]
        angle_range = choice(ranges)
        angle = randint(angle_range[0], angle_range[1])

        # calculate x and y movement based on angle
        x = self.step * cos(radians(angle))
        y = self.step * sin(radians(angle))

        self.movement = (
            x,  # Xaxis
            (-1) * y  # Yaxis is inverted in pygame
        )

    def get_x_movement(self):
        """
        Get the ball's movement in the x direction.
        :return: Number of pixels the ball moves in the x direction.
        """
        return self.movement[0]

    def get_y_movement(self):
        """
        Get the ball's movement in the y direction.
        :return: Number of pixels the ball moves in the y direction.
        """
        return self.movement[1]

    def move_to_start(self, start_pos):
        """
        Move the ball to the starting position.
        :param start_pos: Position to move the ball to (x, y).
        :return: None
        """
        self.pos = start_pos

    def speed_up(self, increment, up=True):
        """
        Change the ball's speed by adjusting or increasing
        the step value.
        :param increment: Amount to change the step by.
        :param up: Optional parameter to indicate whether to increase (True)
                    or set (False) the step value.
        :return: None
        """
        self.movement = (
            self.movement[0] / self.step,
            self.movement[1] / self.step
        )

        if up:
            self.step += increment
        else:
            self.step = increment

        self.movement = (
            self.movement[0] * self.step,
            self.movement[1] * self.step
        )

    def set_step(self, step):
        """
        Set the ball's speed to a specific step value by
        invoking speed_up with up=False.
        :param step: Step to be set.
        :return: None
        """
        self.speed_up(step, False)

    def start_over(self):
        """
        Move the ball to the starting position, randomize its movement,
        and reset its speed to the initial step value.
        :return: None
        """
        self.move_to_start(settings.BALL_START_POS)
        self.randomize_movement()
        self.set_step(settings.BALL_STEP)


class MenuState:
    """
    Class to hold instances of menu elements.
    Attributes:
        buttons: Dictionary of Button objects.
    """
    def __init__(self):
        """
        Initialize the MenuState with buttons for game mode and
        difficulty selection. Buttons are stored in a dictionary
        with their names as keys and Button objects as values.
        Buttons:
            - "single": Button for playing singleplayer mode.
            - "multi": Button for playing multiplayer mode.
            - "easy": Button for selecting easy difficulty.
            - "medium": Button for selecting medium difficulty.
            - "hard": Button for selecting hard difficulty.
        """
        self.buttons = {
            "single": self.create_button("Singleplayer", False, 0),
            "multi": self.create_button("Multiplayer", False, 1),
            "easy": self.create_button("Easy", True, 0),
            "medium": self.create_button("Medium", True, 1),
            "hard": self.create_button("Hard", True, 2)
        }

    @staticmethod
    def create_button(text, is_difficulty, multiplier):
        """
        Create a Button object with specified text and position.
        :param text: Text to be displayed on button.
        :param is_difficulty: Boolean indicating if the
                button is for difficulty selection.
        :param multiplier: Used to calculate button position based on index.
        :return: Button object.
        """
        distance = settings.BUTTON_WIDTH + settings.DIST_BETWEEN_BUTTONS
        if is_difficulty:
            start_pos = (
                settings.DIFF_BUTTON_START_POS_X +
                distance * multiplier,
                settings.DIFF_BUTTON_START_POS_Y
            )
        else:
            start_pos = (
                settings.BUTTON_START_POS_X +
                distance * multiplier,
                settings.BUTTON_START_POS_Y
            )
        return Button(
            start_pos,
            settings.BUTTON_WIDTH,
            settings.BUTTON_HEIGHT,
            settings.BUTTON_COLOR,
            settings.BUTTON_HOVER_COLOR,
            text,
            settings.BUTTON_TEXT_COLOR,
            settings.BUTTON_FONT_SIZE
        )


class Button:
    """
    Button class to represent a clickable button in the menu.
    Attributes:
        rect (Rect): The rectangle (object from pygame)
        representing the button.
        not_hover_color (tuple): The color of the button
        when not hovered over (R, G, B).
        hover_color (tuple): The color of the button
        when hovered over (R, G, B).
        text (str): The text displayed on the button.
        text_color (tuple): The color of the button text (R, G, B).
        font_size (int): The font size of the button text.
        color (tuple): The current color of the button (R, G, B).
    """

    def __init__(self, start_pos, width, height, not_hover_color,
                 hover_color, text, text_color, font_size):
        """
        Initialize the Button with position, size, colors, text, and font size.
        :param start_pos: Starting position of the button (x, y).
        :param width: Width of the button.
        :param height: Height of the button.
        :param not_hover_color: Color displayer when not hovered over.
        :param hover_color: Color displayed when hovered over.
        :param text: Text displayed on the button.
        :param text_color: Color of the displayed text.
        :param font_size: Font size of the displayed text.
        """
        self.rect = Rect(start_pos[0], start_pos[1], width, height)
        self.not_hover_color = not_hover_color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.color = not_hover_color

    def get_dimensions(self):
        """
        Get the dimensions of the button.
        :return: pygame Rect object representing button's dimensions.
        """
        return self.rect

    def get_center(self):
        """
        Get the center position of the button.
        :return: pygame Rect center variable (x, y).
        """
        return self.rect.center

    def set_hover_color(self, is_hover):
        """
        Set the button's color based on hover state.
        :param is_hover: Boolean indicating whether the button is hovered over.
        :return: None
        """
        if is_hover:
            self.color = self.hover_color
        else:
            self.color = self.not_hover_color
