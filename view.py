"""
This module contains the View class responsible for rendering the game state
using Pygame.
Classes:
    View: Handles all rendering tasks for the Pong game.
"""

import pygame
import settings
from model import Model


class View:
    def __init__(self):
        """
        Initialize the Pygame view for rendering the game.
        """
        pygame.init()

        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(settings.SIZE)

        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

    def fill_screen(self, color):
        """
        Fill the screen with the specified color.
        :param color: Tuple representing the RGB color.
        :return: None
        """
        self.screen.fill(color)

    def display_score(self, player1, player2):
        """
        Display the current score of both players on the screen.
        :param player1: Player object representing player 1.
        :param player2: Player object representing player 2.
        :return: None
        """
        score_text = f"{player1.get_score()} : {player2.get_score()}"
        text_surface = self.font.render(score_text, True, settings.TEXT_COLOR)
        text_box = text_surface.get_rect()
        text_box.center = (settings.SIZE[0] // 2, settings.FONT_SIZE)
        self.screen.blit(text_surface, text_box)

    def victory_screen(self, winner):
        """
        Display the victory screen for the winning player.
        :param winner: Player object representing the winning player.
        :return: None
        """
        victory_text = f"{winner.name} Wins"
        text_surface = self.font.render(victory_text,
                                        True,
                                        settings.TEXT_COLOR)
        text_box = text_surface.get_rect()
        text_box.center = (settings.SIZE[0] // 2, settings.SIZE[1] // 2)
        self.screen.blit(text_surface, text_box)

    def render(self, model: Model, winner=None):
        """
        Render the current game state onto the screen.
        :param model: Model instance containing the game state.
        :param winner: Player object representing the winning player, if any.
        :return: None
        """
        pygame.draw.rect(self.screen,
                         model.p1.get_color(),
                         model.p1.get_dimensions())

        pygame.draw.rect(self.screen,
                         model.p2.get_color(),
                         model.p2.get_dimensions())

        pygame.draw.circle(self.screen,
                           model.ball.color,
                           model.ball.pos,
                           model.ball.radius)

        self.display_score(model.p1, model.p2)
        if winner:
            self.victory_screen(winner)

        pygame.display.flip()
