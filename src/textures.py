import pygame
import os
import random
import math
from constants import *

class TextureManager:
    def __init__(self):
        self.textures = {}
        self.use_textures = True
        self.pixel_art_mode = True
        self.load_textures()
        self.create_pixel_art_assets()
        
    def load_textures(self):
        # Dictionary mapping texture names to file paths
        texture_files = {
            'snake_head': os.path.join(IMAGE_DIR, 'snake.p8.png'),  # Menggunakan p8.png untuk gaya pixel art
            'snake_body': os.path.join(IMAGE_DIR, 'snake.p8.png'),
            'food_normal': os.path.join(IMAGE_DIR, 'snake.p8.png'),
            'food_special': os.path.join(IMAGE_DIR, 'snake.p8.png'),
            'food_super': os.path.join(IMAGE_DIR, 'snake.p8.png'),
            'background': os.path.join(IMAGE_DIR, 'snake.p8.png')
        }
        
        # Coba load setiap texture
        for texture_name, filepath in texture_files.items():
            if os.path.exists(filepath):
                try:
                    # Load texture dan simpan ukuran aslinya
                    original_image = pygame.image.load(filepath).convert_alpha()
                    
                    # Simpan gambar original di dictionary textures
                    self.textures[texture_name] = original_image
                except Exception as e:
                    print(f"Error loading texture {texture_name}: {e}")
                    self.textures[texture_name] = None
            else:                # Jika file tidak ada, set texture ke None
                print(f"Texture file not found: {filepath}")
                self.textures[texture_name] = None
    
    def create_pixel_art_assets(self):
        # Buat palette warna 8-bit
        self.pixel_colors = {
            'black': (0, 0, 0),
            'dark_blue': (29, 43, 83),
            'dark_purple': (126, 37, 83),
            'dark_green': (0, 135, 81),
            'brown': (171, 82, 54),
            'dark_gray': (95, 87, 79),
            'light_gray': (194, 195, 199),
            'white': (255, 241, 232),
            'red': (255, 0, 77),
            'orange': (255, 163, 0),
            'yellow': (255, 236, 39),
            'green': (0, 228, 54),
            'blue': (41, 173, 255),
            'lavender': (131, 118, 156),
            'pink': (255, 119, 168),
            'light_peach': (255, 204, 170),
            # Enhanced 8-bit pixel art colors
            'neon_green': (0, 255, 128),
            'pixel_brown': (140, 83, 36),
            'retro_teal': (69, 187, 169),
            'pixel_purple': (176, 38, 255),
            'deep_red': (190, 38, 51),
            'pixel_tan': (235, 195, 95),
            'dark_teal': (38, 92, 66),
            'pixel_orange': (247, 118, 34),
            'electric_blue': (48, 96, 255)
        }
        
        # Buat tekstur pixel art untuk berbagai elemen game
        self.create_snake_textures()
        self.create_food_textures()
        self.create_background_texture()
        self.create_ui_elements()
        
    def create_snake_textures(self):
        # Snake head (base texture) - create a more detailed pixel art style
        size = SNAKE_BLOCK
        pixel_size = max(1, size // 12)  # Fine-grained pixel size

        # Create base snake head (facing right)
        head_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        head_surface.fill((0, 0, 0, 0))
        
        # Base head shape
        for y in range(pixel_size*2, size-pixel_size*2, pixel_size):
            for x in range(pixel_size*2, size, pixel_size):
                pygame.draw.rect(head_surface, self.pixel_colors['green'], 
                                (x, y, pixel_size, pixel_size))
        
        # Top and bottom edges
        for x in range(pixel_size*3, size, pixel_size):
            pygame.draw.rect(head_surface, self.pixel_colors['dark_green'], 
                            (x, pixel_size, pixel_size, pixel_size))
            pygame.draw.rect(head_surface, self.pixel_colors['dark_green'], 
                            (x, size-pixel_size*2, pixel_size, pixel_size))
        
        # Rounded front (lighter green)
        for y in range(pixel_size*2, size-pixel_size*2, pixel_size):
            pygame.draw.rect(head_surface, self.pixel_colors['neon_green'], 
                            (size-pixel_size*2, y, pixel_size*2, pixel_size))
        
        # Eye
        pygame.draw.rect(head_surface, self.pixel_colors['white'], 
                        (size-pixel_size*5, pixel_size*3, pixel_size*2, pixel_size*2))
        pygame.draw.rect(head_surface, self.pixel_colors['black'], 
                        (size-pixel_size*4, pixel_size*3, pixel_size, pixel_size))
        
        # Scale to create the pixelated look
        scaled_head = self.pixelate_surface(head_surface, 1)
        self.textures['snake_head_right'] = scaled_head
        
        # UP direction
        head_up = pygame.Surface((size, size), pygame.SRCALPHA)
        head_up.fill((0, 0, 0, 0))
        
        # Base head shape
        for y in range(pixel_size*2, size, pixel_size):
            for x in range(pixel_size*2, size-pixel_size*2, pixel_size):
                pygame.draw.rect(head_up, self.pixel_colors['green'], 
                                (x, y, pixel_size, pixel_size))
        
        # Left and right edges
        for y in range(pixel_size*3, size, pixel_size):
            pygame.draw.rect(head_up, self.pixel_colors['dark_green'], 
                            (pixel_size, y, pixel_size, pixel_size))
            pygame.draw.rect(head_up, self.pixel_colors['dark_green'], 
                            (size-pixel_size*2, y, pixel_size, pixel_size))
        
        # Rounded top (lighter green)
        for x in range(pixel_size*2, size-pixel_size*2, pixel_size):
            pygame.draw.rect(head_up, self.pixel_colors['neon_green'], 
                            (x, 0, pixel_size, pixel_size*2))
        
        # Eyes (top-facing perspective)
        pygame.draw.rect(head_up, self.pixel_colors['white'], 
                        (pixel_size*3, pixel_size*3, pixel_size*2, pixel_size*2))
        pygame.draw.rect(head_up, self.pixel_colors['white'], 
                        (size-pixel_size*5, pixel_size*3, pixel_size*2, pixel_size*2))
        pygame.draw.rect(head_up, self.pixel_colors['black'], 
                        (pixel_size*3, pixel_size*3, pixel_size, pixel_size))
        pygame.draw.rect(head_up, self.pixel_colors['black'], 
                        (size-pixel_size*4, pixel_size*3, pixel_size, pixel_size))
        
        # Scale the texture
        self.textures['snake_head_up'] = self.pixelate_surface(head_up, 1)
        
        # LEFT direction (mirror right head)
        head_left = pygame.transform.flip(scaled_head, True, False)
        self.textures['snake_head_left'] = head_left
        
        # DOWN direction
        head_down = pygame.Surface((size, size), pygame.SRCALPHA)
        head_down.fill((0, 0, 0, 0))
        
        # Base head shape
        for y in range(pixel_size*2, size, pixel_size):
            for x in range(pixel_size*2, size-pixel_size*2, pixel_size):
                pygame.draw.rect(head_down, self.pixel_colors['green'], 
                                (x, y, pixel_size, pixel_size))
        
        # Left and right edges
        for y in range(pixel_size*3, size, pixel_size):
            pygame.draw.rect(head_down, self.pixel_colors['dark_green'], 
                            (pixel_size, y, pixel_size, pixel_size))
            pygame.draw.rect(head_down, self.pixel_colors['dark_green'], 
                            (size-pixel_size*2, y, pixel_size, pixel_size))
        
        # Rounded bottom (lighter green)
        for x in range(pixel_size*2, size-pixel_size*2, pixel_size):
            pygame.draw.rect(head_down, self.pixel_colors['neon_green'], 
                            (x, size-pixel_size*2, pixel_size, pixel_size*2))
        
        # Eyes (bottom-facing perspective)
        pygame.draw.rect(head_down, self.pixel_colors['white'], 
                        (pixel_size*3, size-pixel_size*6, pixel_size*2, pixel_size*2))
        pygame.draw.rect(head_down, self.pixel_colors['white'], 
                        (size-pixel_size*5, size-pixel_size*6, pixel_size*2, pixel_size*2))
        pygame.draw.rect(head_down, self.pixel_colors['black'], 
                        (pixel_size*4, size-pixel_size*5, pixel_size, pixel_size))
        pygame.draw.rect(head_down, self.pixel_colors['black'], 
                        (size-pixel_size*4, size-pixel_size*5, pixel_size, pixel_size))
        
        # Scale the texture
        self.textures['snake_head_down'] = self.pixelate_surface(head_down, 1)
        
        # Create snake body (more detailed pixel art texture)
        body_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        body_surface.fill((0, 0, 0, 0))
        
        # Draw body with pixel art pattern
        for y in range(pixel_size, size-pixel_size, pixel_size):
            for x in range(pixel_size, size-pixel_size, pixel_size):
                # Create a pattern of slightly different greens
                if (x // pixel_size + y // pixel_size) % 2 == 0:
                    pygame.draw.rect(body_surface, self.pixel_colors['green'], 
                                    (x, y, pixel_size, pixel_size))
                else:
                    pygame.draw.rect(body_surface, self.pixel_colors['dark_green'], 
                                    (x, y, pixel_size, pixel_size))
        
        # Add a pattern in the center for visual effect
        pygame.draw.rect(body_surface, self.pixel_colors['dark_green'], (size//3, size//3, size//3, size//3))
        
        self.textures['snake_body'] = body_surface
        
    def create_food_textures(self):
        size = SNAKE_BLOCK
        pixel_size = max(1, size // 10)  # Fine-grained pixel size
        
        # Normal food (apple) - pixel art style
        food_normal = pygame.Surface((size, size), pygame.SRCALPHA)
        food_normal.fill((0, 0, 0, 0))
        
        # Apple body
        for y in range(pixel_size*2, size-pixel_size*2, pixel_size):
            for x in range(pixel_size*2, size-pixel_size*2, pixel_size):
                # Circular shape
                dx = x - size/2
                dy = y - size/2
                distance = (dx**2 + dy**2)**0.5
                
                if distance < size/2 - pixel_size*2:
                    # Apple gradient (lighter in center, darker at edges)
                    if distance < size/4:
                        pygame.draw.rect(food_normal, self.pixel_colors['deep_red'], 
                                        (x, y, pixel_size, pixel_size))
                    else:
                        pygame.draw.rect(food_normal, self.pixel_colors['red'], 
                                        (x, y, pixel_size, pixel_size))
        
        # Apple stem
        for y in range(0, pixel_size*3, pixel_size):
            pygame.draw.rect(food_normal, self.pixel_colors['pixel_brown'], 
                            (size//2, y, pixel_size, pixel_size))
        
        # Apple leaf
        for x in range(size//2 + pixel_size, size//2 + pixel_size*4, pixel_size):
            y_offset = abs(x - (size//2 + pixel_size*2)) // pixel_size
            pygame.draw.rect(food_normal, self.pixel_colors['dark_green'], 
                            (x, pixel_size*2 + y_offset*pixel_size, pixel_size, pixel_size))
        
        # Scale the texture
        self.textures['food_normal'] = self.pixelate_surface(food_normal, 1)
        
        # Special food (star) - pixel art style
        food_special = pygame.Surface((size, size), pygame.SRCALPHA)
        food_special.fill((0, 0, 0, 0))
        
        # Star shape (pixel by pixel)
        star_color = self.pixel_colors['pixel_purple']
        outline_color = self.pixel_colors['dark_purple']
        center_color = self.pixel_colors['pink']
        
        # Draw star shape (simplified for pixels)
        for y in range(0, size, pixel_size):
            for x in range(0, size, pixel_size):
                # Basic distance check to create star pattern
                dx = x - size/2
                dy = y - size/2
                distance = (dx**2 + dy**2)**0.5
                angle = math.atan2(dy, dx) % (2 * math.pi)
                
                # Star shape modulation
                point_angle = (angle * 5) % (2 * math.pi)
                distance_mod = abs(math.cos(point_angle)) * 0.3 + 0.7
                
                if distance < (size/2 - pixel_size*2) * distance_mod:
                    # Center is a different color
                    if distance < size/5:
                        pygame.draw.rect(food_special, center_color, 
                                        (x, y, pixel_size, pixel_size))
                    else:
                        pygame.draw.rect(food_special, star_color, 
                                        (x, y, pixel_size, pixel_size))
        
        # Scale the texture
        self.textures['food_special'] = self.pixelate_surface(food_special, 1)
        
        # Super food (gem) - pixel art style
        food_super = pygame.Surface((size, size), pygame.SRCALPHA)
        food_super.fill((0, 0, 0, 0))
        
        # Diamond shape
        for y in range(0, size, pixel_size):
            # Calculate width at this y-position (diamond shape)
            relative_y = abs(y - size/2)
            width = size - relative_y * 2
            
            if width > 0:
                start_x = (size - width) // 2
                
                for x in range(int(start_x), int(start_x + width), pixel_size):
                    # Color gradient based on position
                    rel_x = (x - start_x) / width
                    
                    if 0.2 < rel_x < 0.8 and relative_y < size/3:
                        # Inner gem color (yellow)
                        color = self.pixel_colors['yellow']
                    else:
                        # Outer gem color (blue)
                        color = self.pixel_colors['electric_blue']
                        
                    pygame.draw.rect(food_super, color, 
                                    (x, y, pixel_size, pixel_size))
        
        # Shine effect (white highlights)
        pygame.draw.rect(food_super, self.pixel_colors['white'], 
                        (size//3, size//3, pixel_size*2, pixel_size*2))
        pygame.draw.rect(food_super, self.pixel_colors['white'], 
                        (size//2, size//2, pixel_size, pixel_size))
        
        # Create additional special food textures
        self._create_shrink_food_texture()
        self._create_slowmo_food_texture()
        self._create_double_score_food_texture()
        self._create_ghost_food_texture()
    
    def _create_shrink_food_texture(self):
        """Create pixel art texture for shrink food (blue pill)"""
        size = SNAKE_BLOCK
        pixel_size = size // 8
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Create pill shape in blue
        for y in range(pixel_size * 2, size - pixel_size * 2, pixel_size):
            for x in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
                pygame.draw.rect(surface, self.pixel_colors['blue'], 
                                (x, y, pixel_size, pixel_size))
        
        # Add rounded ends
        for x in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
            pygame.draw.rect(surface, self.pixel_colors['blue'], 
                            (x, pixel_size, pixel_size, pixel_size))
            pygame.draw.rect(surface, self.pixel_colors['blue'], 
                            (x, size - pixel_size * 2, pixel_size, pixel_size))
        
        # Add highlight
        for x in range(pixel_size * 3, size - pixel_size * 4, pixel_size):
            pygame.draw.rect(surface, (150, 150, 255), 
                            (x, pixel_size * 2, pixel_size, pixel_size))
        
        # Add minus symbol
        for x in range(pixel_size * 4, size - pixel_size * 4, pixel_size):
            pygame.draw.rect(surface, self.pixel_colors['white'], 
                            (x, pixel_size * 4, pixel_size, pixel_size))
        
        self.textures['shrink_food'] = self.pixelate_surface(surface, 1)
    
    def _create_slowmo_food_texture(self):
        """Create pixel art texture for slowmo food (cyan clock)"""
        size = SNAKE_BLOCK
        pixel_size = size // 8
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Create clock outline
        for i in range(8):
            angle = i * 45 * math.pi / 180
            x = int(size//2 + 3 * pixel_size * math.cos(angle)) - pixel_size//2
            y = int(size//2 + 3 * pixel_size * math.sin(angle)) - pixel_size//2
            pygame.draw.rect(surface, (0, 255, 255), (x, y, pixel_size, pixel_size))
        
        # Fill center
        for y in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
            for x in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
                pygame.draw.rect(surface, (100, 255, 255), 
                                (x, y, pixel_size, pixel_size))
        
        # Add clock hands
        center_x, center_y = size//2, size//2
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (center_x - pixel_size//2, center_y - pixel_size//2, pixel_size, pixel_size))
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (center_x - pixel_size//2, center_y - pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (center_x + pixel_size, center_y - pixel_size//2, pixel_size, pixel_size))
        
        self.textures['slowmo_food'] = self.pixelate_surface(surface, 1)
    
    def _create_double_score_food_texture(self):
        """Create pixel art texture for double score food (golden star with 2x)"""
        size = SNAKE_BLOCK
        pixel_size = size // 8
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Create star shape with golden color
        star_color = (255, 215, 0)
        highlight_color = (255, 255, 150)
        
        # Star center
        for y in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
            for x in range(pixel_size * 3, size - pixel_size * 3, pixel_size):
                pygame.draw.rect(surface, star_color, (x, y, pixel_size, pixel_size))
        
        # Star points
        points = [
            (size//2, pixel_size),  # top
            (size//2, size - pixel_size * 2),  # bottom
            (pixel_size, size//2),  # left
            (size - pixel_size * 2, size//2),  # right
        ]
        
        for px, py in points:
            pygame.draw.rect(surface, star_color, 
                            (px - pixel_size//2, py - pixel_size//2, pixel_size, pixel_size))
        
        # Add highlight
        pygame.draw.rect(surface, highlight_color, 
                        (pixel_size * 3, pixel_size * 3, pixel_size, pixel_size))
        
        # Add "2x" text
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (pixel_size * 2, pixel_size * 5, pixel_size * 4, pixel_size))
        
        self.textures['double_score_food'] = self.pixelate_surface(surface, 1)
    
    def _create_ghost_food_texture(self):
        """Create pixel art texture for ghost food (translucent white spirit)"""
        size = SNAKE_BLOCK
        pixel_size = size // 8
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        # Create ghost shape
        ghost_color = (200, 200, 255, 180)  # Semi-transparent light blue
        
        # Ghost head (rounded top)
        for y in range(pixel_size * 2, pixel_size * 5, pixel_size):
            for x in range(pixel_size * 2, size - pixel_size * 2, pixel_size):
                temp_surface = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
                temp_surface.fill(ghost_color)
                surface.blit(temp_surface, (x, y))
        
        # Ghost body (wavy bottom)
        for x in range(pixel_size * 2, size - pixel_size * 2, pixel_size):
            height = pixel_size * 6 if (x // pixel_size) % 2 == 0 else pixel_size * 5
            temp_surface = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
            temp_surface.fill(ghost_color)
            surface.blit(temp_surface, (x, height))
        
        # Ghost eyes
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (pixel_size * 3, pixel_size * 3, pixel_size, pixel_size))
        pygame.draw.rect(surface, self.pixel_colors['black'], 
                        (pixel_size * 5, pixel_size * 3, pixel_size, pixel_size))
        
        self.textures['ghost_food'] = surface  # Don't pixelate to keep transparency
    
    def create_background_texture(self):
        # Create a retro pixel art background
        # Define grid sizes for the pixel art background
        tile_size = 40
        pixel_size = 4  # Size of each "pixel" in the pixel art
        
        # Create empty background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Base colors for the grid
        base_color1 = self.pixel_colors['dark_blue']
        base_color2 = self.pixel_colors['dark_teal']
        
        # Create pixel art grid pattern
        for grid_y in range(0, SCREEN_HEIGHT, tile_size):
            for grid_x in range(0, SCREEN_WIDTH, tile_size):
                # Alternate colors in a checkerboard pattern
                base_color = base_color1 if (grid_x // tile_size + grid_y // tile_size) % 2 == 0 else base_color2
                
                # Fill the current grid tile with pixel art
                for y in range(0, tile_size, pixel_size):
                    for x in range(0, tile_size, pixel_size):
                        # Add some noise/variation to create a textured look
                        noise = random.randint(-10, 10)
                        color = (
                            max(0, min(255, base_color[0] + noise)),
                            max(0, min(255, base_color[1] + noise)),
                            max(0, min(255, base_color[2] + noise))
                        )
                        
                        # Draw the "pixel"
                        pygame.draw.rect(background, color, 
                                        (grid_x + x, grid_y + y, pixel_size, pixel_size))
        
        # Add a subtle grid overlay
        for y in range(0, SCREEN_HEIGHT, tile_size):
            pygame.draw.line(background, self.pixel_colors['dark_gray'], 
                            (0, y), (SCREEN_WIDTH, y), 1)
        
        for x in range(0, SCREEN_WIDTH, tile_size):
            pygame.draw.line(background, self.pixel_colors['dark_gray'], 
                            (x, 0), (x, SCREEN_HEIGHT), 1)
        
        # Save the background texture
        self.textures['background'] = background
        
    def create_ui_elements(self):
        """Create pixel art UI elements like buttons, score displays, etc."""
        # Button textures (different states)
        button_width = 200
        button_height = 60
        pixel_size = 2
        
        # Normal button
        button_normal = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        
        # Button fill - dark center with lighter borders
        for y in range(0, button_height, pixel_size):
            for x in range(0, button_width, pixel_size):
                # Border area
                is_border = (x < pixel_size*3 or x >= button_width - pixel_size*3 or 
                            y < pixel_size*3 or y >= button_height - pixel_size*3)
                
                # Corner pixels
                is_corner = ((x < pixel_size*5 or x >= button_width - pixel_size*5) and
                            (y < pixel_size*5 or y >= button_height - pixel_size*5))
                
                if is_corner:
                    # Leave corners transparent for rounded effect
                    continue
                elif is_border:
                    pygame.draw.rect(button_normal, self.pixel_colors['electric_blue'], 
                                    (x, y, pixel_size, pixel_size))
                else:
                    pygame.draw.rect(button_normal, self.pixel_colors['dark_blue'], 
                                    (x, y, pixel_size, pixel_size))
        
        # Add scanlines for retro effect
        for y in range(pixel_size*3, button_height - pixel_size*3, pixel_size*4):
            for x in range(pixel_size*5, button_width - pixel_size*5, pixel_size):
                pygame.draw.rect(button_normal, self.pixel_colors['blue'], 
                                (x, y, pixel_size, pixel_size//2))
        
        self.textures['button_normal'] = button_normal
        
        # Hover button (brighter)
        button_hover = button_normal.copy()
        hover_overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        hover_overlay.fill((50, 50, 100, 128))  # Semi-transparent blue overlay
        button_hover.blit(hover_overlay, (0, 0))
        
        self.textures['button_hover'] = button_hover
        
        # Score display background
        score_bg_width = 120
        score_bg_height = 40
        score_bg = pygame.Surface((score_bg_width, score_bg_height), pygame.SRCALPHA)
        
        # Fill with pixel pattern
        for y in range(0, score_bg_height, pixel_size):
            for x in range(0, score_bg_width, pixel_size):
                is_border = (x < pixel_size*2 or x >= score_bg_width - pixel_size*2 or 
                            y < pixel_size*2 or y >= score_bg_height - pixel_size*2)
                
                if is_border:
                    pygame.draw.rect(score_bg, self.pixel_colors['yellow'], 
                                    (x, y, pixel_size, pixel_size))
                else:
                    pygame.draw.rect(score_bg, (0, 0, 0, 180), 
                                    (x, y, pixel_size, pixel_size))
        
        self.textures['score_bg'] = score_bg
        
        # Game over screen overlay
        gameover_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Create scanlines effect
        for y in range(0, SCREEN_HEIGHT, pixel_size*2):
            pygame.draw.line(gameover_overlay, (0, 0, 0, 150), 
                            (0, y), (SCREEN_WIDTH, y), pixel_size)
        
        # Add vignette effect (darker at edges)
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                # Calculate distance from center (normalized)
                dx = abs(x - SCREEN_WIDTH/2) / (SCREEN_WIDTH/2)
                dy = abs(y - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)
                distance = (dx**2 + dy**2)**0.5
                
                # Stronger effect at the edges
                alpha = int(min(255, distance * 150))
                if x % pixel_size == 0 and y % pixel_size == 0:  # Keep pixelated look
                    pygame.draw.rect(vignette, (0, 0, 0, alpha), 
                                    (x, y, pixel_size, pixel_size))
        
        gameover_overlay.blit(vignette, (0, 0))
        self.textures['gameover_overlay'] = gameover_overlay
    
    def pixelate_surface(self, surface, pixel_size=4):
        """Applies a pixelation effect to a surface."""
        width, height = surface.get_size()
          # Create a smaller version of the surface
        small_surface = pygame.transform.scale(surface, (width // pixel_size, height // pixel_size))
        
        # Scale it back up to the original size, resulting in pixelation
        pixelated = pygame.transform.scale(small_surface, (width, height))
        
        return pixelated
    
    def get_texture(self, texture_name):
        # Special case for snake head, return the appropriate direction texture
        if texture_name == 'snake_head':
            # Default to right if no specific direction
            return self.textures.get('snake_head_right')
            
        if self.use_textures and texture_name in self.textures and self.textures[texture_name] is not None:
            return self.textures[texture_name]
        return None
        
    def get_snake_head_texture(self, direction):
        """Get the appropriate snake head texture based on direction."""
        if direction == (0, -SNAKE_BLOCK):  # UP
            texture_name = 'snake_head_up'
        elif direction == (0, SNAKE_BLOCK):  # DOWN
            texture_name = 'snake_head_down'
        elif direction == (-SNAKE_BLOCK, 0):  # LEFT
            texture_name = 'snake_head_left'
        else:  # RIGHT or default
            texture_name = 'snake_head_right'
            
        if self.use_textures and texture_name in self.textures and self.textures[texture_name] is not None:
            return self.textures[texture_name]
        return None
    
    def draw_background(self, screen):
        """Draw a pixel art background for the game."""
        # Create a simple grid pattern background
        grid_size = 32
        dark_color = self.pixel_colors['dark_blue']
        light_color = self.pixel_colors['dark_green']
        
        for y in range(0, 600, grid_size):  # Use hardcoded values for now
            for x in range(0, 800, grid_size):
                # Checkerboard pattern
                if (x // grid_size + y // grid_size) % 2 == 0:
                    color = dark_color
                else:
                    color = light_color
                    
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size))
                
        # Add some subtle border lines
        border_color = self.pixel_colors['dark_gray']
        for y in range(0, 600, grid_size):
            pygame.draw.line(screen, border_color, (0, y), (800, y), 1)
        for x in range(0, 800, grid_size):
            pygame.draw.line(screen, border_color, (x, 0), (x, 600), 1)
    
    def toggle_textures(self):
        self.use_textures = not self.use_textures
        return self.use_textures
