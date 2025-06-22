class MenuModel:
    """Model for menu state and data"""

    def __init__(self):
        self.current_selection = 0
        self.menu_items = ["Start Game", "Settings", "Quit"]

    def get_menu_items(self):
        """Get list of menu items"""
        return self.menu_items

    def set_selection(self, index):
        """Set current menu selection"""
        if 0 <= index < len(self.menu_items):
            self.current_selection = index

    def get_selection(self):
        """Get current menu selection"""
        return self.current_selection

    def get_selected_item(self):
        """Get currently selected menu item"""
        return self.menu_items[self.current_selection]
