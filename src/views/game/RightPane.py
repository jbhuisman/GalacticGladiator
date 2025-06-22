import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class LegendPane:
    """Separate pane for special tiles legend"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.margin = 15
        self.background_color = (60, 40, 80)  # Purple-ish

        # Calculate dynamic height based on content with larger spacing
        self.title_height = 60
        self.item_height = 50
        self.legend_items = [
            ('Verhoogde Positie', '+1 rang in gevecht'),
            ('Dekking', 'Immuun voor speciale vaardigheden'),
            ('Sensor', 'Toont type eenheid'),
            ('Goudmijn', '1 goudstuk na 3 beurten')
        ]
        self.height = self.title_height + (len(self.legend_items) * self.item_height) + self.margin

        # Create text objects with much larger fonts
        self.title = arcade.Text("Special Tiles Legend", self.x + self.margin, self.y + self.height - 35, arcade.color.WHITE, font_size=20, bold=True)

        self.legend_texts = []
        for i, (name, description) in enumerate(self.legend_items):
            y_pos = self.y + self.height - self.title_height - (i * self.item_height) - 20
            name_text = arcade.Text(name, self.x + self.margin + 45, y_pos + 12, arcade.color.WHITE, font_size=16, bold=True)
            desc_text = arcade.Text(description, self.x + self.margin + 45, y_pos - 12, arcade.color.LIGHT_GRAY, font_size=14)
            self.legend_texts.append((name_text, desc_text))

    def draw(self):
        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        # Legend colors
        legend_colors = [(139, 69, 19), (0, 100, 0), (128, 0, 128), (255, 165, 0)]

        for i, (name_text, desc_text) in enumerate(self.legend_texts):
            y_pos = self.y + self.height - self.title_height - (i * self.item_height) - 20
            color = legend_colors[i]

            # Draw larger color square
            arcade.draw_lbwh_rectangle_filled(self.x + self.margin, y_pos - 10, 30, 30, color)
            arcade.draw_lbwh_rectangle_outline(self.x + self.margin, y_pos - 10, 30, 30, arcade.color.WHITE, 2)

            # Draw text
            name_text.draw()
            desc_text.draw()

class UnitTypesPane:
    """Separate pane for unit types"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.margin = 15
        self.background_color = (40, 60, 80)  # Blue-ish

        # Calculate dynamic height based on content with larger spacing
        self.title_height = 60
        self.item_height = 40
        self.unit_info = [
            ('Flag (F)', 'Vlag - Verliezen = Game Over'),
            ('Scout (S)', 'Verkenner - Infiltratie'),
            ('Infantry (I)', 'Infanterie - Standaard troep'),
            ('Sniper (N)', 'Sluipschutter - Lange afstand'),
            ('Shield (H)', 'Schilddrager - Bescherming'),
            ('Warlord (W)', 'Krijgsheer - Verzamelen'),
            ('Commando (C)', 'Commando - Stealth')
        ]
        self.height = self.title_height + (len(self.unit_info) * self.item_height) + self.margin

        # Create text objects with much larger fonts
        self.title = arcade.Text("Unit Types", self.x + self.margin, self.y + self.height - 35, arcade.color.WHITE, font_size=20, bold=True)

        self.unit_type_texts = []
        for i, (name, description) in enumerate(self.unit_info):
            y_pos = self.y + self.height - self.title_height - (i * self.item_height) - 15
            name_text = arcade.Text(name, self.x + self.margin + 40, y_pos + 8, arcade.color.WHITE, font_size=15, bold=True)
            desc_text = arcade.Text(description, self.x + self.margin + 40, y_pos - 8, arcade.color.LIGHT_GRAY, font_size=13)
            self.unit_type_texts.append((name_text, desc_text))

    def draw(self):
        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        for i, (name_text, desc_text) in enumerate(self.unit_type_texts):
            y_pos = self.y + self.height - self.title_height - (i * self.item_height) - 15

            # Draw larger rank circle
            arcade.draw_circle_filled(self.x + self.margin + 18, y_pos, 15, arcade.color.BLUE)
            arcade.draw_circle_outline(self.x + self.margin + 18, y_pos, 15, arcade.color.WHITE, 2)

            # Draw rank number with larger font
            rank_text = arcade.Text(str(i), self.x + self.margin + 18, y_pos, arcade.color.WHITE, font_size=12, bold=True, anchor_x="center", anchor_y="center")
            rank_text.draw()

            # Draw text
            name_text.draw()
            desc_text.draw()


class SpecialAbilitiesPane:
    """Pane showing special abilities and their status"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.margin = 15
        self.background_color = (80, 40, 120)  # Purple-ish

        # Calculate dynamic height based on abilities ONLY - NO DYNAMIC CONTENT
        self.title_height = 60
        self.ability_height = 45
        self.abilities = [
            ('Infiltration', 'Scout - Beweeg door vijanden'),
            ('Long Range', 'Sniper - Aanval op afstand'),
            ('Protection', 'Shield - Bescherm bondgenoten'),
            ('Rally', 'Warlord - Neem units mee'),
            ('Stealth', 'Commando - Word onzichtbaar')
        ]
        self.height = self.title_height + (len(self.abilities) * self.ability_height) + self.margin

        # Create text objects - ONLY STATIC CONTENT
        self.title = arcade.Text("Special Abilities", self.x + self.margin, self.y + self.height - 35,
                                 arcade.color.WHITE, font_size=18, bold=True)

        self.ability_texts = []
        for i, (name, description) in enumerate(self.abilities):
            y_pos = self.y + self.height - self.title_height - (i * self.ability_height) - 20
            name_text = arcade.Text(name, self.x + self.margin + 35, y_pos + 10, arcade.color.WHITE, font_size=14,
                                    bold=True)
            desc_text = arcade.Text(description, self.x + self.margin + 35, y_pos - 10, arcade.color.LIGHT_GRAY,
                                    font_size=12)
            self.ability_texts.append((name_text, desc_text))

    def draw(self, controller):
        # Draw background
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_lbwh_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, 2)

        # Draw title
        self.title.draw()

        # Draw ability icons and descriptions - STATIC ONLY
        ability_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128)]

        for i, (name_text, desc_text) in enumerate(self.ability_texts):
            y_pos = self.y + self.height - self.title_height - (i * self.ability_height) - 20
            color = ability_colors[i]

            # Draw ability icon
            arcade.draw_circle_filled(self.x + self.margin + 15, y_pos, 12, color)
            arcade.draw_circle_outline(self.x + self.margin + 15, y_pos, 12, arcade.color.WHITE, 2)

            # Draw ability letter
            ability_letters = ['I', 'L', 'P', 'R', 'S']
            letter_text = arcade.Text(ability_letters[i], self.x + self.margin + 15, y_pos, arcade.color.WHITE,
                                      font_size=12, bold=True, anchor_x="center", anchor_y="center")
            letter_text.draw()

            # Draw text
            name_text.draw()
            desc_text.draw()

        # NO DYNAMIC SELECTED UNIT INFO - REMOVED COMPLETELY


class GameInfoPane:
    """Main info panel on the right side (static legends + special abilities info)"""

    def __init__(self, controller):
        self.controller = controller
        self.pane_width = 350
        self.x_offset = SCREEN_WIDTH - self.pane_width
        self.margin = 10
        self.pane_spacing = 12

        # Create panes with dynamic positioning
        self._create_panes()

    def _create_panes(self):
        """Create panes and calculate their positions"""
        pane_width = self.pane_width - 2 * self.margin
        current_y = SCREEN_HEIGHT - self.margin

        # 1. Unit Types pane (TOP)
        temp_unit_types = UnitTypesPane(0, 0, pane_width)
        current_y -= temp_unit_types.height
        self.unit_types_pane = UnitTypesPane(self.x_offset + self.margin, current_y, pane_width)

        # 2. Special Abilities pane (MIDDLE)
        current_y -= self.pane_spacing
        temp_abilities = SpecialAbilitiesPane(0, 0, pane_width)
        current_y -= temp_abilities.height
        self.abilities_pane = SpecialAbilitiesPane(self.x_offset + self.margin, current_y, pane_width)

        # 3. Legend pane (BOTTOM)
        current_y -= self.pane_spacing
        temp_legend = LegendPane(0, 0, pane_width)
        current_y -= temp_legend.height
        self.legend_pane = LegendPane(self.x_offset + self.margin, current_y, pane_width)

    def draw(self):
        """Draw the complete info pane"""
        # Draw main background
        arcade.draw_lbwh_rectangle_filled(self.x_offset, 0, self.pane_width, SCREEN_HEIGHT, (30, 30, 30))

        # Draw left border
        arcade.draw_line(self.x_offset, 0, self.x_offset, SCREEN_HEIGHT, arcade.color.WHITE, 3)

        # Draw all sub-panes
        self.unit_types_pane.draw()
        self.abilities_pane.draw(self.controller)  # This needs controller for dynamic content
        self.legend_pane.draw()