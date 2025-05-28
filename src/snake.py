import pygame
import math
import random
from constants import *

class Snake:
    def __init__(self, texture_manager=None):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = (SNAKE_BLOCK, 0)
        self.grow_flag = False
        self.last_direction = self.direction
        self.speed_boost = 0
        self.boost_timer = 0
        self.score_multiplier = 1
        self.multiplier_timer = 0
        self.eating_animation = 0
        self.head_color = YELLOW
        self.texture_manager = texture_manager
        
        # New power-up effects
        self.shrink_timer = 0
        self.slowmo_timer = 0
        self.double_score_timer = 0
        self.ghost_timer = 0
        self.death_animation = 0
        self.is_dying = False

    def move(self):
        # Save the last direction to prevent 180 degree turns
        self.last_direction = self.direction
        
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions.insert(0, new_head)
        
        # Handle shrink effect
        if self.shrink_timer > 0 and len(self.positions) > 3:
            # Remove tail segment during shrink
            self.positions.pop()
            self.positions.pop()  # Remove two segments for shrink effect
        elif not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False
            
        # Update power-up timers
        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.speed_boost = 0
                
        if self.multiplier_timer > 0:
            self.multiplier_timer -= 1
            if self.multiplier_timer <= 0:
                self.score_multiplier = 1
        
        # Update new power-up timers
        if self.shrink_timer > 0:
            self.shrink_timer -= 1
            
        if self.slowmo_timer > 0:
            self.slowmo_timer -= 1
            
        if self.double_score_timer > 0:
            self.double_score_timer -= 1
            
        if self.ghost_timer > 0:
            self.ghost_timer -= 1
                
        # Update eating animation
        if self.eating_animation > 0:
            self.eating_animation -= 1
            
        # Update death animation
        if self.death_animation > 0:
            self.death_animation -= 1
            
    def apply_powerup(self, food_type):
        if food_type == SPECIAL_FOOD:
            # Special food gives speed boost
            self.speed_boost = 1  # Reduced from 3
            self.boost_timer = 300  # 10 seconds at 30 FPS
            self.head_color = PURPLE
        elif food_type == SUPER_FOOD:
            # Super food gives score multiplier
            self.score_multiplier = 2
            self.multiplier_timer = 300  # 10 seconds at 30 FPS
            self.head_color = GOLD
        elif food_type == SHRINK_FOOD:
            # Shrink food makes snake shorter temporarily
            self.shrink_timer = SHRINK_DURATION
            self.head_color = BLUE
        elif food_type == SLOWMO_FOOD:
            # Slowmo food slows down the game
            self.slowmo_timer = SLOWMO_DURATION
            self.head_color = (0, 255, 255)  # Cyan
        elif food_type == DOUBLE_SCORE_FOOD:
            # Double score food doubles score
            self.double_score_timer = DOUBLE_SCORE_DURATION
            self.head_color = (255, 215, 0)  # Gold
        elif food_type == GHOST_FOOD:
            # Ghost food allows passing through self
            self.ghost_timer = GHOST_DURATION
            self.head_color = (200, 200, 255)  # Light blue
        
        # Start eating animation
        self.eating_animation = 15
        
    def get_score_multiplier(self):
        base_multiplier = self.score_multiplier
        if self.double_score_timer > 0:
            base_multiplier *= 2
        return base_multiplier
        
    def get_speed_boost(self):
        return self.speed_boost
    
    def is_ghost_mode(self):
        return self.ghost_timer > 0
    
    def is_slowmo_active(self):
        return self.slowmo_timer > 0
    
    def start_death_animation(self):
        self.is_dying = True
        self.death_animation = 60  # 2 seconds at 30 FPS
            
    def check_collision(self, screen_width, screen_height, obstacle_positions=None):
        # Check if snake hit the wall
        head_x, head_y = self.positions[0]
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height:
            return True
            
        # Check if snake hit obstacles
        if obstacle_positions and self.positions[0] in obstacle_positions:
            return True
            
        # Check if snake hit itself (unless in ghost mode)
        if not self.is_ghost_mode() and self.positions[0] in self.positions[1:]:
            return True
            
        return False

    def grow(self):
        self.grow_flag = True

    def reset(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = (SNAKE_BLOCK, 0)
        self.last_direction = self.direction
        self.grow_flag = False
        self.speed_boost = 0
        self.boost_timer = 0
        self.score_multiplier = 1
        self.multiplier_timer = 0
        self.eating_animation = 0
        self.head_color = YELLOW
        
        # Reset new power-up effects
        self.shrink_timer = 0
        self.slowmo_timer = 0
        self.double_score_timer = 0
        self.ghost_timer = 0
        self.death_animation = 0
        self.is_dying = False

    def get_head_position(self):
        return self.positions[0]

    def get_body_positions(self):
        return self.positions[1:]
        
    def get_all_positions(self):
        return self.positions
    
    def draw(self, screen):
        use_textures = self.texture_manager and self.texture_manager.use_textures
        
        # Death animation effect
        if self.is_dying and self.death_animation > 0:
            # Flash effect during death
            flash_intensity = self.death_animation % 10
            if flash_intensity < 5:
                # Draw with red tint
                for i, position in enumerate(self.positions):
                    if i == 0:  # Head
                        color = (255, 100, 100)  # Red head
                    else:  # Body
                        color = (200, 50, 50)   # Dark red body
                    
                    pygame.draw.rect(screen, color, (position[0], position[1], SNAKE_BLOCK, SNAKE_BLOCK))
                    
                    # Add explosion particles
                    if self.death_animation > 30:
                        for _ in range(3):
                            particle_x = position[0] + random.randint(-10, 10)
                            particle_y = position[1] + random.randint(-10, 10)
                            particle_size = random.randint(2, 4)
                            pygame.draw.rect(screen, (255, 255, 0), 
                                           (particle_x, particle_y, particle_size, particle_size))
                return
        
        # Draw body segments with pixel art style
        for i, pos in enumerate(self.positions[1:]):
            if use_textures:
                # Use texture for snake body with pixel art styling
                body_texture = self.texture_manager.get_texture('snake_body')
                if body_texture:
                    # Apply slight rotation to alternating segments for visual interest
                    if i % 2 == 0 and random.random() > 0.7:
                        # Occasionally rotate slightly for visual variety
                        angle = random.choice([-2, 2, 0])
                        rotated_body = pygame.transform.rotate(body_texture, angle)
                        rect = rotated_body.get_rect(center=(pos[0] + SNAKE_BLOCK/2, pos[1] + SNAKE_BLOCK/2))
                        screen.blit(rotated_body, rect.topleft)
                    else:
                        screen.blit(body_texture, (pos[0], pos[1]))
                else:
                    # Fallback to colored rectangle if texture not available
                    pygame.draw.rect(screen, GREEN, (pos[0], pos[1], SNAKE_BLOCK, SNAKE_BLOCK))
            else:
                pygame.draw.rect(screen, GREEN, (pos[0], pos[1], SNAKE_BLOCK, SNAKE_BLOCK))
            
        # Draw head with pixel art textures
        head = self.positions[0]
        head_size = SNAKE_BLOCK
        pos_offset = 0
        
        # Apply eating animation effect
        if self.eating_animation > 0:
            # Calculate size increase based on animation progress (bigger at start, normal at end)
            animation_progress = self.eating_animation / 15.0  # 15 is max animation frames
            size_increase = 6 * animation_progress  # max 6 pixels bigger
            head_size = SNAKE_BLOCK + size_increase
            pos_offset = size_increase / 2
        
        if use_textures:
            # Get the appropriate head texture based on direction
            if self.texture_manager:
                head_texture = self.texture_manager.get_snake_head_texture(self.direction)
                
                if head_texture:
                    # Handle eating animation scaling if needed
                    if self.eating_animation > 0:
                        # Scale up the texture for eating animation
                        bigger_head = pygame.transform.scale(head_texture, (int(head_size), int(head_size)))
                        rect = bigger_head.get_rect(center=(head[0] + SNAKE_BLOCK/2, head[1] + SNAKE_BLOCK/2))
                        screen.blit(bigger_head, rect)
                        
                        # Add "chomp" effect particles
                        if self.eating_animation > 10:
                            # Random small particles around the head
                            for _ in range(3):
                                particle_x = head[0] + random.randint(-5, SNAKE_BLOCK + 5)
                                particle_y = head[1] + random.randint(-5, SNAKE_BLOCK + 5)
                                particle_size = random.randint(2, 4)
                                
                                pygame.draw.rect(screen, YELLOW, 
                                               (particle_x, particle_y, particle_size, particle_size))
                    else:
                        # Normal drawing
                        screen.blit(head_texture, head)
                else:
                    # Fallback to colored rectangle if texture not available
                    pygame.draw.rect(screen, self.head_color, (
                        head[0] - pos_offset, 
                        head[1] - pos_offset, 
                        head_size, 
                        head_size
                    ))
        else:
            # Draw head with color
            pygame.draw.rect(screen, self.head_color, (
                head[0] - pos_offset, 
                head[1] - pos_offset, 
                head_size, 
                head_size
            ))
        
        # Draw power-up indicator if active - with pixel art style
        if self.boost_timer > 0 or self.multiplier_timer > 0:
            # Position for the indicator
            indicator_x = head[0] + SNAKE_BLOCK/2
            indicator_y = head[1] - 15
            pixel_size = 2  # Size of each "pixel" in the indicator
            
            if self.boost_timer > 0:
                # Draw speed boost indicator (lightning bolt shape) with pixel art style
                color = PURPLE
                
                # Draw individual pixels for lightning bolt shape
                # Bolt points (simplified for pixels)
                bolt_pixels = [
                    (0, 0), (1, 0), (2, 0),
                    (2, 1), (3, 1), 
                    (3, 2), (4, 2),
                    (3, 3), (2, 3),
                    (2, 4), (1, 4),
                    (1, 5), (0, 5),
                    (0, 4), (-1, 4),
                    (-1, 3), (-2, 3),
                    (-2, 2), (-1, 2),
                    (-1, 1), (0, 1)
                ]
                
                for px, py in bolt_pixels:
                    pygame.draw.rect(screen, color, 
                                   (indicator_x + px*pixel_size, indicator_y + py*pixel_size, 
                                    pixel_size, pixel_size))
                
            if self.multiplier_timer > 0:
                # Draw multiplier indicator (x2) - with pixel art style numbers
                color = GOLD
                
                # Draw "x2" using pixel by pixel approach for authentic 8-bit look
                # "x" pixels
                x_pixels = [
                    (0, 0), (2, 0),
                    (1, 1),
                    (0, 2), (2, 2)
                ]
                
                # "2" pixels
                n2_pixels = [
                    (4, 0), (5, 0), (6, 0),
                    (6, 1),
                    (4, 2), (5, 2), (6, 2),
                    (4, 3),
                    (4, 4), (5, 4), (6, 4)
                ]
                
                # Draw the x2 pixels
                for px, py in x_pixels + n2_pixels:
                    pygame.draw.rect(screen, color, 
                                   (indicator_x + px*pixel_size - 6*pixel_size, 
                                    indicator_y + py*pixel_size - 2*pixel_size, 
                                    pixel_size, pixel_size))

    def change_direction(self, direction):
        # Prevent 180 degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction