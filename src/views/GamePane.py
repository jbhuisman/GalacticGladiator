import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR


class GamePane(arcade.View):
    """Main game view pane"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.setup_ui()

    def setup_ui(self):
        """Setup game UI elements"""
        # Create horizontal layout for top UI
        h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Score display
        self.score_label = arcade.gui.UILabel(text="Score: 0",
                                              font_size=16,
                                              text_color=arcade.color.WHITE)
        h_box.add(self.score_label)
        h_box.add(arcade.gui.UISpace(width=20))

        # Pause button
        self.pause_button = arcade.gui.UIFlatButton(text="Pause",
                                                    width=100,
                                                    height=40)
        self.pause_button.on_click = self.on_pause_click
        h_box.add(self.pause_button)
        h_box.add(arcade.gui.UISpace(width=10))

        # Menu button
        menu_button = arcade.gui.UIFlatButton(text="Menu",
                                              width=100,
                                              height=40)
        menu_button.on_click = self.on_menu_click
        h_box.add(menu_button)

        # Use UIAnchorLayout to position at top left
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(child=h_box, anchor_x="left", anchor_y="top",
                         align_x=10, align_y=-10)
        self.manager.add(anchor_layout)

    def update_score(self, score):
        """Update score display"""
        self.score_label.text = f"Score: {score}"

    def update_pause_button(self, is_paused):
        """Update pause button text"""
        self.pause_button.text = "Resume" if is_paused else "Pause"

    def on_pause_click(self, event):
        """Handle pause button click"""
        self.controller.toggle_pause()

    def on_menu_click(self, event):
        """Handle menu button click"""
        self.controller.show_menu()

    def on_draw(self):
        """Draw the game"""
        self.clear()

        # Draw game elements
        arcade.draw_text("Game Area - Add your game graphics here",
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

        # Draw UI
        self.manager.draw()

    def on_update(self, delta_time):
        """Update game logic"""
        self.controller.update(delta_time)

    def on_key_press(self, key, modifiers):
        """Handle key press"""
        if key == arcade.key.ESCAPE:
            self.controller.show_menu()

    def on_show_view(self):
        """Called when view is shown"""
        arcade.set_background_color(BACKGROUND_COLOR)
