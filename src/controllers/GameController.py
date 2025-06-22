from models.GameModel import GameModel
from views.GamePane import GamePane


class GameController:
    """Controller for game interactions"""

    def __init__(self, window):
        self.window = window
        self.model = GameModel()
        self.view = GamePane(self)

    def update(self, delta_time):
        """Update game state"""
        self.model.update(delta_time)
        self.view.update_score(self.model.get_score())

    def toggle_pause(self):
        """Toggle game pause"""
        self.model.toggle_pause()
        self.view.update_pause_button(self.model.is_game_paused())

    def show_menu(self):
        """Return to main menu"""
        from controllers.MenuController import MenuController
        menu_controller = MenuController(self.window)
        self.window.show_view(menu_controller.view)

    def get_view(self):
        """Get the game view"""
        return self.view
