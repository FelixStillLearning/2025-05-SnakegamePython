import pygame
import os
from constants import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        self.load_sounds()
        
    def load_sounds(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Map sound effects to files
        sound_mapping = {
            'eat': 'Collect_Point_2.wav',
            'special': 'Character_Vowel_4.wav',
            'super': 'High_Score.wav',
            'crash': 'Orc_Hit03.wav',
            'menu_select': 'Menu_Select2.wav',
            'menu_change': 'Spring1.wav',
            'pause': 'Animal_Vowel_4.wav'
        }
        
        # Load each sound effect
        for sound_name, filename in sound_mapping.items():
            filepath = os.path.join(SOUND_DIR, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                except Exception as e:
                    print(f"Error loading sound {sound_name}: {e}")
                    self.sounds[sound_name] = self._create_placeholder_sound(sound_name)
            else:
                print(f"Sound file not found: {filepath}")
                self.sounds[sound_name] = self._create_placeholder_sound(sound_name)
                
    def _create_placeholder_sound(self, sound_type):
        # Create a placeholder sound effect in memory
        # This avoids errors when sound files are missing
        buffer = bytearray(88200)  # 1 second of silence (44100 * 2)
        
        if sound_type == 'eat':
            # Generate a short beep
            freq = 800
            for i in range(4410):  # 0.1 seconds
                value = int(127 * (1 + (i < 2205) - 2 * (i >= 2205)))
                buffer[i * 2] = buffer[i * 2 + 1] = value
                
        elif sound_type in ['special', 'super']:
            # Generate a higher pitched beep
            freq = 1000
            for i in range(8820):  # 0.2 seconds
                value = int(127 * (1 + (i < 4410) - 2 * (i >= 4410)))
                buffer[i * 2] = buffer[i * 2 + 1] = value
                
        elif sound_type == 'crash':
            # Generate a low noise
            freq = 200
            for i in range(22050):  # 0.5 seconds
                value = int(127 * (1 + (i < 11025) - 2 * (i >= 11025)))
                buffer[i * 2] = buffer[i * 2 + 1] = value
                
        sound = pygame.mixer.Sound(buffer=buffer)
        return sound
                
    def play_sound(self, sound_name):
        # Play a sound effect if sound is enabled
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def toggle_sound(self):
        # Toggle sound effects on/off
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
        
    def toggle_music(self):
        # Toggle background music on/off
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled and not self.music_playing:
            self.play_music()
        elif not self.music_enabled and self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
            
        return self.music_enabled
        
    def play_music(self, music_file='Music_Loop_1.wav'):
        # Play background music if music is enabled
        if self.music_enabled:
            filepath = os.path.join(SOUND_DIR, 'Music Loop 1', music_file)
            if os.path.exists(filepath):
                try:
                    pygame.mixer.music.load(filepath)
                    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                    self.music_playing = True
                except Exception as e:
                    print(f"Could not play music: {filepath} - {e}")
            else:
                print(f"Music file not found: {filepath}")
                
    def stop_music(self):
        # Stop currently playing music
        pygame.mixer.music.stop()
        self.music_playing = False
