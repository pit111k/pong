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

    def handle_exit_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
                    self.running = False

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

    def run(self):
        """
        Run the main game loop and control the game flow via MVC pattern.
        :return: None
        """
        self.running = True

        # main game loop
        while self.running:
            self.view.fill_screen(settings.SCREEN_FILL)

            if not settings.chosen:
                self.model.menu_state.btn_single.set_hover_color(self.model.mouse_on_btn(self.model.menu_state.btn_single.rect, pygame.mouse.get_pos()))
                self.model.menu_state.btn_multi.set_hover_color(self.model.mouse_on_btn(self.model.menu_state.btn_multi.rect, pygame.mouse.get_pos()))
                self.view.render_game_mode(self.model.menu_state.btn_single, self.model.menu_state.btn_multi)
                self.handle_exit_input()
                self.view.flip()
                continue

            # process input
            self.handle_exit_input()
            self.handle_player_movement_input()

            # update game state
            winner = None

            # returns Player object if there's a winners
            if self.model.update():
                winner = self.model.check_winner()
                self.running = False

            # render changed state
            self.view.render(self.model, winner)

            if self.running is False and winner is not None:
                pygame.time.delay(settings.DELAY_AFTER_VICTORY)

            # cap framerate
            self.fps.tick(settings.FRAMERATE)
