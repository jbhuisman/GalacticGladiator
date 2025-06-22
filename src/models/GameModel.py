import random
from models.Unit import create_unit_set
from models.SpecialTile import create_special_tiles


class GameModel:
    """Model for Galactic Gladiators game state and logic"""

    def __init__(self):
        # Game state
        self.board_size = 10  # 10x10 grid
        self.current_player = 'human'  # 'human' or 'ai'
        self.game_phase = 'setup'  # 'setup', 'playing', 'game_over'
        self.winner = None
        self.gold_human = 0
        self.gold_ai = 0

        # Board state
        self.board_state = {}  # (row, col) -> Unit
        self.special_tiles = create_special_tiles()

        # Units
        self.human_units = create_unit_set('human')
        self.ai_units = create_unit_set('ai')
        self.setup_units_remaining = {'human': list(self.human_units), 'ai': list(self.ai_units)}

        # Setup phase tracking
        self.setup_phase = 'human'  # 'human' or 'ai'

        # Selected unit/position for UI
        self.selected_unit = None
        self.selected_position = None
        self.valid_moves = []
        self.valid_attacks = []

        # Auto-place AI units at start
        self.ai_setup()

    def get_setup_rows(self, player):
        """Get the rows where a player can place units during setup"""
        if player == 'human':
            return [0, 1]  # Top rows
        else:
            return [8, 9]  # Bottom rows

    def can_place_unit_at(self, position, player):
        """Check if a unit can be placed at position during setup"""
        if self.game_phase != 'setup':
            return False

        row, col = position
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False

        if position in self.board_state:
            return False  # Already occupied

        valid_rows = self.get_setup_rows(player)
        return row in valid_rows

    def place_unit(self, unit, position):
        """Place a unit at position during setup"""
        if not self.can_place_unit_at(position, unit.owner):
            return False

        self.board_state[position] = unit
        unit.position = position

        # Remove from remaining units
        if unit in self.setup_units_remaining[unit.owner]:
            self.setup_units_remaining[unit.owner].remove(unit)

        # Check if human setup phase is complete
        if (self.setup_phase == 'human' and 
            len(self.setup_units_remaining['human']) == 0):
            self.game_phase = 'playing'
            self.current_player = 'human'

        return True

    def ai_setup(self):
        """AI automatically places its units"""
        ai_rows = self.get_setup_rows('ai')
        available_positions = []

        for row in ai_rows:
            for col in range(self.board_size):
                if (row, col) not in self.board_state:
                    available_positions.append((row, col))

        # Randomly place all AI units
        random.shuffle(available_positions)
        for i, unit in enumerate(self.ai_units):
            if i < len(available_positions):
                position = available_positions[i]
                self.board_state[position] = unit
                unit.position = position

        self.setup_units_remaining['ai'] = []

    def get_valid_moves(self, unit):
        """Get valid moves for a unit"""
        if not unit.position:
            return []

        row, col = unit.position
        moves = []

        # Check all adjacent positions (orthogonal only)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)

            if (0 <= new_row < self.board_size and
                    0 <= new_col < self.board_size and
                    new_pos not in self.board_state):
                moves.append(new_pos)

        return moves

    def get_valid_attacks(self, unit):
        """Get valid attack targets for a unit"""
        if not unit.position:
            return []

        row, col = unit.position
        attacks = []

        # Check all adjacent positions (orthogonal only)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)

            if (0 <= new_row < self.board_size and
                    0 <= new_col < self.board_size and
                    new_pos in self.board_state):

                target = self.board_state[new_pos]
                if unit.can_attack(target):
                    attacks.append(new_pos)

        return attacks

    def move_unit(self, unit, new_position):
        """Move a unit to a new position"""
        if new_position not in self.get_valid_moves(unit):
            return False

        # Remove from old position
        if unit.position in self.board_state:
            del self.board_state[unit.position]

        # Place at new position
        self.board_state[new_position] = unit
        unit.position = new_position

        # Apply special tile effects
        if new_position in self.special_tiles:
            tile = self.special_tiles[new_position]
            tile.apply_effect(unit)

            # Check for goldmine reward
            if tile.check_goldmine_reward():
                if unit.owner == 'human':
                    self.gold_human += 1
                else:
                    self.gold_ai += 1

        return True

    def attack_unit(self, attacker, target_position):
        """Perform an attack between two units"""
        if target_position not in self.get_valid_attacks(attacker):
            return False

        target = self.board_state[target_position]

        # Calculate effective ranks (including tile bonuses)
        attacker_rank = attacker.rank
        target_rank = target.rank

        # Apply tile bonuses
        if attacker.position in self.special_tiles:
            attacker_rank += self.special_tiles[attacker.position].get_combat_bonus()

        if target_position in self.special_tiles:
            target_rank += self.special_tiles[target_position].get_combat_bonus()

        # Determine winner (higher rank wins, defender wins ties, except flag)
        if target.rank == 0:  # Flag always loses
            winner = attacker
            loser = target
        elif attacker.rank == 0:  # Flag can't attack
            return False
        elif attacker_rank > target_rank:
            winner = attacker
            loser = target
        elif attacker_rank < target_rank:
            winner = target
            loser = attacker
        else:  # Equal ranks, defender wins
            winner = target
            loser = attacker

        # Remove loser from board
        if loser.position in self.board_state:
            del self.board_state[loser.position]

        # Move winner to target position if attacker won
        if winner == attacker:
            # Remove attacker from old position
            if attacker.position in self.board_state:
                del self.board_state[attacker.position]
            # Place attacker at target position
            self.board_state[target_position] = attacker
            attacker.position = target_position

        # Check for flag capture (game over)
        if loser.unit_type == 'flag':
            self.game_phase = 'game_over'
            self.winner = winner.owner

            # Award victory gold
            if winner.owner == 'human':
                self.gold_human += 10
            else:
                self.gold_ai += 10

            # Award remaining unit gold
            for unit in self.get_remaining_units('human'):
                self.gold_human += 1
            for unit in self.get_remaining_units('ai'):
                self.gold_ai += 1

        return True

    def get_remaining_units(self, player):
        """Get remaining units for a player"""
        return [unit for unit in self.board_state.values() if unit.owner == player]

    def select_unit(self, position):
        """Select a unit at the given position"""
        if position in self.board_state:
            unit = self.board_state[position]
            if unit.owner == self.current_player:
                self.selected_unit = unit
                self.selected_position = position
                self.valid_moves = self.get_valid_moves(unit)
                self.valid_attacks = self.get_valid_attacks(unit)
                return True
        return False

    def handle_cell_click(self, position):
        """Handle clicking on a cell"""
        if self.game_phase == 'setup':
            if self.setup_phase == 'human' and len(self.setup_units_remaining['human']) > 0:
                # Place next unit
                next_unit = self.setup_units_remaining['human'][0]
                return self.place_unit(next_unit, position)

        elif self.game_phase == 'playing' and self.current_player == 'human':
            if not self.selected_unit:
                # Try to select a unit
                return self.select_unit(position)
            else:
                # Try to move or attack
                if position in self.valid_moves:
                    success = self.move_unit(self.selected_unit, position)
                    if success:
                        self.end_turn()
                    return success
                elif position in self.valid_attacks:
                    success = self.attack_unit(self.selected_unit, position)
                    if success:
                        self.end_turn()
                    return success
                else:
                    # Try to select different unit
                    self.clear_selection()
                    return self.select_unit(position)

        return False

    def clear_selection(self):
        """Clear current selection"""
        self.selected_unit = None
        self.selected_position = None
        self.valid_moves = []
        self.valid_attacks = []

    def end_turn(self):
        """End current player's turn"""
        self.clear_selection()

        if self.game_phase == 'playing':
            if self.current_player == 'human':
                self.current_player = 'ai'
                # AI will make move automatically
                self.ai_turn()
            else:
                self.current_player = 'human'

    def ai_turn(self):
        """AI makes a move"""
        if self.game_phase != 'playing' or self.current_player != 'ai':
            return

        # Simple AI: random valid move
        ai_units = [unit for unit in self.board_state.values() if unit.owner == 'ai']
        random.shuffle(ai_units)

        for unit in ai_units:
            # Try attacks first
            attacks = self.get_valid_attacks(unit)
            if attacks:
                target_pos = random.choice(attacks)
                if self.attack_unit(unit, target_pos):
                    self.end_turn()
                    return

            # Then try moves
            moves = self.get_valid_moves(unit)
            if moves:
                move_pos = random.choice(moves)
                if self.move_unit(unit, move_pos):
                    self.end_turn()
                    return

        # If no moves possible, just end turn
        self.end_turn()

    def get_board_state(self):
        """Get current board state for display"""
        return self.board_state

    def get_setup_remaining_count(self, player):
        """Get number of units remaining to place in setup"""
        return len(self.setup_units_remaining.get(player, []))

    def get_next_setup_unit(self, player):
        """Get the next unit to be placed during setup"""
        remaining = self.setup_units_remaining.get(player, [])
        return remaining[0] if remaining else None