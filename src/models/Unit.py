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

    def use_special_ability(self):
        """Use the unit's special ability"""
        if not self.special_used and self.special_ability:
            self.special_used = True
            return True
        return False

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