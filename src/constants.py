SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_BLOCK = 20

# Game state constants
MENU = 0
GAME_RUNNING = 1
GAME_PAUSED = 2
GAME_OVER = 3

# Difficulty settings
EASY = 10   # Reduced from 3
MEDIUM = 12  # Reduced from 8
HARD = 15  # Reduced from 12

# Special food types
NORMAL_FOOD = 0
SPECIAL_FOOD = 1
SUPER_FOOD = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)

# File paths
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscores.txt")
ASSET_DIR = os.path.join(BASE_DIR, "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")

# Animation constants
ANIMATION_FRAMES = 15  # Increased from 5 to slow down animations