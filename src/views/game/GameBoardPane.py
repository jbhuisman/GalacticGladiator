import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class GameBoardPane:
    """Handles drawing of the game board and units"""
    
    def __init__(self, controller):
        self.controller = controller
        
        # Board settings - Centered between two side panes
        self.left_pane_width = 320   # Left action pane
        self.right_pane_width = 350  # Right info pane
        self.board_size = 10
        self.board_margin = 20  # Reduced margin for better centering
        
        # Calculate available space in the middle
        available_width = SCREEN_WIDTH - self.left_pane_width - self.right_pane_width - 2 * self.board_margin
        available_height = SCREEN_HEIGHT - 150 - 2 * self.board_margin
        self.cell_size = min(available_width // self.board_size, available_height // self.board_size)
        
        # Calculate total board size
        total_board_width = self.board_size * self.cell_size
        total_board_height = self.board_size * self.cell_size
        
        # Center the board in the available middle space
        middle_space_start = self.left_pane_width
        middle_space_width = SCREEN_WIDTH - self.left_pane_width - self.right_pane_width
        
        self.board_start_x = middle_space_start + (middle_space_width - total_board_width) // 2
        self.board_start_y = (SCREEN_HEIGHT - total_board_height) // 2 - 25  # Slight offset for UI
        
        # Unit text cache for performance
        self.unit_text_cache = {}
        
    def draw_board_grid(self):
        """Draw the game board grid"""
        # Draw board background
        arcade.draw_lbwh_rectangle_filled(
            self.board_start_x,
            self.board_start_y,
            self.board_size * self.cell_size,
            self.board_size * self.cell_size,
            arcade.color.DARK_GRAY
        )

        # Highlight setup rows
        if self.controller.model.game_phase == 'setup':
            if self.controller.model.setup_phase == 'human':
                # Highlight rows 0 and 1 (which are at the TOP visually)
                for logical_row in [0, 1]:
                    visual_row = self.board_size - 1 - logical_row
                    arcade.draw_lbwh_rectangle_filled(
                        self.board_start_x,
                        self.board_start_y + visual_row * self.cell_size,
                        self.board_size * self.cell_size,
                        self.cell_size,
                        (0, 0, 139, 80)  # DARK_BLUE with alpha
                    )

        # Draw grid lines
        for i in range(self.board_size + 1):
            # Vertical lines
            arcade.draw_line(
                self.board_start_x + i * self.cell_size,
                self.board_start_y,
                self.board_start_x + i * self.cell_size,
                self.board_start_y + self.board_size * self.cell_size,
                arcade.color.WHITE,
                1
            )
            # Horizontal lines
            arcade.draw_line(
                self.board_start_x,
                self.board_start_y + i * self.cell_size,
                self.board_start_x + self.board_size * self.cell_size,
                self.board_start_y + i * self.cell_size,
                arcade.color.WHITE,
                1
            )
    
    def draw_special_tiles(self):
        """Draw special tiles in middle section"""
        for position, tile in self.controller.model.special_tiles.items():
            logical_row, col = position
            visual_row = self.board_size - 1 - logical_row
            
            colors = {
                'elevated': (139, 69, 19, 150),  # BROWN
                'cover': (0, 100, 0, 150),  # DARK_GREEN  
                'sensor': (128, 0, 128, 150),  # PURPLE
                'goldmine': (255, 165, 0, 150)  # ORANGE
            }

            color = colors.get(tile.tile_type, (128, 128, 128, 150))

            # Draw tile background
            arcade.draw_lbwh_rectangle_filled(
                self.board_start_x + col * self.cell_size + 2,
                self.board_start_y + visual_row * self.cell_size + 2,
                self.cell_size - 4,
                self.cell_size - 4,
                color
            )
    
    def draw_valid_actions(self):
        """Draw highlights for valid moves and attacks"""
        if self.controller.model.game_phase == 'playing':
            # Highlight valid moves in green
            for position in self.controller.model.valid_moves:
                logical_row, col = position
                visual_row = self.board_size - 1 - logical_row
                arcade.draw_lbwh_rectangle_filled(
                    self.board_start_x + col * self.cell_size + 2,
                    self.board_start_y + visual_row * self.cell_size + 2,
                    self.cell_size - 4,
                    self.cell_size - 4,
                    (0, 255, 0, 100)  # GREEN with alpha
                )

            # Highlight valid attacks in red
            for position in self.controller.model.valid_attacks:
                logical_row, col = position
                visual_row = self.board_size - 1 - logical_row
                arcade.draw_lbwh_rectangle_filled(
                    self.board_start_x + col * self.cell_size + 2,
                    self.board_start_y + visual_row * self.cell_size + 2,
                    self.cell_size - 4,
                    self.cell_size - 4,
                    (255, 0, 0, 100)  # RED with alpha
                )

            # Highlight selected unit
            if self.controller.model.selected_position:
                logical_row, col = self.controller.model.selected_position
                visual_row = self.board_size - 1 - logical_row
                arcade.draw_lbwh_rectangle_outline(
                    self.board_start_x + col * self.cell_size + 1,
                    self.board_start_y + visual_row * self.cell_size + 1,
                    self.cell_size - 2,
                    self.cell_size - 2,
                    arcade.color.YELLOW,
                    3
                )

            # Show special ability modes
            model = self.controller.model
            if model.rally_mode:
                # Show rally indicator
                arcade.draw_text("RALLY MODE ACTIVE", 
                               self.board_start_x, 
                               self.board_start_y - 30,
                               arcade.color.YELLOW, 16)
            elif model.infiltration_mode:
                # Show infiltration indicator
                arcade.draw_text("INFILTRATION MODE ACTIVE", 
                               self.board_start_x, 
                               self.board_start_y - 30,
                               arcade.color.GREEN, 16)
            elif model.long_range_mode:
                # Show long range indicator
                arcade.draw_text("LONG RANGE MODE ACTIVE", 
                               self.board_start_x, 
                               self.board_start_y - 30,
                               arcade.color.RED, 16)
    
    def draw_units(self):
        """Draw game units on the board"""
        board_state = self.controller.get_board_state()

        for position, unit in board_state.items():
            logical_row, col = position
            visual_row = self.board_size - 1 - logical_row
            
            center_x = self.board_start_x + col * self.cell_size + self.cell_size // 2
            center_y = self.board_start_y + visual_row * self.cell_size + self.cell_size // 2

            # Unit colors - Add special effects
            if unit.owner == 'human':
                color = arcade.color.BLUE
                text_color = arcade.color.WHITE
            else:
                color = arcade.color.RED
                text_color = arcade.color.WHITE
            
            # Special visual effects for abilities
            if hasattr(unit, 'stealth_active') and unit.stealth_active:
                color = (*color[:3], 128)  # Make transparent for stealth
            if hasattr(unit, 'protected_by_shield') and unit.protected_by_shield:
                # Draw shield effect
                arcade.draw_circle_outline(center_x, center_y, self.cell_size // 3 + 5, arcade.color.CYAN, 3)

            # Draw unit background
            arcade.draw_circle_filled(center_x, center_y, self.cell_size // 3, color)
            arcade.draw_circle_outline(center_x, center_y, self.cell_size // 3, arcade.color.BLACK, 2)

            # Create text cache key
            text_key = (position, unit.owner, unit.rank if unit.owner == 'human' else unit.get_display_char() if unit.is_revealed else "")
            
            if text_key not in self.unit_text_cache:
                if unit.owner == 'human':
                    display_text = str(unit.rank)
                else:
                    # FOG OF WAR: Only show revealed enemy units
                    display_text = unit.get_display_char() if unit.is_revealed else "?"
                
                if display_text:
                    self.unit_text_cache[text_key] = arcade.Text(
                        display_text, center_x, center_y, text_color,
                        font_size=16 if unit.owner == 'human' else 14,
                        anchor_x="center", anchor_y="center"
                    )

            # Draw text if it exists
            if text_key in self.unit_text_cache and self.unit_text_cache[text_key].text:
                self.unit_text_cache[text_key].draw()
    
    def get_cell_from_mouse(self, x, y):
        """Convert mouse coordinates to board cell"""
        if (self.board_start_x <= x <= self.board_start_x + self.board_size * self.cell_size and
                self.board_start_y <= y <= self.board_start_y + self.board_size * self.cell_size):

            col = (x - self.board_start_x) // self.cell_size
            visual_row = (y - self.board_start_y) // self.cell_size
            
            # Convert visual row to logical row (flip Y-axis)
            logical_row = self.board_size - 1 - visual_row

            if 0 <= logical_row < self.board_size and 0 <= col < self.board_size:
                return (logical_row, col)
        return None
    
    def draw(self):
        """Draw the complete board"""
        self.draw_board_grid()
        self.draw_special_tiles()
        self.draw_valid_actions()
        self.draw_units()