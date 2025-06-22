import random

class SpecialTile:
    """Represents a special tile on the board"""
    
    def __init__(self, tile_type, position):
        self.tile_type = tile_type  # 'elevated', 'cover', 'sensor', 'goldmine'
        self.position = position
        self.unit_on_tile = None
        self.goldmine_turns = 0  # For goldmine tiles
    
    def get_effect_description(self):
        """Get description of tile effect"""
        descriptions = {
            'elevated': '+1 Rank in combat',
            'cover': 'Immune to special abilities',
            'sensor': 'Reveals unit type',
            'goldmine': '1 gold after 3 turns'
        }
        return descriptions.get(self.tile_type, '')
    
    def apply_effect(self, unit):
        """Apply tile effect to unit"""
        if self.tile_type == 'sensor':
            unit.is_revealed = True
        elif self.tile_type == 'goldmine':
            if self.unit_on_tile == unit:
                self.goldmine_turns += 1
            else:
                self.goldmine_turns = 1
                self.unit_on_tile = unit
    
    def get_combat_bonus(self):
        """Get combat rank bonus from this tile"""
        if self.tile_type == 'elevated':
            return 1
        return 0
    
    def blocks_special_abilities(self):
        """Check if this tile blocks special abilities"""
        return self.tile_type == 'cover'
    
    def check_goldmine_reward(self):
        """Check if goldmine should give reward"""
        if self.tile_type == 'goldmine' and self.goldmine_turns >= 3:
            self.goldmine_turns = 0
            return True
        return False


def create_special_tiles():
    """Create all special tiles for the middle section"""
    tiles = {}
    
    # Get all positions in middle 4 rows (rows 3-6)
    middle_positions = []
    for row in range(3, 7):
        for col in range(10):
            middle_positions.append((row, col))
    
    # Randomly select positions for special tiles
    selected_positions = random.sample(middle_positions, 12)
    
    # 3 Elevated positions (C in ASCII)
    for i in range(3):
        pos = selected_positions[i]
        tiles[pos] = SpecialTile('elevated', pos)
    
    # 2 Cover positions (P in ASCII)
    for i in range(3, 5):
        pos = selected_positions[i]
        tiles[pos] = SpecialTile('cover', pos)
    
    # 4 Sensor positions (R in ASCII)
    for i in range(5, 9):
        pos = selected_positions[i]
        tiles[pos] = SpecialTile('sensor', pos)
    
    # 3 Goldmine positions (Y in ASCII)
    for i in range(9, 12):
        pos = selected_positions[i]
        tiles[pos] = SpecialTile('goldmine', pos)
    
    return tiles