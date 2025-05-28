import pygame
import sys
import math
from constants import *
from snake import Snake
from food import Food
from obstacles import ObstacleManager
from sounds import SoundManager
from textures import TextureManager
from highscore import HighScore

DIFFICULTY_SPEED = {'easy': EASY, 'medium': MEDIUM, 'hard': HARD}

class GameManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.game_state = MENU
        self.selected_difficulty = 'medium'
        self.selected_game_mode = CLASSIC_MODE
        self.menu_selection = 0
        self.settings_selection = 0
        
        # Game components
        self.snake = None
        self.food = None
        self.obstacle_manager = None
        self.highscore = HighScore()
        self.sound_manager = SoundManager()
        self.texture_manager = TextureManager()
        
        # Game variables
        self.score = 0
        self.current_speed = 0
        self.frame_counter = 0
        self.time_remaining = 0  # For time attack mode
        self.paused = False
        
        # Animation variables
        self.menu_animation_timer = 0
        self.transition_alpha = 0
        self.transitioning = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_state == MENU:
                self._handle_menu_input(event.key)
            elif self.game_state == GAME_MODE_SELECT:
                self._handle_game_mode_input(event.key)
            elif self.game_state == SETTINGS:
                self._handle_settings_input(event.key)
            elif self.game_state == HIGH_SCORES:
                self._handle_high_scores_input(event.key)
            elif self.game_state == GAME_RUNNING:
                self._handle_game_input(event.key)
            elif self.game_state == GAME_PAUSED:
                self._handle_pause_input(event.key)
            elif self.game_state == GAME_OVER:
                self._handle_game_over_input(event.key)
    
    def _handle_menu_input(self, key):
        menu_options = 6  # Start, Game Mode, High Scores, Settings, About, Quit
        
        if key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % menu_options
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % menu_options
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.sound_manager.play_sound('menu_select')
            if self.menu_selection == 0:  # Start Game
                self._start_new_game()
            elif self.menu_selection == 1:  # Game Mode
                self.game_state = GAME_MODE_SELECT
            elif self.menu_selection == 2:  # High Scores
                self.game_state = HIGH_SCORES
            elif self.menu_selection == 3:  # Settings
                self.game_state = SETTINGS
            elif self.menu_selection == 4:  # About
                self._show_about()
            elif self.menu_selection == 5:  # Quit
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def _handle_game_mode_input(self, key):
        if key == pygame.K_UP:
            self.selected_game_mode = (self.selected_game_mode - 1) % 3
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_DOWN:
            self.selected_game_mode = (self.selected_game_mode + 1) % 3
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.sound_manager.play_sound('menu_select')
            self._start_new_game()
        elif key == pygame.K_ESCAPE:
            self.game_state = MENU
    
    def _handle_settings_input(self, key):
        settings_options = 4  # Sound, Music, Difficulty, Back
        
        if key == pygame.K_UP:
            self.settings_selection = (self.settings_selection - 1) % settings_options
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_DOWN:
            self.settings_selection = (self.settings_selection + 1) % settings_options
            self.sound_manager.play_sound('menu_change')
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.sound_manager.play_sound('menu_select')
            if self.settings_selection == 0:  # Toggle Sound
                self.sound_manager.toggle_sound()
            elif self.settings_selection == 1:  # Toggle Music
                self.sound_manager.toggle_music()
            elif self.settings_selection == 2:  # Change Difficulty
                # Cycle through string keys
                if self.selected_difficulty == 'easy':
                    self.selected_difficulty = 'medium'
                elif self.selected_difficulty == 'medium':
                    self.selected_difficulty = 'hard'
                else:
                    self.selected_difficulty = 'easy'
            elif self.settings_selection == 3:  # Back
                self.game_state = MENU
        elif key == pygame.K_ESCAPE:
            self.game_state = MENU
    
    def _handle_high_scores_input(self, key):
        if key == pygame.K_ESCAPE or key == pygame.K_RETURN:
            self.game_state = MENU
    
    def _handle_game_input(self, key):
        if key == pygame.K_UP and self.snake.direction != (0, SNAKE_BLOCK):
            self.snake.change_direction((0, -SNAKE_BLOCK))
        elif key == pygame.K_DOWN and self.snake.direction != (0, -SNAKE_BLOCK):
            self.snake.change_direction((0, SNAKE_BLOCK))
        elif key == pygame.K_LEFT and self.snake.direction != (SNAKE_BLOCK, 0):
            self.snake.change_direction((-SNAKE_BLOCK, 0))
        elif key == pygame.K_RIGHT and self.snake.direction != (-SNAKE_BLOCK, 0):
            self.snake.change_direction((SNAKE_BLOCK, 0))
        elif key == pygame.K_ESCAPE or key == pygame.K_p:
            self.game_state = GAME_PAUSED
            self.sound_manager.play_sound('pause')
    
    def _handle_pause_input(self, key):
        if key == pygame.K_ESCAPE or key == pygame.K_p or key == pygame.K_RETURN:
            self.game_state = GAME_RUNNING
        elif key == pygame.K_q:
            self.game_state = MENU
    
    def _handle_game_over_input(self, key):
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            self._start_new_game()
        elif key == pygame.K_ESCAPE:
            self.game_state = MENU
    
    def _start_new_game(self):
        self.game_state = GAME_RUNNING
        self.score = 0
        self.current_speed = DIFFICULTY_SPEED[self.selected_difficulty]
        self.frame_counter = 0
        
        # Initialize game objects
        self.snake = Snake(self.texture_manager)
        self.food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, self.texture_manager)
        self.obstacle_manager = ObstacleManager(SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_game_mode)
        
        # Setup time attack mode
        if self.selected_game_mode == TIME_ATTACK_MODE:
            self.time_remaining = TIME_ATTACK_DURATION * 30  # Convert to frames
        
        # Spawn initial food
        self.food.spawn(self.snake.get_all_positions(), self.obstacle_manager.get_obstacle_positions())
    
    def _show_about(self):
        # Simple about dialog - could be expanded
        pass
    
    def update(self):
        if self.game_state == MENU:
            self._update_menu()
        elif self.game_state == GAME_RUNNING:
            self._update_game()
        elif self.game_state == GAME_PAUSED:
            self._update_pause()
    
    def _update_menu(self):
        self.menu_animation_timer += 1
        # Update background music
        if not self.sound_manager.music_playing:
            self.sound_manager.play_music()
    
    def _update_game(self):
        # Update frame counter
        self.frame_counter += 1
        
        # Calculate movement threshold based on speed and slowmo
        base_threshold = max(30 - self.current_speed * 2, 1)
        if self.snake and self.snake.is_slowmo_active():
            movement_threshold = base_threshold * 2  # Slow down during slowmo
        else:
            movement_threshold = base_threshold
        
        # Move snake
        if self.frame_counter >= movement_threshold:
            self.snake.move()
            self.frame_counter = 0
            
            # Check collision
            if self.snake.check_collision(SCREEN_WIDTH, SCREEN_HEIGHT, 
                                        self.obstacle_manager.get_obstacle_positions()):
                self._game_over()
                return
        
        # Check food collision
        if self.snake.get_head_position() == self.food.get_position():
            self.sound_manager.play_sound('eat')
            food_type = self.food.get_food_type()
            
            # Apply food effects
            if food_type != NORMAL_FOOD:
                self.snake.apply_powerup(food_type)
                if food_type == SPECIAL_FOOD:
                    self.sound_manager.play_sound('special')
                elif food_type == SUPER_FOOD:
                    self.sound_manager.play_sound('super')
            
            # Update score
            points = self.food.get_points() * self.snake.get_score_multiplier()
            self.score += points
            
            # Grow snake (except for shrink food)
            if food_type != SHRINK_FOOD:
                self.snake.grow()
            
            # Spawn new food
            self.food.spawn(self.snake.get_all_positions(), 
                          self.obstacle_manager.get_obstacle_positions())
            
            # Add obstacles occasionally in classic mode
            if self.selected_game_mode == CLASSIC_MODE and self.score % 100 == 0:
                self.obstacle_manager.add_random_obstacle(
                    self.snake.get_all_positions(), 
                    self.food.get_position()
                )
        
        # Update time attack mode
        if self.selected_game_mode == TIME_ATTACK_MODE:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self._game_over()
                return
        
        # Update game objects
        self.food.update()
        self.obstacle_manager.update()

    def _update_pause(self):
        # Nothing to update during pause
        pass

    def _game_over(self):
        self.game_state = GAME_OVER
        self.sound_manager.play_sound('crash')

        # Update and save high score
        if self.score > self.highscore.scores.get(self.selected_difficulty, 0):
            self.highscore.scores[self.selected_difficulty] = self.score
            self.highscore.save_scores()

        # Start death animation
        if self.snake:
            self.snake.start_death_animation()
    
    def draw(self):
        if self.game_state == MENU:
            self._draw_menu()
        elif self.game_state == GAME_MODE_SELECT:
            self._draw_game_mode_select()
        elif self.game_state == SETTINGS:
            self._draw_settings()
        elif self.game_state == HIGH_SCORES:
            self._draw_high_scores()
        elif self.game_state == GAME_RUNNING:
            self._draw_game()
        elif self.game_state == GAME_PAUSED:
            self._draw_pause()
        elif self.game_state == GAME_OVER:
            self._draw_game_over()
    
    def _draw_menu(self):
        self.screen.fill(BLACK)
        
        # Draw animated title
        title_y = 100 + math.sin(self.menu_animation_timer * 0.1) * 10
        self._draw_text("PIXEL SNAKE", 72, SCREEN_WIDTH // 2, int(title_y), YELLOW)
        
        # Draw menu options
        menu_items = [
            "Start Game",
            "Game Mode", 
            "High Scores",
            "Settings",
            "About",
            "Quit"
        ]
        
        start_y = 250
        for i, item in enumerate(menu_items):
            color = WHITE if i == self.menu_selection else GRAY
            if i == self.menu_selection:
                # Add selection indicator
                self._draw_text(">", 36, SCREEN_WIDTH // 2 - 120, start_y + i * 50, YELLOW)
                self._draw_text("<", 36, SCREEN_WIDTH // 2 + 120, start_y + i * 50, YELLOW)
            
            self._draw_text(item, 36, SCREEN_WIDTH // 2, start_y + i * 50, color)
    
    def _draw_game_mode_select(self):
        self.screen.fill(BLACK)
        
        self._draw_text("SELECT GAME MODE", 48, SCREEN_WIDTH // 2, 100, YELLOW)
        
        game_modes = [
            "Classic Mode",
            "Time Attack", 
            "Challenge Mode"
        ]
        
        descriptions = [
            "Traditional snake game with growing obstacles",
            "Score as much as possible in 2 minutes",
            "Navigate through predefined obstacle courses"
        ]
        
        start_y = 200
        for i, (mode, desc) in enumerate(zip(game_modes, descriptions)):
            color = WHITE if i == self.selected_game_mode else GRAY
            if i == self.selected_game_mode:
                self._draw_text(">", 36, SCREEN_WIDTH // 2 - 150, start_y + i * 80, YELLOW)
                
            self._draw_text(mode, 36, SCREEN_WIDTH // 2, start_y + i * 80, color)
            self._draw_text(desc, 20, SCREEN_WIDTH // 2, start_y + i * 80 + 30, GRAY)
        
        self._draw_text("Press ENTER to start, ESC to go back", 24, SCREEN_WIDTH // 2, 500, WHITE)
    
    def _draw_settings(self):
        self.screen.fill(BLACK)
        
        self._draw_text("SETTINGS", 48, SCREEN_WIDTH // 2, 100, YELLOW)
        
        settings_items = [
            f"Sound: {'ON' if self.sound_manager.sound_enabled else 'OFF'}",
            f"Music: {'ON' if self.sound_manager.music_enabled else 'OFF'}",
            f"Difficulty: {self.selected_difficulty.upper()}",
            "Back to Menu"
        ]
        
        start_y = 200
        for i, item in enumerate(settings_items):
            color = WHITE if i == self.settings_selection else GRAY
            if i == self.settings_selection:
                self._draw_text(">", 36, SCREEN_WIDTH // 2 - 150, start_y + i * 60, YELLOW)
            
            self._draw_text(item, 32, SCREEN_WIDTH // 2, start_y + i * 60, color)
    
    def _draw_high_scores(self):
        self.screen.fill(BLACK)
        
        self._draw_text("HIGH SCORES", 48, SCREEN_WIDTH // 2, 100, YELLOW)
        
        difficulties = ["EASY", "MEDIUM", "HARD"]
        colors = [GREEN, YELLOW, RED]
        
        start_y = 200
        for i, (diff_name, diff_value, color) in enumerate(zip(difficulties, [EASY, MEDIUM, HARD], colors)):
            score = self.highscore.get_high_score(diff_value)
            self._draw_text(f"{diff_name}: {score}", 32, SCREEN_WIDTH // 2, start_y + i * 60, color)
        
        self._draw_text("Press ESC or ENTER to go back", 24, SCREEN_WIDTH // 2, 450, WHITE)
    
    def _draw_game(self):
        # Draw background
        self.texture_manager.draw_background(self.screen)
        
        # Draw obstacles
        self.obstacle_manager.draw(self.screen, self.texture_manager)
        
        # Draw food
        self.food.draw(self.screen)
        
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw UI
        self._draw_game_ui()
    
    def _draw_pause(self):
        # Draw game state with overlay
        self._draw_game()
        
        # Draw pause overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        self._draw_text("PAUSED", 72, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, YELLOW)
        self._draw_text("Press P or ESC to resume", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)
        self._draw_text("Press Q to quit to menu", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)
    
    def _draw_game_over(self):
        # Draw game state
        self._draw_game()
        
        # Draw game over overlay with scanlines effect
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        
        # Add scanlines
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(overlay, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        self._draw_text("GAME OVER", 72, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, RED)
        self._draw_text(f"Final Score: {self.score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, WHITE)
        
        # Show high score if achieved
        high_score = self.highscore.get_high_score(self.selected_difficulty)
        if self.score >= high_score:
            self._draw_text("NEW HIGH SCORE!", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, GOLD)
        else:
            self._draw_text(f"High Score: {high_score}", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, GRAY)
        
        self._draw_text("Press ENTER to play again", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)
        self._draw_text("Press ESC for main menu", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, WHITE)
    
    def _draw_game_ui(self):
        # Draw score
        self._draw_text(f"Score: {self.score}", 32, 100, 30, WHITE)
        
        # Draw multiplier if active
        if self.snake.get_score_multiplier() > 1:
            self._draw_text(f"Multiplier: x{self.snake.get_score_multiplier()}", 24, 100, 65, GOLD)
        
        # Draw active power-ups
        power_up_y = 100
        if self.snake.boost_timer > 0:
            self._draw_text("SPEED BOOST", 20, 100, power_up_y, PURPLE)
            power_up_y += 25
        
        if self.snake.is_ghost_mode():
            self._draw_text("GHOST MODE", 20, 100, power_up_y, (200, 200, 255))
            power_up_y += 25
        
        if self.snake.is_slowmo_active():
            self._draw_text("SLOW MOTION", 20, 100, power_up_y, (0, 255, 255))
            power_up_y += 25
        
        if self.snake.double_score_timer > 0:
            self._draw_text("DOUBLE SCORE", 20, 100, power_up_y, (255, 215, 0))
            power_up_y += 25
        
        # Draw time remaining for time attack
        if self.selected_game_mode == TIME_ATTACK_MODE:
            time_seconds = self.time_remaining // 30
            minutes = time_seconds // 60
            seconds = time_seconds % 60
            time_color = RED if time_seconds < 30 else WHITE
            self._draw_text(f"Time: {minutes:02d}:{seconds:02d}", 32, SCREEN_WIDTH - 120, 30, time_color)
    
    def _draw_text(self, text, size, x, y, color=WHITE):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
