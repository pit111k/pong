"""
Controller module for handling user input and game loop.

Classes:
    Controller: Manages the game loop and user input.
"""

from view import View
from model import Model
import pygame
import settings


class Controller:
    """
    Controller class to manage the game loop and user input.

    Attributes:
        model (Model): The game model.
        view (View): The game view.
        running (bool): Flag to control the game loop.
        fps (pygame.time.Clock): Clock to manage the frame rate.
    """

    def __init__(self, model: Model, view: View):
        """
        Initialize the Controller with model and view.
        :param model: The model class instance.
        :param view: The view class instance.
        """
        self.model = model
        self.view = view
        self.running = False
        self.fps = pygame.time.Clock()

    def handle_events(self, buttons_hovered=None):
        """
        A function to handle events like escape or mouse events.
        :param buttons_hovered: A dictionary of buttons. Button name is
        a key and a value is represented by a boolean
        :return:None
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
                    self.running = False

            if (event.type == pygame.MOUSEBUTTONUP and
                    buttons_hovered is not None):
                if (event.button == 1 and buttons_hovered["multi"] and not
                        settings.game_mode_chosen):
                    self.apply_multi_mode()
                    # print("mode: multi")
                elif (event.button == 1 and buttons_hovered["single"] and not
                        settings.game_mode_chosen):
                    self.apply_single_mode()
                    # print("mode: single")
                elif event.button == 1 and buttons_hovered["easy"]:
                    self.apply_difficulty("easy")
                    # print("diff: easy")
                elif event.button == 1 and buttons_hovered["medium"]:
                    self.apply_difficulty("medium")
                    # print("diff: medium")
                elif event.button == 1 and buttons_hovered["hard"]:
                    self.apply_difficulty("hard")
                    # print("diff: hard")

    def handle_player_movement_input(self):
        """
        Handle user input for controlling the game.
        :return: None
        """

        # get keys pressed
        keys = pygame.key.get_pressed()

        # player movement
        if keys[pygame.K_w]:
            self.model.p1.move_up()
        if keys[pygame.K_s]:
            self.model.p1.move_down()
        if settings.GAME_MODE == "multiplayer":
            if keys[pygame.K_UP]:
                self.model.p2.move_up()
            if keys[pygame.K_DOWN]:
                self.model.p2.move_down()
        else:
            self.model.p2.auto_move(self.model.ball.pos, settings.SIZE)

    def apply_difficulty(self, difficulty):
        """
        Apply the chosen difficulty setting.
        :param difficulty: string representing the chosen difficulty level.
        :return: None
        """
        settings.difficulty_chosen = True
        settings.DIFFICULTY = difficulty
        self.model.update_step()

    def apply_single_mode(self):
        """
        Apply the single player mode setting by updating the relevant settings.
        :return: None
        """
        settings.game_mode_chosen = True
        settings.GAME_MODE = "single"
        settings.AUTO = True
        self.model.p2.auto = True
        self.model.update_step()

    def apply_multi_mode(self):
        """
        Apply the multiplayer mode setting by updating the relevant settings.
        :return: None
        """
        settings.game_mode_chosen = True
        settings.GAME_MODE = "multiplayer"
        settings.AUTO = False
        self.model.update_step()
        # print(f"test, {settings.AUTO}")

    def run(self):
        """
        Run the main game loop and control the game flow via MVC pattern.
        :return: None
        """
        self.running = True

        # main game loop
        while self.running:
            self.view.fill_screen(settings.SCREEN_FILL)

            if not settings.game_mode_chosen:
                buttons_hovered = self.model.get_hovered_btns(
                    pygame.mouse.get_pos()
                )
                self.model.change_color_if_hover(buttons_hovered)

                self.view.render_game_mode(
                    self.model.menu_state.buttons["single"],
                    self.model.menu_state.buttons["multi"]
                )

                self.handle_events(buttons_hovered)
                self.view.flip()
                continue

            elif (not settings.difficulty_chosen and
                  settings.GAME_MODE == "single"):
                buttons_hovered = self.model.get_hovered_btns(
                    pygame.mouse.get_pos()
                )
                self.model.change_color_if_hover(buttons_hovered)

                self.view.render_difficulty(
                    self.model.menu_state.buttons["easy"],
                    self.model.menu_state.buttons["medium"],
                    self.model.menu_state.buttons["hard"]
                )

                self.handle_events(buttons_hovered)
                self.view.flip()
                continue

            # process input
            self.handle_events()
            self.handle_player_movement_input()

            # update game state
            winner = None

            # returns Player object if there's a winners
            if self.model.update():
                winner = self.model.check_winner()
                self.running = False

            # render changed state, winner argument is optional
            self.view.render(self.model, winner)

            if self.running is False and winner is not None:
                pygame.time.delay(settings.DELAY_AFTER_VICTORY)

            # cap framerate
            self.fps.tick(settings.FRAMERATE)
