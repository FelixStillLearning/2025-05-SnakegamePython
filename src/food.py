import pygame
import random
import os
import math
from constants import *

class Food:
    def __init__(self, screen_width, screen_height, texture_manager=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = None
        self.food_type = NORMAL_FOOD
        self.special_counter = 0
        self.special_timer = 0
        self.animation_counter = 0
        self.animation_growing = True
        self.texture_manager = texture_manager
        self.rotation_angle = 0
        self.spawn()

    def spawn(self, snake_positions=None):
        # Make food spawn aligned with the snake grid (SNAKE_BLOCK)
        valid_position = False
        
        while not valid_position:
            x = random.randint(0, (self.screen_width // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            y = random.randint(0, (self.screen_height // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            new_position = (x, y)
            
            # Ensure food doesn't spawn on snake
            if snake_positions and new_position in snake_positions:
                continue
            else:
                valid_position = True
                
        self.position = new_position
        
        # Random chance for special food
        self.special_counter += 1
        
        # Every 5 regular foods, spawn a special food
        if self.special_counter >= 5:
            self.special_counter = 0
            rand_val = random.random()
            if rand_val < 0.7:  # 70% chance for special food
                self.food_type = SPECIAL_FOOD
                self.special_timer = 300  # 10 seconds at 30 FPS
            elif rand_val < 0.9:  # 20% chance for super food
                self.food_type = SUPER_FOOD
                self.special_timer = 150  # 5 seconds at 30 FPS
            else:  # 10% chance for normal food
                self.food_type = NORMAL_FOOD
        else:
            self.food_type = NORMAL_FOOD
            
        return self.position

    def update(self):
        # Update special food timer
        if self.food_type != NORMAL_FOOD:
            self.special_timer -= 1
            if self.special_timer <= 0:
                self.food_type = NORMAL_FOOD
                
        # Update animation counter
        self.animation_counter += 1
        if self.animation_counter >= ANIMATION_FRAMES:
            self.animation_counter = 0
            self.animation_growing = not self.animation_growing
            
        # Rotate food texture for animation effect
        if self.food_type != NORMAL_FOOD:
            # Special food rotates faster
            self.rotation_angle = (self.rotation_angle + (2 if self.food_type == SPECIAL_FOOD else 4)) % 360

    def get_position(self):
        return self.position
        
    def get_food_type(self):
        return self.food_type
        
    def get_points(self):
        if self.food_type == NORMAL_FOOD:
            return 10
        elif self.food_type == SPECIAL_FOOD:
            return 25
        elif self.food_type == SUPER_FOOD:
            return 50
    
    def draw(self, screen):
        use_textures = self.texture_manager and self.texture_manager.use_textures
        
        # Calculate animation size offset
        anim_offset = 0
        if self.food_type != NORMAL_FOOD:
            max_offset = 4  # Maximum size increase/decrease
            if self.animation_growing:
                anim_offset = (self.animation_counter / ANIMATION_FRAMES) * max_offset
            else:
                anim_offset = ((ANIMATION_FRAMES - self.animation_counter) / ANIMATION_FRAMES) * max_offset
                
        food_size = SNAKE_BLOCK + anim_offset
        position_offset = anim_offset / 2
        
        # Determine texture based on food type
        texture_name = None
        color = RED
        
        if self.food_type == NORMAL_FOOD:
            texture_name = 'food_normal'
            color = RED
        elif self.food_type == SPECIAL_FOOD:
            texture_name = 'food_special'
            color = PURPLE
        elif self.food_type == SUPER_FOOD:
            texture_name = 'food_super'
            color = GOLD
            
        if use_textures:
            # Use texture for food
            food_texture = self.texture_manager.get_texture(texture_name)
            if food_texture:
                # Add pixel art animation effects based on food type
                if self.food_type == SUPER_FOOD:
                    # Super food gets special rotation and pulsing effects
                    # More dramatic animation for super food
                    rotated_food = pygame.transform.rotate(food_texture, self.rotation_angle)
                    
                    # Add brightness pulsing (8-bit style)
                    pulse = int(math.sin(pygame.time.get_ticks() * 0.01) * 30)
                    pulse_surface = rotated_food.copy()
                    
                    # Apply brightness in a pixel art way (using overlay)
                    overlay = pygame.Surface(pulse_surface.get_size(), pygame.SRCALPHA)
                    if pulse > 0:
                        overlay.fill((pulse, pulse, pulse, 0))
                        pulse_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                    
                    # Scale with pixelation
                    scaled_food = pygame.transform.scale(pulse_surface, (int(food_size), int(food_size)))
                    
                    rect = scaled_food.get_rect(center=(
                        self.position[0] + SNAKE_BLOCK/2, 
                        self.position[1] + SNAKE_BLOCK/2
                    ))
                    screen.blit(scaled_food, rect)
                    
                    # Add pixel art glow effect (small individual pixels)
                    pixel_size = 2
                    for i in range(6):
                        angle = i * math.pi / 3 + pygame.time.get_ticks() * 0.005
                        distance = 4 + math.sin(pygame.time.get_ticks() * 0.01) * 2
                        px = self.position[0] + SNAKE_BLOCK/2 + math.cos(angle) * distance
                        py = self.position[1] + SNAKE_BLOCK/2 + math.sin(angle) * distance
                        
                        pygame.draw.rect(screen, YELLOW, 
                                        (px, py, pixel_size, pixel_size))
                
                elif self.food_type == SPECIAL_FOOD:
                    # Special food gets rotation and slight scaling
                    rotated_food = pygame.transform.rotate(food_texture, self.rotation_angle)
                    scaled_food = pygame.transform.scale(rotated_food, (int(food_size), int(food_size)))
                    
                    rect = scaled_food.get_rect(center=(
                        self.position[0] + SNAKE_BLOCK/2, 
                        self.position[1] + SNAKE_BLOCK/2
                    ))
                    screen.blit(scaled_food, rect)
                    
                    # Add subtle pixel art sparkle effect
                    if random.random() > 0.8:
                        pixel_size = 2
                        # Random sparkle position near the food
                        spark_x = self.position[0] + random.randint(0, SNAKE_BLOCK)
                        spark_y = self.position[1] + random.randint(0, SNAKE_BLOCK)
                        
                        pygame.draw.rect(screen, WHITE, 
                                        (spark_x, spark_y, pixel_size, pixel_size))
                
                else:
                    # Normal food has subtle pixel art bounce animation
                    bounce_offset = int(math.sin(pygame.time.get_ticks() * 0.01) * 2)
                    
                    # Add a "floating" effect
                    screen.blit(food_texture, (
                        self.position[0], 
                        self.position[1] + bounce_offset
                    ))
                    
                    # Occasionally add a shine pixel
                    if random.random() > 0.95:
                        pygame.draw.rect(screen, WHITE, (
                            self.position[0] + SNAKE_BLOCK//3, 
                            self.position[1] + SNAKE_BLOCK//3, 
                            2, 2
                        ))
            else:
                # Fallback to colored rectangle if texture not available
                pygame.draw.rect(screen, color, (
                    self.position[0] - position_offset, 
                    self.position[1] - position_offset, 
                    food_size, 
                    food_size
                ))
        else:
            # Draw food with solid color if not using textures
            pygame.draw.rect(screen, color, (
                self.position[0] - position_offset, 
                self.position[1] - position_offset, 
                food_size, 
                food_size
            ))
            
        # Draw timer for special food with pixel art style
        if self.food_type != NORMAL_FOOD:
            # Draw a pixel art timer bar above the food
            timer_width = SNAKE_BLOCK
            timer_height = 3
            timer_y = self.position[1] - 6
            timer_progress = min(1.0, self.special_timer / (300.0 if self.food_type == SPECIAL_FOOD else 150.0))
            
            # Draw pixel-by-pixel for timer background
            for x in range(0, timer_width, 2):
                pygame.draw.rect(screen, GRAY, (
                    self.position[0] + x,
                    timer_y,
                    2,
                    timer_height
                ))
            
            # Draw pixel-by-pixel for timer progress
            color = PURPLE if self.food_type == SPECIAL_FOOD else GOLD
            progress_width = int(timer_width * timer_progress)
            for x in range(0, progress_width, 2):
                pygame.draw.rect(screen, color, (
                    self.position[0] + x,
                    timer_y,
                    2,
                    timer_height
                ))