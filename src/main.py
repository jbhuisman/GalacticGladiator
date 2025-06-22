import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from controllers.GameController import GameController


class GameWindow(arcade.Window):
    """Main application window"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Start directly with game controller
        game_controller = GameController(self)
        self.show_view(game_controller.view)


def main():
    """Main function to start the game"""
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()