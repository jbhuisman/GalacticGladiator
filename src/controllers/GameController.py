import arcade

from models.GameModel import GameModel
from views.GamePane import GamePane


class GameController:
    """Controller for Galactic Gladiators game interactions"""
    
    # Singleton pattern to prevent multiple instances
    _instance = None

    def __new__(cls, window):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, window):
        # Prevent re-initialization
        if hasattr(self, 'initialized'):
            self.window = window  # Update window reference
            return
            
        self.window = window
        self.model = GameModel(load_from_save=True)  # Try to load autosave
        self.view = GamePane(self)
        self.initialized = True

    def new_game(self):
        """Force start new game"""
        self.model = GameModel(load_from_save=False)
        self.view = GamePane(self)

    def update(self, delta_time):
        """Update game state"""
        # Game logic is handled by user actions and AI turns
        pass

    def show_menu(self):
        """Quit the application (no menu anymore)"""
        # Autosave before quitting
        if self.model:
            self.model.autosave()
        arcade.exit()

    def get_board_state(self):
        """Get current board state"""
        return self.model.get_board_state()

    def handle_cell_click(self, cell):
        """Handle cell click on board"""
        result = self.model.handle_cell_click(cell)
        # Autosave after important actions
        if result and self.model.game_phase == 'playing':
            self.model.autosave()
        return result

    def use_special_ability(self):
        """Use special ability of selected unit"""
        if not self.model.selected_unit:
            return False
            
        result = self.model.activate_special_ability(self.model.selected_unit)
        if result:
            self.model.autosave()
        return result
    
    def end_turn(self):
        """End current player's turn"""
        if (self.model.game_phase == 'playing' and 
            self.model.current_player == 'human'):
            self.model.end_turn()

    def get_view(self):
        """Get the game view"""
        return self.view

    @classmethod
    def reset_instance(cls):
        """Reset singleton for new game"""
        cls._instance = None