import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from controllers.MenuController import MenuController


class GameWindow(arcade.Window):
    """Main application window"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Start with menu controller
        menu_controller = MenuController(self)
        self.show_view(menu_controller.get_view())


def main():
    """Main function to start the game"""
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()