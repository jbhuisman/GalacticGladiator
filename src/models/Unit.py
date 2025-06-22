class Unit:
    """Base class for all game units"""

    def __init__(self, unit_type, rank, owner, special_ability=None):
        self.unit_type = unit_type  # 'scout', 'infantry', etc.
        self.rank = rank  # 0-6
        self.owner = owner  # 'human' or 'ai'
        self.special_ability = special_ability
        self.special_used = False
        self.is_revealed = False
        self.position = None
        self.stealth_active = False  # For commando stealth
        self.protected_by_shield = False  # For shield protection

    def can_attack(self, target):
        """Check if this unit can attack the target"""
        if target.owner == self.owner:
            return False
        return True

    def attack(self, target):
        """Attack another unit, returns winner"""
        # Higher rank wins, defender wins ties (except flag vs anyone)
        if target.rank == 0:  # Flag always loses
            return self
        elif self.rank == 0:  # Flag can't attack
            return target
        elif self.rank > target.rank:
            return self
        elif self.rank < target.rank:
            return target
        else:  # Equal ranks, defender wins
            return target

    def use_special_ability(self, game_model=None):
        """Use the unit's special ability"""
        if self.special_used or not self.special_ability:
            return False
            
        # Check if on cover tile (blocks special abilities)
        if self.position and game_model:
            if self.position in game_model.special_tiles:
                tile = game_model.special_tiles[self.position]
                if tile.blocks_special_abilities():
                    return False
        
        self.special_used = True
        
        # Activate ability based on type
        if self.special_ability == 'stealth':
            self.stealth_active = True
            return True
        elif self.special_ability == 'protection' and game_model:
            self._activate_shield_protection(game_model)
            return True
        # Other abilities are handled in GameModel
        
        return True

    def _activate_shield_protection(self, game_model):
        """Shield Bearer protects adjacent allied units"""
        if not self.position:
            return
            
        row, col = self.position
        # Check all adjacent positions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            adj_pos = (new_row, new_col)
            
            if adj_pos in game_model.board_state:
                adjacent_unit = game_model.board_state[adj_pos]
                if adjacent_unit.owner == self.owner:
                    adjacent_unit.protected_by_shield = True

    def reset_special_effects(self):
        """Reset temporary special effects (called each turn)"""
        self.stealth_active = False
        self.protected_by_shield = False

    def get_display_char(self):
        """Get character to display for this unit"""
        chars = {
            'scout': 'S',
            'infantry': 'I',
            'sniper': 'N',
            'shield': 'H',
            'warlord': 'W',
            'commando': 'C',
            'flag': 'F'
        }
        return chars.get(self.unit_type, '?')

    def get_special_ability_description(self):
        """Get description of special ability"""
        descriptions = {
            'infiltration': 'Kan door vijandelijke eenheden bewegen',
            'long_range': 'Kan op afstand van 2 cellen aanvallen',
            'protection': 'Beschermt aangrenzende bondgenoten',
            'rally': 'Kan bondgenoten meenemen bij beweging',
            'stealth': 'Onzichtbaar voor 1 beurt na activatie'
        }
        return descriptions.get(self.special_ability, 'Geen speciale vaardigheid')


def create_unit_set(owner):
    """Create a complete set of units for one player"""
    units = []

    # 3 Scouts (Rank 1)
    for i in range(3):
        units.append(Unit('scout', 1, owner, 'infiltration'))

    # 7 Infantry (Rank 2)
    for i in range(7):
        units.append(Unit('infantry', 2, owner))

    # 3 Snipers (Rank 3)
    for i in range(3):
        units.append(Unit('sniper', 3, owner, 'long_range'))

    # 2 Shield Bearers (Rank 4)
    for i in range(2):
        units.append(Unit('shield', 4, owner, 'protection'))

    # 2 Warlords (Rank 5)
    for i in range(2):
        units.append(Unit('warlord', 5, owner, 'rally'))

    # 2 Commandos (Rank 6)
    for i in range(2):
        units.append(Unit('commando', 6, owner, 'stealth'))

    # 1 Flag (Rank 0)
    units.append(Unit('flag', 0, owner))

    return units