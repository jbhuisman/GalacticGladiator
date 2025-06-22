from models.GameModel import GameModel
from views.GamePane import GamePane


class GameController:
    """Controller for Galactic Gladiators game interactions"""

    def __init__(self, window):
        self.window = window
        self.model = GameModel()
        self.view = GamePane(self)

    def update(self, delta_time):
        """Update game state"""
        # Game logic is handled by user actions and AI turns
        pass

    def show_menu(self):
        """Return to main menu"""
        from controllers.MenuController import MenuController
        menu_controller = MenuController(self.window)
        self.window.show_view(menu_controller.get_view())

    def get_board_state(self):
        """Get current board state"""
        return self.model.get_board_state()

    def handle_cell_click(self, cell):
        """Handle cell click on board"""
        self.model.handle_cell_click(cell)

    def get_view(self):
        """Get the game view"""
        return self.view