import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR


class GamePane(arcade.View):
    """Main game view pane for Galactic Gladiators"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Game board settings for 10x10
        self.board_size = 10  # 10x10 grid
        self.board_margin = 50
        self.cell_size = min((SCREEN_WIDTH - 2 * self.board_margin) // self.board_size,
                             (SCREEN_HEIGHT - 150 - 2 * self.board_margin) // self.board_size)
        self.board_start_x = (SCREEN_WIDTH - self.board_size * self.cell_size) // 2
        self.board_start_y = (SCREEN_HEIGHT - self.board_size * self.cell_size) // 2 - 25

        self.setup_ui()

    def setup_ui(self):
        """Setup game UI elements"""
        # Create horizontal layout for top UI
        h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Game phase display
        self.phase_label = arcade.gui.UILabel(text="Setup Phase",
                                              font_size=16,
                                              text_color=arcade.color.WHITE)
        h_box.add(self.phase_label)
        h_box.add(arcade.gui.UISpace(width=20))

        # Current player display
        self.player_label = arcade.gui.UILabel(text="Your Turn",
                                               font_size=16,
                                               text_color=arcade.color.CYAN)
        h_box.add(self.player_label)
        h_box.add(arcade.gui.UISpace(width=20))

        # Gold display
        self.gold_label = arcade.gui.UILabel(text="Gold: 0",
                                             font_size=16,
                                             text_color=arcade.color.GOLD)
        h_box.add(self.gold_label)
        h_box.add(arcade.gui.UISpace(width=20))

        # Units remaining in setup
        self.units_label = arcade.gui.UILabel(text="Units to place: 20",
                                              font_size=16,
                                              text_color=arcade.color.WHITE)
        h_box.add(self.units_label)
        h_box.add(arcade.gui.UISpace(width=20))

        # Menu button
        menu_button = arcade.gui.UIFlatButton(text="Menu",
                                              width=100,
                                              height=40)
        menu_button.on_click = self.on_menu_click
        h_box.add(menu_button)

        # Use UIAnchorLayout to position at top
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(child=h_box, anchor_x="center_x", anchor_y="top",
                          align_y=-10)
        self.manager.add(anchor_layout)

        # Instructions label at bottom
        self.instructions_label = arcade.gui.UILabel(
            text="Setup: Click empty cells in your rows to place units",
            font_size=12,
            text_color=arcade.color.LIGHT_GRAY
        )

        # Add instructions to bottom
        instructions_anchor = arcade.gui.UIAnchorLayout()
        instructions_anchor.add(child=self.instructions_label, anchor_x="center_x", anchor_y="bottom",
                                align_y=10)
        self.manager.add(instructions_anchor)

    def draw_game_board(self):
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

        # Draw special tiles
        self.draw_special_tiles()

        # Draw valid moves/attacks
        self.draw_valid_actions()

    def draw_special_tiles(self):
        """Draw special tiles in middle section"""
        for position, tile in self.controller.model.special_tiles.items():
            logical_row, col = position
            visual_row = self.board_size - 1 - logical_row
            
            center_x = self.board_start_x + col * self.cell_size + self.cell_size // 2
            center_y = self.board_start_y + visual_row * self.cell_size + self.cell_size // 2

            # Different colors for different tile types
            colors = {
                'elevated': (139, 69, 19, 100),  # BROWN - C in ASCII
                'cover': (0, 100, 0, 100),  # DARK_GREEN - P in ASCII  
                'sensor': (128, 0, 128, 100),  # PURPLE - R in ASCII
                'goldmine': (255, 165, 0, 100)  # ORANGE - Y in ASCII
            }

            color = colors.get(tile.tile_type, (128, 128, 128, 100))

            # Draw tile background
            arcade.draw_lbwh_rectangle_filled(
                self.board_start_x + col * self.cell_size + 2,
                self.board_start_y + visual_row * self.cell_size + 2,
                self.cell_size - 4,
                self.cell_size - 4,
                color
            )

            # Draw tile symbol matching ASCII diagram
            symbols = {
                'elevated': 'C',  # Verhoogde positie
                'cover': 'P',     # Dekking
                'sensor': 'R',    # Sensor
                'goldmine': 'Y'   # Goudmijn
            }
            symbol = symbols.get(tile.tile_type, '?')

            arcade.draw_text(symbol, center_x, center_y, arcade.color.WHITE,
                             font_size=12, anchor_x="center", anchor_y="center")

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

    def draw_units(self):
        """Draw game units on the board"""
        board_state = self.controller.get_board_state()

        for position, unit in board_state.items():
            logical_row, col = position
            visual_row = self.board_size - 1 - logical_row
            
            center_x = self.board_start_x + col * self.cell_size + self.cell_size // 2
            center_y = self.board_start_y + visual_row * self.cell_size + self.cell_size // 2

            # Unit colors
            if unit.owner == 'human':
                color = arcade.color.BLUE
                text_color = arcade.color.WHITE
            else:
                color = arcade.color.RED
                text_color = arcade.color.WHITE

            # Draw unit background
            arcade.draw_circle_filled(center_x, center_y, self.cell_size // 3, color)
            arcade.draw_circle_outline(center_x, center_y, self.cell_size // 3, arcade.color.BLACK, 2)

            # For human units: always show rank number (like ASCII diagram)
            if unit.owner == 'human':
                # Show rank number as main symbol
                arcade.draw_text(str(unit.rank), center_x, center_y, text_color,
                                 font_size=16, anchor_x="center", anchor_y="center")
            else:
                # AI units show "B" (like ASCII diagram) unless revealed
                if unit.is_revealed:
                    symbol = unit.get_display_char()
                    arcade.draw_text(symbol, center_x, center_y, text_color,
                                     font_size=14, anchor_x="center", anchor_y="center")
                else:
                    # Hidden AI unit - show "B" like in ASCII diagram
                    arcade.draw_text("B", center_x, center_y, text_color,
                                     font_size=14, anchor_x="center", anchor_y="center")

    def draw_next_unit_info(self):
        """Draw info about next unit to place during setup"""
        if (self.controller.model.game_phase == 'setup' and
                self.controller.model.setup_phase == 'human'):

            next_unit = self.controller.model.get_next_setup_unit('human')
            if next_unit:
                # Draw unit info in corner
                info_x = SCREEN_WIDTH - 200
                info_y = SCREEN_HEIGHT - 100

                arcade.draw_text("Next Unit:", info_x, info_y + 30, arcade.color.WHITE, font_size=14)
                arcade.draw_text(f"{next_unit.unit_type.title()}", info_x, info_y + 10, arcade.color.WHITE,
                                 font_size=12)
                arcade.draw_text(f"Rank: {next_unit.rank}", info_x, info_y - 10, arcade.color.CYAN, font_size=14)

                if next_unit.special_ability:
                    arcade.draw_text(f"Special: {next_unit.special_ability}", info_x, info_y - 30,
                                     arcade.color.YELLOW, font_size=10)

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

    def update_ui(self):
        """Update UI elements based on game state"""
        model = self.controller.model

        # Update phase label
        if model.game_phase == 'setup':
            self.phase_label.text = f"Setup Phase - {model.setup_phase.title()}"
        elif model.game_phase == 'playing':
            self.phase_label.text = "Game Playing"
        else:
            self.phase_label.text = f"Game Over - {model.winner.title()} Wins!"

        # Update player label
        if model.game_phase == 'setup' and model.setup_phase == 'human':
            self.player_label.text = "Place Your Units"
        elif model.game_phase == 'setup':
            self.player_label.text = "AI Placing Units"
        elif model.current_player == 'human':
            self.player_label.text = "Your Turn"
        else:
            self.player_label.text = "AI Turn"

        # Update gold
        self.gold_label.text = f"Gold: {model.gold_human}"

        # Update units remaining
        if model.game_phase == 'setup':
            remaining = model.get_setup_remaining_count('human')
            self.units_label.text = f"Units to place: {remaining}"
        else:
            human_units = len(model.get_remaining_units('human'))
            ai_units = len(model.get_remaining_units('ai'))
            self.units_label.text = f"Your units: {human_units} | AI units: {ai_units}"

        # Update instructions
        if model.game_phase == 'setup' and model.setup_phase == 'human':
            self.instructions_label.text = "Click empty cells in TOP rows (0-1) to place your units"
        elif model.game_phase == 'playing' and model.current_player == 'human':
            if model.selected_unit:
                self.instructions_label.text = "Click green cells to move, red cells to attack"
            else:
                self.instructions_label.text = "Click your units (numbers) to select them"
        else:
            self.instructions_label.text = "Waiting for AI..."

    def on_menu_click(self, event):
        """Handle menu button click"""
        self.controller.show_menu()

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks on the board"""
        cell = self.get_cell_from_mouse(x, y)
        if cell:
            self.controller.handle_cell_click(cell)

    def on_draw(self):
        """Draw the game"""
        self.clear()

        # Draw game board
        self.draw_game_board()

        # Draw units
        self.draw_units()

        # Draw next unit info during setup
        self.draw_next_unit_info()

        # Draw UI
        self.manager.draw()

    def on_update(self, delta_time):
        """Update game logic"""
        self.controller.update(delta_time)
        self.update_ui()

    def on_key_press(self, key, modifiers):
        """Handle key press"""
        if key == arcade.key.ESCAPE:
            self.controller.show_menu()

    def on_show_view(self):
        """Called when view is shown"""
        arcade.set_background_color(BACKGROUND_COLOR)