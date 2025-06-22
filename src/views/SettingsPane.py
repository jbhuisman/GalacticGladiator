import arcade
import arcade.gui
from config import BACKGROUND_COLOR


class SettingsPane(arcade.View):
    """Settings view pane"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.setup_ui()

    def setup_ui(self):
        """Setup settings UI"""
        # Create vertical box layout
        v_box = arcade.gui.UIBoxLayout()

        # Title
        title = arcade.gui.UILabel(text="SETTINGS",
                                   font_size=24,
                                   text_color=arcade.color.WHITE)
        v_box.add(title)
        v_box.add(arcade.gui.UISpace(height=40))

        # Volume setting
        self.volume_label = arcade.gui.UILabel(text="Volume: 50%",
                                               font_size=16,
                                               text_color=arcade.color.WHITE)
        v_box.add(self.volume_label)
        v_box.add(arcade.gui.UISpace(height=30))

        # Back button
        back_button = arcade.gui.UIFlatButton(text="Back to Menu",
                                              width=200,
                                              height=50)
        back_button.on_click = self.on_back_click
        v_box.add(back_button)

        # Use UIAnchorLayout to center the layout
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(child=v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)

    def update_volume_display(self, volume):
        """Update volume display"""
        self.volume_label.text = f"Volume: {volume}%"

    def on_back_click(self, event):
        """Handle back button click"""
        self.controller.show_menu()

    def on_draw(self):
        """Draw settings"""
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        """Handle key press"""
        if key == arcade.key.ESCAPE:
            self.controller.show_menu()

    def on_show_view(self):
        """Called when view is shown"""
        arcade.set_background_color(BACKGROUND_COLOR)