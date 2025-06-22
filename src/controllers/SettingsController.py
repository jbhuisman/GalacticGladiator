from models.SettingsModel import SettingsModel
from views.SettingsPane import SettingsPane


class SettingsController:
    """Controller for settings interactions"""

    def __init__(self, window):
        self.window = window
        self.model = SettingsModel()
        self.view = SettingsPane(self)
        self.view.update_volume_display(self.model.get_volume())

    def show_menu(self):
        """Return to main menu"""
        from controllers.MenuController import MenuController
        menu_controller = MenuController(self.window)
        self.window.show_view(menu_controller.view)

    def change_volume(self, volume):
        """Change volume setting"""
        self.model.set_volume(volume)
        self.view.update_volume_display(self.model.get_volume())

    def get_view(self):
        """Get the settings view"""
        return self.view
