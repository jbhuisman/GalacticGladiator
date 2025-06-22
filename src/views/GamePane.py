import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from views.game.GameBoardPane import GameBoardPane
from views.game.GameUIPane import GameUIPane
from views.game.RightPane import GameInfoPane
from views.game.LeftPane import GameActionPane


class GamePane(arcade.View):
    """Main game view that coordinates all sub-panes"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Create sub-panes
        self.board_pane = GameBoardPane(controller)
        self.ui_pane = GameUIPane(controller)
        self.info_pane = GameInfoPane(controller)      # Right side - static legends
        self.action_pane = GameActionPane(controller)  # Left side - dynamic actions

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks"""
        # Let UIManager handle its events first
        if hasattr(self.ui_pane, 'manager') and self.ui_pane.manager:
            # Check if the UI manager wants to handle this event
            # by temporarily enabling it just for this event
            if self._ui_manager_wants_event(x, y):
                # Let the UI manager handle it - don't pass to our handlers
                return
        
        # Check if click is on action pane buttons (left side)
        if x < 320:  # Left pane area
            self.action_pane.on_mouse_press(x, y, button, modifiers)
        else:
            # Check if click is on board
            cell = self.board_pane.get_cell_from_mouse(x, y)
            if cell:
                self.controller.handle_cell_click(cell)

    def _ui_manager_wants_event(self, x, y):
        """Check if UI manager should handle this mouse event"""
        # Check if click is in top UI area (where buttons are)
        if y > SCREEN_HEIGHT - 60:  # Top 60 pixels
            return True
        # Check if click is in bottom UI area (where instructions are)
        if y < 40:  # Bottom 40 pixels
            return True
        return False

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse release"""
        if x < 320:  # Left pane area
            self.action_pane.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse motion"""
        if x < 320:  # Left pane area
            self.action_pane.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        """Draw the complete game view"""
        self.clear()

        # Draw all panes
        self.action_pane.draw()   # Left side first
        self.board_pane.draw()
        self.info_pane.draw()     # Right side
        self.ui_pane.draw()       # Top/bottom UI

    def on_update(self, delta_time):
        """Update game logic"""
        self.controller.update(delta_time)
        self.ui_pane.update_ui()

    def on_key_press(self, key, modifiers):
        """Handle key press"""
        if key == arcade.key.ESCAPE:
            # ESC now quits the game directly
            arcade.exit()
        elif key == arcade.key.SPACE:
            # Activate special ability (alternative to button)
            if (self.controller.model.selected_unit and 
                self.controller.model.game_phase == 'playing' and 
                self.controller.model.current_player == 'human'):
                self.controller.use_special_ability()
        elif key == arcade.key.ENTER:
            # End turn (alternative to button)
            if (self.controller.model.game_phase == 'playing' and 
                self.controller.model.current_player == 'human'):
                self.controller.end_turn()

    def on_show_view(self):
        """Called when view is shown"""
        arcade.set_background_color(BACKGROUND_COLOR)