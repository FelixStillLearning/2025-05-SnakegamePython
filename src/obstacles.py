import pygame
import random
import math
from constants import *

class Obstacle:
    def __init__(self, x, y, obstacle_type="static"):
        self.x = x
        self.y = y
        self.type = obstacle_type  # "static" or "moving"
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]) if obstacle_type == "moving" else (0, 0)
        self.move_counter = 0
        self.move_delay = 60  # Move every 2 seconds at 30 FPS
        self.animation_frame = 0
        
    def update(self, screen_width, screen_height):
        if self.type == "moving":
            self.move_counter += 1
            if self.move_counter >= self.move_delay:
                self.move_counter = 0
                
                # Try to move in current direction
                new_x = self.x + self.direction[0] * SNAKE_BLOCK
                new_y = self.y + self.direction[1] * SNAKE_BLOCK
                
                # Check boundaries and change direction if needed
                if new_x < 0 or new_x >= screen_width or new_y < 0 or new_y >= screen_height:
                    # Change direction
                    self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                else:
                    self.x = new_x
                    self.y = new_y
        
        # Update animation
        self.animation_frame = (self.animation_frame + 1) % (ANIMATION_FRAMES * 2)
    
    def get_position(self):
        return (self.x, self.y)
    
    def draw(self, screen, texture_manager=None):
        use_textures = texture_manager and texture_manager.use_textures
        
        if use_textures:
            # Use textured obstacle
            obstacle_surface = self._create_obstacle_texture()
            screen.blit(obstacle_surface, (self.x, self.y))
        else:
            # Simple colored rectangle
            color = (100, 100, 100) if self.type == "static" else (150, 100, 50)
            
            # Add pulsing effect for moving obstacles
            if self.type == "moving":
                pulse = abs(math.sin(self.animation_frame * 0.2)) * 50
                color = (min(255, color[0] + pulse), color[1], color[2])
            
            pygame.draw.rect(screen, color, (self.x, self.y, OBSTACLE_SIZE, OBSTACLE_SIZE))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, OBSTACLE_SIZE, OBSTACLE_SIZE), 2)
    
    def _create_obstacle_texture(self):
        """Create pixel art texture for obstacles"""
        surface = pygame.Surface((SNAKE_BLOCK, SNAKE_BLOCK))
        
        if self.type == "static":
            # Static obstacle - stone/brick pattern
            base_color = (80, 80, 80)
            highlight = (120, 120, 120)
            shadow = (40, 40, 40)
            
            # Fill base
            surface.fill(base_color)
            
            # Add brick pattern
            for y in range(0, SNAKE_BLOCK, 4):
                for x in range(0, SNAKE_BLOCK, 8):
                    if (y // 4) % 2 == 0:
                        pygame.draw.rect(surface, highlight, (x, y, 3, 3))
                    else:
                        pygame.draw.rect(surface, highlight, (x + 4, y, 3, 3))
            
            # Add border
            pygame.draw.rect(surface, shadow, (0, 0, SNAKE_BLOCK, SNAKE_BLOCK), 2)
            
        else:  # moving obstacle
            # Moving obstacle - crystal/energy pattern
            pulse = abs(math.sin(self.animation_frame * 0.3))
            base_r = int(100 + pulse * 50)
            base_g = int(50 + pulse * 30)
            base_b = int(150 + pulse * 80)
            
            base_color = (base_r, base_g, base_b)
            highlight = (min(255, base_r + 50), min(255, base_g + 50), min(255, base_b + 50))
            
            # Fill base
            surface.fill(base_color)
            
            # Add energy pattern
            center = SNAKE_BLOCK // 2
            for i in range(3):
                radius = center - i * 3
                if radius > 0:
                    pygame.draw.circle(surface, highlight, (center, center), radius, 1)
            
            # Add sparkle effect
            for _ in range(3):
                x = random.randint(2, SNAKE_BLOCK - 3)
                y = random.randint(2, SNAKE_BLOCK - 3)
                pygame.draw.rect(surface, (255, 255, 255), (x, y, 1, 1))
        
        return surface


class ObstacleManager:
    def __init__(self, screen_width, screen_height, game_mode=CLASSIC_MODE):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.game_mode = game_mode
        
        if game_mode == CHALLENGE_MODE:
            self._create_challenge_obstacles()
    
    def _create_challenge_obstacles(self):
        """Create predefined obstacles for challenge mode"""
        # Create some static obstacles in strategic positions
        obstacles_positions = [
            (200, 200, "static"),
            (400, 300, "static"),
            (600, 200, "static"),
            (300, 400, "moving"),
            (500, 450, "moving")
        ]
        
        for x, y, obs_type in obstacles_positions:
            if x < self.screen_width - SNAKE_BLOCK and y < self.screen_height - SNAKE_BLOCK:
                self.obstacles.append(Obstacle(x, y, obs_type))
    
    def add_random_obstacle(self, snake_positions, food_position):
        """Add a random obstacle that doesn't conflict with snake or food"""
        if len(self.obstacles) >= MAX_OBSTACLES:
            return
        
        attempts = 50  # Prevent infinite loop
        while attempts > 0:
            x = random.randint(0, (self.screen_width // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            y = random.randint(0, (self.screen_height // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            
            # Check if position conflicts with snake, food, or existing obstacles
            position = (x, y)
            if (position not in snake_positions and 
                position != food_position and
                not any(obs.get_position() == position for obs in self.obstacles)):
                
                obstacle_type = "moving" if random.random() < 0.3 else "static"
                self.obstacles.append(Obstacle(x, y, obstacle_type))
                break
            
            attempts -= 1
    
    def update(self):
        """Update all obstacles"""
        for obstacle in self.obstacles:
            obstacle.update(self.screen_width, self.screen_height)
    
    def draw(self, screen, texture_manager=None):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(screen, texture_manager)
    
    def check_collision(self, position):
        """Check if position collides with any obstacle"""
        return any(obstacle.get_position() == position for obstacle in self.obstacles)
    
    def get_obstacle_positions(self):
        """Get all obstacle positions"""
        return [obstacle.get_position() for obstacle in self.obstacles]
    
    def clear(self):
        """Clear all obstacles"""
        self.obstacles.clear()
