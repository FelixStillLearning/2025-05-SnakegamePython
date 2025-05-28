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
        self.spawn_animation = 0  # Animation when food appears
        self.spawn_particles = []  # Particles when food spawns
        self.spawn()

    def spawn(self, snake_positions=None, obstacle_positions=None):
        # Make food spawn aligned with the snake grid (SNAKE_BLOCK)
        valid_position = False
        
        while not valid_position:
            x = random.randint(0, (self.screen_width // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            y = random.randint(0, (self.screen_height // SNAKE_BLOCK) - 1) * SNAKE_BLOCK
            new_position = (x, y)
            
            # Ensure food doesn't spawn on snake or obstacles
            if ((snake_positions and new_position in snake_positions) or 
                (obstacle_positions and new_position in obstacle_positions)):
                continue
            else:
                valid_position = True
                
        self.position = new_position
        
        # Start spawn animation
        self.spawn_animation = 30  # 1 second at 30 FPS
        
        # Create spawn particles
        self.spawn_particles = []
        for _ in range(8):
            angle = random.random() * 2 * math.pi
            speed = random.uniform(2, 5)
            self.spawn_particles.append({
                'x': new_position[0] + SNAKE_BLOCK // 2,
                'y': new_position[1] + SNAKE_BLOCK // 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 20,
                'max_life': 20
            })
        
        # Random chance for special food
        self.special_counter += 1
        
        # Every 5 regular foods, spawn a special food
        if self.special_counter >= 5:
            self.special_counter = 0
            rand_val = random.random()
            if rand_val < 0.3:  # 30% chance for special food
                self.food_type = SPECIAL_FOOD
                self.special_timer = 300  # 10 seconds at 30 FPS
            elif rand_val < 0.5:  # 20% chance for super food
                self.food_type = SUPER_FOOD
                self.special_timer = 150  # 5 seconds at 30 FPS
            elif rand_val < 0.65:  # 15% chance for shrink food
                self.food_type = SHRINK_FOOD
                self.special_timer = 200  # 6.7 seconds
            elif rand_val < 0.75:  # 10% chance for slowmo food
                self.food_type = SLOWMO_FOOD
                self.special_timer = 250  # 8.3 seconds
            elif rand_val < 0.85:  # 10% chance for double score food
                self.food_type = DOUBLE_SCORE_FOOD
                self.special_timer = 300  # 10 seconds
            elif rand_val < 0.95:  # 10% chance for ghost food
                self.food_type = GHOST_FOOD
                self.special_timer = 200  # 6.7 seconds
            else:  # 5% chance for normal food
                self.food_type = NORMAL_FOOD
        else:
            self.food_type = NORMAL_FOOD
            
        return self.position

    def update(self):
        # Update spawn animation
        if self.spawn_animation > 0:
            self.spawn_animation -= 1
        
        # Update spawn particles
        for particle in self.spawn_particles[:]:
            if isinstance(particle, Particle):
                # Particle class instances are updated in the draw method
                continue
            else:
                # Dictionary-based particles
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['life'] -= 1
                particle['vx'] *= 0.95  # Slow down
                particle['vy'] *= 0.95
                
                if particle['life'] <= 0:
                    self.spawn_particles.remove(particle)
        
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
        elif self.food_type == SHRINK_FOOD:
            return 15
        elif self.food_type == SLOWMO_FOOD:
            return 20
        elif self.food_type == DOUBLE_SCORE_FOOD:
            return 30
        elif self.food_type == GHOST_FOOD:
            return 40
        return 10
    
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
        elif self.food_type == SHRINK_FOOD:
            texture_name = 'shrink_food'
            color = BLUE
        elif self.food_type == SLOWMO_FOOD:
            texture_name = 'slowmo_food'
            color = (0, 255, 255)
        elif self.food_type == DOUBLE_SCORE_FOOD:
            texture_name = 'double_score_food'
            color = (255, 215, 0)
        elif self.food_type == GHOST_FOOD:
            texture_name = 'ghost_food'
            color = (200, 200, 255)
            
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
        
        # Draw spawn animation and particles
        if self.spawn_animation > 0:
            # Draw expanding circle effect
            alpha = int((self.spawn_animation / 30) * 100)
            radius = int((30 - self.spawn_animation) * 2)
            
            # Create a surface for the circle with alpha
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 255, 255, alpha), (radius, radius), radius, 2)
            
            circle_x = self.position[0] + SNAKE_BLOCK // 2 - radius
            circle_y = self.position[1] + SNAKE_BLOCK // 2 - radius
            screen.blit(circle_surface, (circle_x, circle_y))
        
        # Draw spawn particles
        for particle in self.spawn_particles:
            if isinstance(particle, Particle):
                # Particle class instances
                particle.update()
                particle.draw(screen)
                
                # Remove old particles
                if particle.lifetime <= 0:
                    self.spawn_particles.remove(particle)
            else:
                # Dictionary-based particles
                alpha = int((particle['life'] / particle['max_life']) * 255)
                particle_size = max(1, int((particle['life'] / particle['max_life']) * 3))
                
                # Create particle surface with alpha
                particle_surface = pygame.Surface((particle_size, particle_size), pygame.SRCALPHA)
                particle_surface.fill((255, 255, 255, alpha))
                screen.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Create new particles
        if random.random() < 0.3:  # 30% chance to create a particle
            self.spawn_particles.append(Particle(
                self.position[0] + random.randint(0, SNAKE_BLOCK),
                self.position[1] + random.randint(0, SNAKE_BLOCK),
                color
            ))
        
class Particle:
    def __init__(self, x, y, color):
        self.position = [x, y]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.lifetime = 30  # Lifetime in frames
        self.color = color
        
    def update(self):
        # Update position and lifetime
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.lifetime -= 1
        
    def draw(self, screen):
        # Draw the particle
        pygame.draw.circle(screen, self.color, (
            int(self.position[0]), 
            int(self.position[1])
        ), 2)