import pygame
import sys
import os
import math
import random
from snake import Snake
from food import Food
from highscore import HighScore
from sounds import SoundManager
from textures import TextureManager
from constants import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Initialize game components
highscore = HighScore()
sound_manager = SoundManager()
texture_manager = TextureManager()

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    
def draw_button(screen, text, size, x, y, width, height, color, hover_color, text_color, is_hover=False):
    button_color = hover_color if is_hover else color
    pygame.draw.rect(screen, button_color, (x - width//2, y - height//2, width, height), border_radius=5)
    pygame.draw.rect(screen, WHITE, (x - width//2, y - height//2, width, height), 2, border_radius=5)
    draw_text(screen, text, size, x, y, text_color)
    return pygame.Rect(x - width//2, y - height//2, width, height)

def show_menu():
    # Load high scores
    easy_highscore = highscore.get_high_score(EASY)
    medium_highscore = highscore.get_high_score(MEDIUM)
    hard_highscore = highscore.get_high_score(HARD)
    
    # Menu state
    selected_difficulty = MEDIUM
    mouse_pos = (0, 0)
    
    # Play background music
    sound_manager.play_music()
    
    # Initialize button rects
    easy_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 250 - 30, 200, 60)
    medium_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 330 - 30, 200, 60)
    hard_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 410 - 30, 200, 60)
    sound_button = pygame.Rect(100 - 80, 50 - 20, 160, 40)
    music_button = pygame.Rect(300 - 80, 50 - 20, 160, 40)
    texture_button = pygame.Rect(500 - 80, 50 - 20, 160, 40)
    
    # Create pixel art overlay for menu
    scanlines = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(scanlines, (0, 0, 0, 30), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Title animation variables
    title_scale = 1.0
    scale_increasing = True
    title_color_offset = 0
    
    # Create pixel art button textures
    button_normal = texture_manager.get_texture('button_normal')
    button_hover = texture_manager.get_texture('button_hover')
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(mouse_pos):
                    sound_manager.play_sound('menu_select')
                    return EASY
                elif medium_button.collidepoint(mouse_pos):
                    sound_manager.play_sound('menu_select')
                    return MEDIUM
                elif hard_button.collidepoint(mouse_pos):
                    sound_manager.play_sound('menu_select')
                    return HARD
                elif sound_button.collidepoint(mouse_pos):
                    sound_enabled = sound_manager.toggle_sound()
                    sound_manager.play_sound('menu_change')
                elif music_button.collidepoint(mouse_pos):
                    music_enabled = sound_manager.toggle_music()
                elif texture_button.collidepoint(mouse_pos):
                    texture_enabled = texture_manager.toggle_textures()
                    sound_manager.play_sound('menu_change')
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    sound_manager.play_sound('menu_change')
                    if selected_difficulty == EASY:
                        selected_difficulty = MEDIUM
                    elif selected_difficulty == MEDIUM:
                        selected_difficulty = HARD if event.key == pygame.K_DOWN else EASY
                    else:  # HARD
                        selected_difficulty = MEDIUM
                        
                if event.key == pygame.K_RETURN:
                    sound_manager.play_sound('menu_select')
                    return selected_difficulty
                    
                if event.key == pygame.K_s:
                    sound_enabled = sound_manager.toggle_sound()
                    sound_manager.play_sound('menu_change')
                    
                if event.key == pygame.K_m:
                    music_enabled = sound_manager.toggle_music()
                    
                if event.key == pygame.K_t:
                    texture_enabled = texture_manager.toggle_textures()
                    sound_manager.play_sound('menu_change')
                    
        # Clear screen and draw pixel art background
        if texture_manager.use_textures:
            # Use pixel art background
            background_texture = texture_manager.get_texture('background')
            if background_texture:
                screen.blit(background_texture, (0, 0))
            else:
                screen.fill(BLACK)
            
            # Add scanline effect
            screen.blit(scanlines, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Update title animation
        if scale_increasing:
            title_scale += 0.002
            if title_scale >= 1.1:
                scale_increasing = False
        else:
            title_scale -= 0.002
            if title_scale <= 0.95:
                scale_increasing = True
                
        title_color_offset = (title_color_offset + 1) % 360
        title_color = (
            min(255, max(0, int(127 + 128 * math.sin(math.radians(title_color_offset))))),
            min(255, max(0, int(200 + 55 * math.sin(math.radians(title_color_offset + 120))))),
            min(255, max(0, int(100 + 155 * math.sin(math.radians(title_color_offset + 240)))))
        )
        
        # Draw title with pixel art style
        pixel_title_size = 80
        pixel_size = 4
        title_text = "SNAKE GAME"
        title_surface = pygame.Surface((len(title_text) * pixel_title_size//2, pixel_title_size), pygame.SRCALPHA)
        
        # Create custom pixel font for title
        font = pygame.font.SysFont(None, int(pixel_title_size * title_scale))
        temp_text = font.render(title_text, True, title_color)
        
        # Apply pixelation effect
        small_text = pygame.transform.scale(temp_text, (temp_text.get_width() // pixel_size, temp_text.get_height() // pixel_size))
        pixelated_text = pygame.transform.scale(small_text, (temp_text.get_width(), temp_text.get_height()))
        
        # Draw the pixelated text
        text_rect = pixelated_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(pixelated_text, text_rect)
        
        # Draw difficulty buttons with hover effect and pixel art
        easy_hover = easy_button.collidepoint(mouse_pos) or selected_difficulty == EASY
        medium_hover = medium_button.collidepoint(mouse_pos) or selected_difficulty == MEDIUM
        hard_hover = hard_button.collidepoint(mouse_pos) or selected_difficulty == HARD
        
        # Draw buttons with pixel art textures if available
        if texture_manager.use_textures and button_normal and button_hover:
            # Draw Easy button
            button_tex = button_hover if easy_hover else button_normal
            screen.blit(button_tex, (SCREEN_WIDTH//2 - button_tex.get_width()//2, 250 - button_tex.get_height()//2))
            
            # Draw Medium button
            button_tex = button_hover if medium_hover else button_normal
            screen.blit(button_tex, (SCREEN_WIDTH//2 - button_tex.get_width()//2, 330 - button_tex.get_height()//2))
            
            # Draw Hard button
            button_tex = button_hover if hard_hover else button_normal
            screen.blit(button_tex, (SCREEN_WIDTH//2 - button_tex.get_width()//2, 410 - button_tex.get_height()//2))
            
            # Draw button text in pixel art style
            pixel_font_size = 26
            font = pygame.font.SysFont(None, pixel_font_size)
            
            # Pixelate text function
            def pixelate_text(text, pos, color=WHITE):
                temp = font.render(text, True, color)
                small = pygame.transform.scale(temp, (temp.get_width() // 2, temp.get_height() // 2))
                pixel = pygame.transform.scale(small, (temp.get_width(), temp.get_height()))
                rect = pixel.get_rect(center=pos)
                screen.blit(pixel, rect)
            
            pixelate_text("Easy", (SCREEN_WIDTH//2, 250))
            pixelate_text("Medium", (SCREEN_WIDTH//2, 330))
            pixelate_text("Hard", (SCREEN_WIDTH//2, 410))
        else:
            # Fallback to regular buttons
            easy_button = draw_button(screen, "Easy", 40, SCREEN_WIDTH//2, 250, 200, 60, BLUE, BLUE, WHITE, easy_hover)
            medium_button = draw_button(screen, "Medium", 40, SCREEN_WIDTH//2, 330, 200, 60, BLUE, BLUE, WHITE, medium_hover)
            hard_button = draw_button(screen, "Hard", 40, SCREEN_WIDTH//2, 410, 200, 60, BLUE, BLUE, WHITE, hard_hover)
        
        # Draw high scores with pixel art styling
        draw_text(screen, "High Scores:", 40, SCREEN_WIDTH//2, 480, YELLOW)
        
        # Use pixel art score background if available
        score_bg = texture_manager.get_texture('score_bg')
        if texture_manager.use_textures and score_bg:
            hs_y_positions = [520, 550, 580]
            hs_texts = [f"Easy: {easy_highscore}", f"Medium: {medium_highscore}", f"Hard: {hard_highscore}"]
            
            for i, (text, y) in enumerate(zip(hs_texts, hs_y_positions)):
                # Position score background
                bg_rect = score_bg.get_rect(center=(SCREEN_WIDTH//2, y))
                screen.blit(score_bg, bg_rect)
                
                # Draw score text
                pixelate_text(text, (SCREEN_WIDTH//2, y))
        else:
            # Fallback to regular text
            draw_text(screen, f"Easy: {easy_highscore}", 30, SCREEN_WIDTH//2, 520, WHITE)
            draw_text(screen, f"Medium: {medium_highscore}", 30, SCREEN_WIDTH//2, 550, WHITE)
            draw_text(screen, f"Hard: {hard_highscore}", 30, SCREEN_WIDTH//2, 580, WHITE)
        
        # Draw toggle buttons for sound/music/textures
        sound_icon = "Sound: ON" if sound_manager.sound_enabled else "Sound: OFF"
        music_icon = "Music: ON" if sound_manager.music_enabled else "Music: OFF"
        texture_icon = "Textures: ON" if texture_manager.use_textures else "Textures: OFF"
        
        # Use smaller pixel buttons for toggles
        if texture_manager.use_textures and button_normal:
            # Scale down button for toggles
            toggle_btn = pygame.transform.scale(button_normal, (160, 40))
            
            # Draw toggle buttons
            screen.blit(toggle_btn, (100 - 80, 50 - 20))
            screen.blit(toggle_btn, (300 - 80, 50 - 20))
            screen.blit(toggle_btn, (500 - 80, 50 - 20))
            
            # Draw button text
            pixelate_text(sound_icon, (100, 50), WHITE)
            pixelate_text(music_icon, (300, 50), WHITE)
            pixelate_text(texture_icon, (500, 50), WHITE)
        else:
            # Fallback to regular buttons
            sound_button = draw_button(screen, sound_icon, 30, 100, 50, 160, 40, GRAY, GRAY, WHITE, False)
            music_button = draw_button(screen, music_icon, 30, 300, 50, 160, 40, GRAY, GRAY, WHITE, False)
            texture_button = draw_button(screen, texture_icon, 30, 500, 50, 160, 40, GRAY, GRAY, WHITE, False)
        
        # Draw instructions with pixel art style
        instructions_text1 = "Press arrow keys to navigate, Enter to select"
        instructions_text2 = "Press S: Sound, M: Music, T: Textures"
        
        if texture_manager.use_textures:
            pixelate_text(instructions_text1, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 50), GRAY)
            pixelate_text(instructions_text2, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 25), GRAY)
        else:
            draw_text(screen, instructions_text1, 20, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, GRAY)
            draw_text(screen, instructions_text2, 20, SCREEN_WIDTH//2, SCREEN_HEIGHT - 25, GRAY)
        
        # Update display
        pygame.display.flip()
        clock.tick(30)


def game_loop(difficulty):
    # Initialize game elements
    snake = Snake(texture_manager)
    food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, texture_manager)
    score = 0
    game_state = GAME_RUNNING
    game_speed = difficulty
    high_score = highscore.get_high_score(difficulty)
    
    # Define visual effects
    flash_effect = 0
    
    # Add a frame counter to control snake movement
    frame_counter = 0
    
    while True:
        # Adjust game speed based on snake's boost
        current_speed = game_speed + snake.get_speed_boost()
        
        # Increment frame counter
        frame_counter += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Toggle pause
                    if game_state == GAME_RUNNING:
                        game_state = GAME_PAUSED
                        sound_manager.play_sound('pause')
                    elif game_state == GAME_PAUSED:
                        game_state = GAME_RUNNING
                        sound_manager.play_sound('pause')
                        
                if event.key == pygame.K_r and game_state == GAME_OVER:
                    # Return to main menu
                    return
                    
                if event.key == pygame.K_m:
                    sound_manager.toggle_music()
                    
                if event.key == pygame.K_s:
                    sound_manager.toggle_sound()
                    
                if event.key == pygame.K_t:
                    texture_manager.toggle_textures()
                    
                if game_state == GAME_RUNNING:
                    if event.key == pygame.K_UP:
                        snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction('RIGHT')

        # Update game state
        if game_state == GAME_RUNNING:
            # Update food
            food.update()
            
            # Only move the snake every N frames depending on difficulty
            # Lower current_speed = slower movement
            movement_threshold = max(30 - current_speed*2, 1)  # Convert speed to frames
            
            if frame_counter >= movement_threshold:
                # Move snake
                snake.move()
                frame_counter = 0  # Reset frame counter
            
            # Check for collisions
            if snake.check_collision(SCREEN_WIDTH, SCREEN_HEIGHT):
                game_state = GAME_OVER
                sound_manager.play_sound('crash')
                
                # Check for high score
                if score > high_score:
                    highscore.update_score(difficulty, score)
            
            # Check if snake ate food
            if snake.get_head_position() == food.get_position():
                # Apply effects based on food type
                food_type = food.get_food_type()
                points = food.get_points()
                
                # Apply powerup if special food
                if food_type != NORMAL_FOOD:
                    snake.apply_powerup(food_type)
                
                # Apply score multiplier
                points *= snake.get_score_multiplier()
                
                # Update score and grow snake
                score += points
                snake.grow()
                
                # Spawn new food, giving snake positions to avoid
                food.spawn(snake.get_all_positions())
                
                # Play appropriate sound and trigger flash effect
                if food_type == NORMAL_FOOD:
                    sound_manager.play_sound('eat')
                    flash_effect = 5
                elif food_type == SPECIAL_FOOD:
                    sound_manager.play_sound('special')
                    flash_effect = 10
                elif food_type == SUPER_FOOD:
                    sound_manager.play_sound('super')
                    flash_effect = 15

        # Clear screen
        screen.fill(BLACK)
        
        # Apply flash effect
        if flash_effect > 0:
            flash_alpha = min(100, flash_effect * 10)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, flash_alpha))
            screen.blit(overlay, (0, 0))
            flash_effect -= 1
        
        # Draw game elements
        snake.draw(screen)
        food.draw(screen)
        
        # Draw UI with pixel art styling
        if texture_manager.use_textures:
            # Get score background texture if available
            score_bg = texture_manager.get_texture('score_bg')
            
            # Pixelate text function
            def pixelate_text(text, pos, color, size=30):
                font = pygame.font.SysFont(None, size)
                temp = font.render(text, True, color)
                small = pygame.transform.scale(temp, (temp.get_width() // 2, temp.get_height() // 2))
                pixel = pygame.transform.scale(small, (temp.get_width(), temp.get_height()))
                rect = pixel.get_rect(center=pos)
                screen.blit(pixel, rect)
            
            # Draw score with pixel art styling
            if score_bg:
                # Position score background
                score_bg_rect = score_bg.get_rect(topleft=(10, 10))
                screen.blit(score_bg, score_bg_rect)
                
                # Draw score text
                pixelate_text(f"Score: {score}", (70, 30), WHITE)
                
                # Draw high score
                high_score_bg_rect = score_bg.get_rect(topright=(SCREEN_WIDTH - 10, 10))
                screen.blit(score_bg, high_score_bg_rect)
                pixelate_text(f"High: {high_score}", (SCREEN_WIDTH - 70, 30), WHITE)
                
                # Draw difficulty
                difficulty_text = "Easy" if difficulty == EASY else "Medium" if difficulty == MEDIUM else "Hard"
                diff_bg_rect = score_bg.get_rect(center=(SCREEN_WIDTH//2, 30))
                screen.blit(score_bg, diff_bg_rect)
                pixelate_text(f"Diff: {difficulty_text}", (SCREEN_WIDTH//2, 30), WHITE)
            else:
                # Fallback to simple text
                pixelate_text(f"Score: {score}", (70, 30), WHITE)
                pixelate_text(f"High: {high_score}", (SCREEN_WIDTH - 70, 30), WHITE)
                difficulty_text = "Easy" if difficulty == EASY else "Medium" if difficulty == MEDIUM else "Hard"
                pixelate_text(f"Diff: {difficulty_text}", (SCREEN_WIDTH//2, 30), WHITE)
            
            # Draw power-up status with pixel art styling
            if snake.get_speed_boost() > 0:
                # Draw speed boost indicator with pixel art style
                boost_text = "SPEED BOOST"
                
                # Create pixelated flashing text
                flash = abs(math.sin(pygame.time.get_ticks() * 0.01)) > 0.5
                pixelate_text(boost_text, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 30), 
                             PURPLE if flash else (PURPLE[0]//2, PURPLE[1]//2, PURPLE[2]//2), 30)
                
                # Add small animated pixel arrow indicators
                arrow_time = pygame.time.get_ticks() // 100 % 3
                arrow_pixels = [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ] if arrow_time == 0 else [
                    [0, 0, 0],
                    [0, 1, 0],
                    [1, 1, 1]
                ] if arrow_time == 1 else [
                    [1, 0, 0],
                    [1, 1, 0],
                    [1, 0, 0]
                ]
                
                pixel_size = 3
                arrow_x = SCREEN_WIDTH//2 - 100
                arrow_y = SCREEN_HEIGHT - 30
                
                for y, row in enumerate(arrow_pixels):
                    for x, pixel in enumerate(row):
                        if pixel:
                            pygame.draw.rect(screen, PURPLE, 
                                           (arrow_x + x*pixel_size, arrow_y - 5 + y*pixel_size, 
                                            pixel_size, pixel_size))
                
                arrow_x = SCREEN_WIDTH//2 + 80
                for y, row in enumerate(arrow_pixels):
                    for x, pixel in enumerate(row):
                        if pixel:
                            pygame.draw.rect(screen, PURPLE, 
                                           (arrow_x + x*pixel_size, arrow_y - 5 + y*pixel_size, 
                                            pixel_size, pixel_size))
                
            if snake.get_score_multiplier() > 1:
                # Draw score multiplier with pixel art style
                multi_text = f"SCORE x{snake.get_score_multiplier()}"
                
                # Pulsate the text
                scale = 1.0 + abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.2
                size = int(30 * scale)
                
                pixelate_text(multi_text, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 60), GOLD, size)
                
                # Add sparkle effect
                if random.random() > 0.7:
                    sparkle_x = SCREEN_WIDTH//2 + random.randint(-50, 50)
                    sparkle_y = SCREEN_HEIGHT - 60 + random.randint(-10, 10)
                    sparkle_size = random.randint(2, 4)
                    
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x, sparkle_y, sparkle_size, sparkle_size))
        else:
            # Draw UI with standard styling
            draw_text(screen, f"Score: {score}", 30, 70, 20)
            high_score = max(high_score, score)
            draw_text(screen, f"High Score: {high_score}", 30, SCREEN_WIDTH - 100, 20)
            difficulty_text = "Easy" if difficulty == EASY else "Medium" if difficulty == MEDIUM else "Hard"
            draw_text(screen, f"Difficulty: {difficulty_text}", 25, SCREEN_WIDTH//2, 20)
            
            # Draw power-up status if active
            if snake.get_speed_boost() > 0:
                draw_text(screen, "SPEED BOOST", 25, SCREEN_WIDTH//2, SCREEN_HEIGHT - 30, PURPLE)
                
            if snake.get_score_multiplier() > 1:
                draw_text(screen, f"SCORE x{snake.get_score_multiplier()}", 25, SCREEN_WIDTH//2, SCREEN_HEIGHT - 60, GOLD)
        
        # Draw game state messages
        if game_state == GAME_PAUSED:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "GAME PAUSED", 50, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            draw_text(screen, "Press P to continue", 30, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
            draw_text(screen, "M: Music, S: Sound, T: Textures", 25, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90)
        
        elif game_state == GAME_OVER:
            # Apply pixel art game over screen
            if texture_manager.use_textures:
                # Semi-transparent overlay with scanlines
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                # Add scanlines for retro effect
                for y in range(0, SCREEN_HEIGHT, 4):
                    pygame.draw.line(screen, (255, 0, 0, 40), (0, y), (SCREEN_WIDTH, y), 1)
                
                # Create 8-bit style game over text
                pixel_size = 4
                gameover_text = "GAME OVER"
                font = pygame.font.SysFont(None, 80)
                temp_text = font.render(gameover_text, True, RED)
                
                # Apply pixelation
                small_surface = pygame.transform.scale(temp_text, (temp_text.get_width() // pixel_size, temp_text.get_height() // pixel_size))
                pixelated_text = pygame.transform.scale(small_surface, (temp_text.get_width(), temp_text.get_height()))
                
                # Make it pulse
                pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.003) * 55) + 200)
                
                # Apply color shift using overlay
                colored_overlay = pygame.Surface(pixelated_text.get_size(), pygame.SRCALPHA)
                colored_overlay.fill((pulse, 0, 0, 0))
                pixelated_text.blit(colored_overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                
                # Draw the text
                text_rect = pixelated_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
                screen.blit(pixelated_text, text_rect)
                
                # Pixelate text function for reuse
                def pixelate_text(text, pos, color, size):
                    font = pygame.font.SysFont(None, size)
                    temp = font.render(text, True, color)
                    small = pygame.transform.scale(temp, (temp.get_width() // pixel_size, temp.get_height() // pixel_size))
                    pixel = pygame.transform.scale(small, (temp.get_width(), temp.get_height()))
                    rect = pixel.get_rect(center=pos)
                    screen.blit(pixel, rect)
                
                # Draw pixelated score
                pixelate_text(f"Final Score: {score}", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), YELLOW, 50)
                
                # Show new high score message if applicable
                if score > high_score:
                    # Add a blinking effect
                    if pygame.time.get_ticks() % 1000 < 500:  # Blink every half second
                        pixelate_text("NEW HIGH SCORE!", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60), GOLD, 40)
                
                # Draw pixelated retry message
                pixelate_text("Press R to return to menu", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), WHITE, 40)
                
                # Add pixel art decoration (skull or death animation)
                if pygame.time.get_ticks() % 1000 < 500:  # Blink every half second
                    pixel_skull = [
                        "  ######  ",
                        " ######## ",
                        "##  ##  ##",
                        "##  ##  ##",
                        "##########",
                        " ######## ",
                        "  ######  ",
                        " ## ## ## ",
                        "##  ##  ##"
                    ]
                    
                    skull_x = SCREEN_WIDTH//2 - len(pixel_skull[0])*4//2
                    skull_y = SCREEN_HEIGHT//2 + 140
                    pixel_size = 4
                    
                    for y, row in enumerate(pixel_skull):
                        for x, char in enumerate(row):
                            if char == '#':
                                pygame.draw.rect(screen, RED, 
                                               (skull_x + x*pixel_size, skull_y + y*pixel_size, 
                                                pixel_size, pixel_size))
            else:
                # Fallback to standard game over screen
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                # Animate game over text
                bounce = abs(math.sin(pygame.time.get_ticks() / 300)) * 10
                
                draw_text(screen, "GAME OVER", 60, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50 + bounce, RED)
                draw_text(screen, f"Final Score: {score}", 40, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)
                
                # Show new high score message if applicable
                if score > high_score:
                    draw_text(screen, "NEW HIGH SCORE!", 35, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60, GOLD)
                    
                draw_text(screen, "Press R to return to menu", 30, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
        
        # Update display
        pygame.display.flip()
        clock.tick(30)


def main():
    while True:
        # Show main menu and get selected difficulty
        difficulty = show_menu()
        
        # Start game with selected difficulty
        game_loop(difficulty)


if __name__ == '__main__':
    main()