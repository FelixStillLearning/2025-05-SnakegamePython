import pygame
import sys
from game_manager import GameManager
from constants import *

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pixel Snake Game - Enhanced Edition')
    clock = pygame.time.Clock()
    
    # Initialize game manager
    game_manager = GameManager(screen, clock)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)
        
        # Update game
        game_manager.update()
        
        # Draw everything
        game_manager.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(30)  # 30 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
