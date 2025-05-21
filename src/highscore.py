import os
from constants import *

class HighScore:
    def __init__(self):
        self.scores = {
            'easy': 0,
            'medium': 0,
            'hard': 0
        }
        self.load_scores()
        
    def load_scores(self):
        # Try to load high scores from file
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, 'r') as file:
                    for line in file:
                        parts = line.strip().split(':')
                        if len(parts) == 2:
                            difficulty, score = parts
                            if difficulty in self.scores:
                                try:
                                    self.scores[difficulty] = int(score)
                                except ValueError:
                                    pass
        except Exception as e:
            print(f"Error loading high scores: {e}")
            
    def save_scores(self):
        # Save high scores to file
        try:
            with open(HIGHSCORE_FILE, 'w') as file:
                for difficulty, score in self.scores.items():
                    file.write(f"{difficulty}:{score}\n")
        except Exception as e:
            print(f"Error saving high scores: {e}")
            
    def update_score(self, difficulty, score):
        # Update high score if the new score is higher
        difficulty_key = 'easy' if difficulty == EASY else 'medium' if difficulty == MEDIUM else 'hard'
        if score > self.scores[difficulty_key]:
            self.scores[difficulty_key] = score
            self.save_scores()
            return True
        return False
        
    def get_high_score(self, difficulty):
        # Get high score for the specified difficulty
        difficulty_key = 'easy' if difficulty == EASY else 'medium' if difficulty == MEDIUM else 'hard'
        return self.scores[difficulty_key]
