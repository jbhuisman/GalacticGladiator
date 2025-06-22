import arcade
from models.MenuModel import MenuModel
from views.MenuPane import MenuPane


class MenuController:
    """Controller for menu interactions"""

    def __init__(self, window):
        self.window = window
        self.model = MenuModel()
        self.view = MenuPane(self)

    def start_game(self):
        """Start a new game"""
        from controllers.GameController import GameController
        game_controller = GameController(self.window)
        self.window.show_view(game_controller.view)

    def show_settings(self):
        """Show settings screen"""
        from controllers.SettingsController import SettingsController
        settings_controller = SettingsController(self.window)
        self.window.show_view(settings_controller.view)

    def quit_game(self):
        """Quit the application"""
        arcade.exit()

    def get_view(self):
        """Get the menu view"""
        return self.view
