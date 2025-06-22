 
import arcade
import arcade.gui
from config import BACKGROUND_COLOR


class MenuPane(arcade.View):
    """Main menu view pane"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.setup_ui()

    def setup_ui(self):
        """Setup menu UI elements"""
        # Create a vertical box to center elements
        v_box = arcade.gui.UIBoxLayout()

        # Title
        title = arcade.gui.UILabel(text="GALACTIC GLADIATOR",
                                   font_size=24,
                                   text_color=arcade.color.WHITE)
        v_box.add(title)
        v_box.add(arcade.gui.UISpace(height=30))

        # Start button
        start_button = arcade.gui.UIFlatButton(text="Start Game",
                                               width=200,
                                               height=50)
        start_button.on_click = self.on_start_click
        v_box.add(start_button)
        v_box.add(arcade.gui.UISpace(height=20))

        # Settings button
        settings_button = arcade.gui.UIFlatButton(text="Settings",
                                                  width=200,
                                                  height=50)
        settings_button.on_click = self.on_settings_click
        v_box.add(settings_button)
        v_box.add(arcade.gui.UISpace(height=20))

        # Quit button
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=200,
                                              height=50)
        quit_button.on_click = self.on_quit_click
        v_box.add(quit_button)

        # Use UIAnchorLayout to center the v_box
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(child=v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)

    def on_start_click(self, event):
        """Handle start button click"""
        self.controller.start_game()

    def on_settings_click(self, event):
        """Handle settings button click"""
        self.controller.show_settings()

    def on_quit_click(self, event):
        """Handle quit button click"""
        self.controller.quit_game()

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        """Called when view is shown"""
        arcade.set_background_color(BACKGROUND_COLOR)