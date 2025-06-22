import arcade
import arcade.gui


class GameUIPane:
    """Handles the top UI elements and instructions"""

    def __init__(self, controller):
        self.controller = controller
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
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

        # Actions remaining display
        self.actions_label = arcade.gui.UILabel(text="Actions: 2/2",
                                                font_size=16,
                                                text_color=arcade.color.YELLOW)
        h_box.add(self.actions_label)
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

        # Quit button (replaces Menu button)
        quit_button = arcade.gui.UIFlatButton(text="QUIT",
                                              width=100,
                                              height=40)
        quit_button.on_click = self.on_quit_click
        h_box.add(quit_button)

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

        # Update actions remaining
        if model.game_phase == 'playing':
            self.actions_label.text = f"Actions: {model.actions_remaining}/{model.max_actions_per_turn}"
        else:
            self.actions_label.text = "Actions: -/-"

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
                ability_mode = ""
                if model.rally_mode:
                    ability_mode = " (RALLY MODE)"
                elif model.infiltration_mode:
                    ability_mode = " (INFILTRATION MODE)"
                elif model.long_range_mode:
                    ability_mode = " (LONG RANGE MODE)"

                self.instructions_label.text = f"Click green cells to move, red cells to attack{ability_mode}"
            else:
                self.instructions_label.text = f"Click your units to select them (Actions: {model.actions_remaining})"
        else:
            self.instructions_label.text = "Waiting for AI..."

    def on_quit_click(self, event):
        """Handle quit button click"""
        arcade.exit()

    def draw(self):
        """Draw the UI"""
        self.manager.draw()