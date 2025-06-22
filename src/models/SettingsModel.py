class SettingsModel:
    """Model for game settings"""

    def __init__(self):
        self.volume = 50
        self.difficulty = "Normal"
        self.fullscreen = False

    def set_volume(self, volume):
        """Set volume level (0-100)"""
        self.volume = max(0, min(100, volume))

    def get_volume(self):
        """Get current volume level"""
        return self.volume

    def set_difficulty(self, difficulty):
        """Set game difficulty"""
        valid_difficulties = ["Easy", "Normal", "Hard"]
        if difficulty in valid_difficulties:
            self.difficulty = difficulty

    def get_difficulty(self):
        """Get current difficulty"""
        return self.difficulty

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen

    def is_fullscreen(self):
        """Check if fullscreen is enabled"""
        return self.fullscreen
