import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class GameStatsPane:
    """Separate pane for game statistics"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.margin = 15
        self.background_color = (40, 80, 60)  # Green-ish

        # Larger height for bigger text
        self.height = 140

        # Create text objects with much larger fonts
        self.title = arcade.Text("Game Status", self.x + self.margin, self.y + self.height - 35, arcade.color.WHITE,
                                 font_size=18, bold=True)

        # Game stats text objects
        self.gold_human_text = arcade.Text("", self.x + self.margin, self.y + self.height - 65, arcade.color.GOLD,
                                           font_size=16, bold=True)
        self.gold_ai_text = arcade.Text("", self.x + self.margin, self.y + self.height - 85, arcade.color.ORANGE,
                                        font_size=16, bold=True)
        self.units_remaining_text = arcade.Text("", self.x + self.margin, self.y + self.height - 110,
                                                arcade.color.WHITE, font_size=16, bold=True)
        self.ai_units_text = arcade.Text("", self.x + self.margin, self.y + self.height - 130, arcade.color.RED,
                                         font_size=16, bold=True)

    def draw(self, controller):
        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        # Update text objects
        model = controller.model
        self.gold_human_text.text = f"Your Gold: {model.gold_human}"
        self.gold_ai_text.text = f"AI Gold: {model.gold_ai}"

        if model.game_phase == 'setup':
            remaining = model.get_setup_remaining_count('human')
            self.units_remaining_text.text = f"Units to place: {remaining}"
            self.ai_units_text.text = ""
        else:
            human_units = len(model.get_remaining_units('human'))
            ai_units = len(model.get_remaining_units('ai'))
            self.units_remaining_text.text = f"Your units: {human_units}"
            self.ai_units_text.text = f"AI units: {ai_units}"

        # Draw all stats
        self.gold_human_text.draw()
        self.gold_ai_text.draw()
        self.units_remaining_text.draw()
        if self.ai_units_text.text:
            self.ai_units_text.draw()


class NextUnitPane:
    """Separate pane for next unit info"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.margin = 15
        self.background_color = (80, 60, 40)  # Brown-ish

        # Larger height for bigger text
        self.height = 160

        # Create text objects with much larger fonts
        self.title = arcade.Text("Next Unit to Place", self.x + self.margin, self.y + self.height - 35,
                                 arcade.color.CYAN, font_size=18, bold=True)

        # Dynamic text objects
        self.next_unit_type = arcade.Text("", self.x + self.margin + 45, self.y + self.height - 75, arcade.color.WHITE,
                                          font_size=16, bold=True)
        self.next_unit_rank = arcade.Text("", self.x + self.margin + 45, self.y + self.height - 100, arcade.color.WHITE,
                                          font_size=16, bold=True)
        self.next_unit_special = arcade.Text("", self.x + self.margin + 45, self.y + self.height - 125,
                                             arcade.color.YELLOW, font_size=14, bold=True)

    def draw(self, controller):
        # Only draw during human setup phase
        if not (controller.model.game_phase == 'setup' and controller.model.setup_phase == 'human'):
            return

        next_unit = controller.model.get_next_setup_unit('human')
        if not next_unit:
            return

        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        # Draw larger unit preview circle
        arcade.draw_circle_filled(self.x + self.margin + 20, self.y + self.height - 70, 18, arcade.color.BLUE)
        arcade.draw_circle_outline(self.x + self.margin + 20, self.y + self.height - 70, 18, arcade.color.WHITE, 2)

        # Draw rank in circle with larger font
        rank_preview = arcade.Text(str(next_unit.rank), self.x + self.margin + 20, self.y + self.height - 70,
                                   arcade.color.WHITE, font_size=14, bold=True, anchor_x="center", anchor_y="center")
        rank_preview.draw()

        # Update and draw unit details
        self.next_unit_type.text = f"Type: {next_unit.unit_type.title()}"
        self.next_unit_rank.text = f"Rank: {next_unit.rank}"

        if next_unit.special_ability:
            self.next_unit_special.text = f"Special: {next_unit.special_ability}"
        else:
            self.next_unit_special.text = ""

        self.next_unit_type.draw()
        self.next_unit_rank.draw()
        if self.next_unit_special.text:
            self.next_unit_special.draw()


class SelectedUnitPane:
    """Pane showing selected unit and available actions - ALWAYS VISIBLE AT BOTTOM"""

    def __init__(self, x, y, width, controller):
        self.x = x
        self.y = y
        self.width = width
        self.controller = controller
        self.margin = 15
        self.background_color = (60, 80, 100)  # Blue-ish

        # Fixed height - always visible
        self.height = 160  # Increased to fit text and buttons with more space

        # Create UI manager for buttons
        self.ui_manager = arcade.gui.UIManager()

        # Create text objects - positioned at top of pane
        self.title = arcade.Text("Unit Actions", self.x + self.margin, self.y + self.height - 25, arcade.color.WHITE,
                                 font_size=16, bold=True)
        self.unit_info = arcade.Text("", self.x + self.margin, self.y + self.height - 50, arcade.color.WHITE,
                                     font_size=14, bold=True)
        self.ability_info = arcade.Text("", self.x + self.margin, self.y + self.height - 70, arcade.color.YELLOW,
                                        font_size=12)

        self.setup_buttons()

    def setup_buttons(self):
        """Setup action buttons - POSITIONED AT VERY BOTTOM OF PANE"""
        # Create vertical layout for buttons
        v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=5)

        # Special ability button
        self.ability_button = arcade.gui.UIFlatButton(
            text="Use Special Ability",
            width=self.width - 2 * self.margin - 10,
            height=25
        )
        self.ability_button.on_click = self.on_ability_click
        v_box.add(self.ability_button)

        # End turn button
        self.end_turn_button = arcade.gui.UIFlatButton(
            text="End Turn",
            width=self.width - 2 * self.margin - 10,
            height=25
        )
        self.end_turn_button.on_click = self.on_end_turn_click
        v_box.add(self.end_turn_button)

        # Position buttons at VERY BOTTOM of pane - even lower than before
        button_anchor = arcade.gui.UIAnchorLayout()
        button_anchor.add(child=v_box, anchor_x="left", anchor_y="bottom",
                          align_x=self.x + self.margin + 5, align_y=self.y + 5)  # Even lower
        self.ui_manager.add(button_anchor)

    def on_ability_click(self, event):
        """Handle special ability button click"""
        if (self.controller.model.selected_unit and
                self.controller.model.game_phase == 'playing' and
                self.controller.model.current_player == 'human'):
            success = self.controller.use_special_ability()
            if not success:
                print("Special ability could not be used!")

    def on_end_turn_click(self, event):
        """Handle end turn button click"""
        if (self.controller.model.game_phase == 'playing' and
                self.controller.model.current_player == 'human'):
            self.controller.end_turn()

    def update_buttons(self):
        """Update button states based on game state"""
        model = self.controller.model

        # Update ability button
        if (model.selected_unit and model.game_phase == 'playing' and
                model.current_player == 'human' and model.selected_unit.special_ability and
                not model.selected_unit.special_used):
            self.ability_button.disabled = False
            # Check if on cover tile
            if model.selected_unit.position and model.selected_unit.position in model.special_tiles:
                tile = model.special_tiles[model.selected_unit.position]
                if tile.blocks_special_abilities():
                    self.ability_button.disabled = True
        else:
            self.ability_button.disabled = True

        # Update end turn button
        if model.game_phase == 'playing' and model.current_player == 'human':
            self.end_turn_button.disabled = False
        else:
            self.end_turn_button.disabled = True

    def draw(self, controller):
        # ALWAYS DRAW THE PANE
        model = controller.model

        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        # Only show content if unit is selected AND it's human's unit
        if (model.selected_unit and model.selected_unit.owner == 'human' and
                model.game_phase == 'playing'):

            unit = model.selected_unit

            # Update and draw unit info
            self.unit_info.text = f"{unit.unit_type.title()} (Rank {unit.rank})"
            self.unit_info.draw()

            # Update ability info
            if unit.special_ability:
                if unit.special_used:
                    self.ability_info.text = f"{unit.special_ability.title()}: GEBRUIKT"
                    self.ability_info.color = arcade.color.RED
                else:
                    # Check if blocked by cover
                    blocked = False
                    if unit.position and unit.position in model.special_tiles:
                        tile = model.special_tiles[unit.position]
                        if tile.blocks_special_abilities():
                            blocked = True

                    if blocked:
                        self.ability_info.text = f"{unit.special_ability.title()}: GEBLOKKEERD"
                        self.ability_info.color = arcade.color.ORANGE
                    else:
                        self.ability_info.text = f"{unit.special_ability.title()}: BESCHIKBAAR"
                        self.ability_info.color = arcade.color.GREEN
            else:
                self.ability_info.text = "Geen speciale vaardigheid"
                self.ability_info.color = arcade.color.GRAY

            self.ability_info.draw()
        else:
            # EMPTY CONTENT - no text when no unit selected
            # Don't draw unit_info or ability_info
            pass

        # Update button states and draw (always visible but may be disabled)
        self.update_buttons()
        self.ui_manager.draw()


class GameActionPane:
    """Main action panel on the left side (dynamic content only)"""

    def __init__(self, controller):
        self.controller = controller
        self.pane_width = 320
        self.x_offset = 0
        self.margin = 10
        self.pane_spacing = 12

        # Create panes with dynamic positioning
        self._create_panes()

    def _create_panes(self):
        """Create panes and calculate their positions"""
        pane_width = self.pane_width - 2 * self.margin

        # SELECTED UNIT PANE ALWAYS AT BOTTOM
        selected_unit_height = 160  # Match the height in SelectedUnitPane
        self.selected_unit_pane = SelectedUnitPane(
            self.x_offset + self.margin,
            self.margin,  # At the very bottom
            pane_width,
            self.controller
        )

        # OTHER PANES START FROM TOP AND WORK DOWN
        current_y = SCREEN_HEIGHT - self.margin

        # Game Stats pane (TOP)
        temp_game_stats = GameStatsPane(0, 0, pane_width)
        current_y -= temp_game_stats.height
        self.game_stats_pane = GameStatsPane(self.x_offset + self.margin, current_y, pane_width)

        # Next Unit pane (BELOW GAME STATS)
        current_y -= self.pane_spacing
        temp_next_unit = NextUnitPane(0, 0, pane_width)
        current_y -= temp_next_unit.height
        self.next_unit_pane = NextUnitPane(self.x_offset + self.margin, current_y, pane_width)

    def draw(self):
        """Draw the complete action pane"""
        # Draw main background
        arcade.draw_lbwh_rectangle_filled(self.x_offset, 0, self.pane_width, SCREEN_HEIGHT, (25, 25, 35))

        # Draw right border
        arcade.draw_line(self.pane_width, 0, self.pane_width, SCREEN_HEIGHT, arcade.color.WHITE, 3)

        # Draw all sub-panes
        self.game_stats_pane.draw(self.controller)  # Top
        self.next_unit_pane.draw(self.controller)  # Middle (when visible)
        self.selected_unit_pane.draw(self.controller)  # Bottom (always visible)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse press for UI elements"""
        self.selected_unit_pane.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse release for UI elements"""
        self.selected_unit_pane.ui_manager.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse motion for UI elements"""
        self.selected_unit_pane.ui_manager.on_mouse_motion(x, y, dx, dy)