"""
This module defines the global constants used throughout the Pong game.
It centralizes configuration to allow for easy game balancing and
style adjustments.

The setting are organized into following categories:
- Basic game parameters: Window dimensions and framerate
- Text controls: Color, font, and size of all text
- Objects' dimensions: Size and color of paddles and ball
- Objects' starting positions: Initial coordinates of paddles and ball
- Movement: Speed settings for ball and paddles
- Win conditions: Score required to win and delay after victory
- Game mode: Single or multiplayer settings and AI difficulty
"""

# basic game parameters
SIZE = (1600, 1200)
SCREEN_FILL = (0, 0, 0)  # black
WINDOW_TITLE = "Pong"
FRAMERATE = 60

# text controls
TEXT_COLOR = (255, 255, 255)  # white
FONT_SIZE = 50
FONT = "Poppins-Light.ttf"

# objects' dimensions
RECT_SIZE = (40, 200)
RECT_COLOR = (255, 255, 255)  # white
BALL_RADIUS = 20
BALL_COLOR = (255, 255, 255)  # white

# objects' starting positions
PLAYER1_POS = (0, 0)
PLAYER2_POS = (SIZE[0] - RECT_SIZE[0], 0)
BALL_START_POS = (SIZE[0] // 2, SIZE[1] // 2)

# movement
BALL_STEP = 5
PLAYER_STEP = 10
BALL_SPEED_INCREMENT = 5  # per vertical bounce

# win conditions
WINNING_SCORE = 2
DELAY_AFTER_VICTORY = 3000  # milliseconds

# game mode
GAME_MODE = "single"  # single or multiplayer
DIFFICULTY = "medium"  # easy, medium, hard
DIFFICULTIES = {
    "easy": 5,
    "medium": 10,
    "hard": 25
}

AUTO = False
PLAYER1_NAME = "Player 1"
PLAYER2_NAME = "Player 2"

if GAME_MODE == "single":
    PLAYER2_NAME = "Computer"
    AUTO = True
