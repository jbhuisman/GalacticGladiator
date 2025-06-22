class GameModel:
    """Model for game logic and state"""

    def __init__(self):
        self.score = 0
        self.is_running = True
        self.is_paused = False

    def update(self, delta_time):
        """Update game logic"""
        if self.is_running and not self.is_paused:
            self.score += 1

    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused

    def reset_game(self):
        """Reset game to initial state"""
        self.score = 0
        self.is_running = True
        self.is_paused = False

    def get_score(self):
        """Get current score"""
        return self.score

    def is_game_paused(self):
        """Check if game is paused"""
        return self.is_paused
