"""
Main module to run the Pong game using MVC architecture.
"""

from controller import Controller
from model import Model
from view import View


def main():
    """
    Main function to initialize and run the Pong game using MVC architecture.
    :return: None
    """
    # initialize MVC components
    model = Model()
    view = View()
    pong = Controller(model, view)

    # run the game
    pong.run()


if __name__ == "__main__":
    main()
