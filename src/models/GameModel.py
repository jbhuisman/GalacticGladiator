import random
import json
import os
from datetime import datetime
from models.Unit import create_unit_set
from models.SpecialTile import create_special_tiles


class GameModel:
    """Model for Galactic Gladiators game state and logic"""

    def __init__(self, load_from_save=True):
        # Try to load from autosave first
        if load_from_save and self._load_autosave():
            return  # Successfully loaded from save
            
        # Create new game
        self._create_new_game()
        
        # Create initial autosave
        self._create_autosave()

    def _create_new_game(self):
        """Create a completely new game"""
        # Game state
        self.board_size = 10  # 10x10 grid
        self.current_player = 'human'  # 'human' or 'ai'
        self.game_phase = 'setup'  # 'setup', 'playing', 'game_over'
        self.winner = None
        self.gold_human = 0
        self.gold_ai = 0

        # Turn management - Multiple actions per turn
        self.actions_remaining = 2  # Each player gets 2 actions per turn
        self.max_actions_per_turn = 2

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

        # Special ability states
        self.rally_mode = False  # For warlord rally ability
        self.infiltration_mode = False  # For scout infiltration
        self.long_range_mode = False  # For sniper long range

        # Turn counter for effects
        self.turn_counter = 0

        # Auto-place AI units at start
        self.ai_setup()

    def _create_autosave(self):
        """Create autosave file"""
        try:
            save_data = self._serialize_game_state()
            with open('autosave_01.json', 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Failed to create autosave: {e}")

    def _load_autosave(self):
        """Load game from autosave file"""
        try:
            if not os.path.exists('autosave_01.json'):
                return False
                
            with open('autosave_01.json', 'r') as f:
                save_data = json.load(f)
                
            return self._deserialize_game_state(save_data)
        except Exception as e:
            print(f"Failed to load autosave: {e}")
            return False

    def _serialize_game_state(self):
        """Convert game state to JSON-serializable format"""
        # Serialize units
        def serialize_unit(unit):
            return {
                'unit_type': unit.unit_type,
                'rank': unit.rank,
                'owner': unit.owner,
                'special_ability': unit.special_ability,
                'special_used': unit.special_used,
                'is_revealed': unit.is_revealed,
                'position': unit.position,
                'stealth_active': getattr(unit, 'stealth_active', False),
                'protected_by_shield': getattr(unit, 'protected_by_shield', False)
            }

        # Serialize board state
        board_data = {}
        for pos, unit in self.board_state.items():
            key = f"{pos[0]},{pos[1]}"
            board_data[key] = serialize_unit(unit)

        # Serialize special tiles
        tiles_data = {}
        for pos, tile in self.special_tiles.items():
            key = f"{pos[0]},{pos[1]}"
            tiles_data[key] = {
                'tile_type': tile.tile_type,
                'position': tile.position,
                'goldmine_turns': getattr(tile, 'goldmine_turns', 0)
            }

        return {
            'timestamp': datetime.now().isoformat(),
            'board_size': self.board_size,
            'current_player': self.current_player,
            'game_phase': self.game_phase,
            'winner': self.winner,
            'gold_human': self.gold_human,
            'gold_ai': self.gold_ai,
            'actions_remaining': self.actions_remaining,
            'max_actions_per_turn': self.max_actions_per_turn,
            'setup_phase': self.setup_phase,
            'turn_counter': self.turn_counter,
            'board_state': board_data,
            'special_tiles': tiles_data,
            'human_units': [serialize_unit(u) for u in self.human_units],
            'ai_units': [serialize_unit(u) for u in self.ai_units]
        }

    def _deserialize_game_state(self, save_data):
        """Load game state from JSON data"""
        try:
            from models.Unit import Unit
            from models.SpecialTile import SpecialTile
            
            # Load basic state
            self.board_size = save_data['board_size']
            self.current_player = save_data['current_player']
            self.game_phase = save_data['game_phase']
            self.winner = save_data['winner']
            self.gold_human = save_data['gold_human']
            self.gold_ai = save_data['gold_ai']
            self.actions_remaining = save_data['actions_remaining']
            self.max_actions_per_turn = save_data['max_actions_per_turn']
            self.setup_phase = save_data['setup_phase']
            self.turn_counter = save_data['turn_counter']

            # Deserialize units
            def deserialize_unit(unit_data):
                from models.Unit import Unit
                unit = Unit(
                    unit_data['unit_type'],
                    unit_data['rank'],
                    unit_data['owner'],
                    unit_data['special_ability']
                )
                unit.special_used = unit_data['special_used']
                unit.is_revealed = unit_data['is_revealed']
                unit.position = tuple(unit_data['position']) if unit_data['position'] else None
                unit.stealth_active = unit_data.get('stealth_active', False)
                unit.protected_by_shield = unit_data.get('protected_by_shield', False)
                return unit

            # Load units
            self.human_units = [deserialize_unit(u) for u in save_data['human_units']]
            self.ai_units = [deserialize_unit(u) for u in save_data['ai_units']]

            # Load board state
            self.board_state = {}
            for pos_key, unit_data in save_data['board_state'].items():
                row, col = map(int, pos_key.split(','))
                position = (row, col)
                unit = deserialize_unit(unit_data)
                self.board_state[position] = unit

            # Load special tiles
            self.special_tiles = {}
            for pos_key, tile_data in save_data['special_tiles'].items():
                row, col = map(int, pos_key.split(','))
                position = (row, col)
                tile = SpecialTile(tile_data['tile_type'], position)
                tile.goldmine_turns = tile_data.get('goldmine_turns', 0)
                self.special_tiles[position] = tile

            # Calculate remaining setup units
            placed_units = set(self.board_state.values())
            self.setup_units_remaining = {
                'human': [u for u in self.human_units if u not in placed_units],
                'ai': [u for u in self.ai_units if u not in placed_units]
            }

            # Reset UI state
            self.selected_unit = None
            self.selected_position = None
            self.valid_moves = []
            self.valid_attacks = []
            self.rally_mode = False
            self.infiltration_mode = False
            self.long_range_mode = False

            return True
            
        except Exception as e:
            print(f"Failed to deserialize game state: {e}")
            return False

    def autosave(self):
        """Save current game state"""
        self._create_autosave()

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
            self.actions_remaining = self.max_actions_per_turn
            # Autosave when setup complete
            self.autosave()

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
                    0 <= new_col < self.board_size):
                
                # Normal movement - cell must be empty
                if new_pos not in self.board_state:
                    moves.append(new_pos)
                
                # INFILTRATION: Scout can move through enemies
                elif (unit.special_ability == 'infiltration' and 
                      self.infiltration_mode and new_pos in self.board_state):
                    target_unit = self.board_state[new_pos]
                    if target_unit.owner != unit.owner:
                        # Can move through enemy, check position beyond
                        beyond_row, beyond_col = new_row + dr, new_col + dc
                        beyond_pos = (beyond_row, beyond_col)
                        if (0 <= beyond_row < self.board_size and 
                            0 <= beyond_col < self.board_size and
                            beyond_pos not in self.board_state):
                            moves.append(beyond_pos)

        # RALLY: Warlord can move allied units with them
        if (unit.special_ability == 'rally' and self.rally_mode):
            # Add positions where allies can be moved to
            rally_moves = self._get_rally_moves(unit)
            moves.extend(rally_moves)

        return moves

    def get_valid_attacks(self, unit):
        """Get valid attack targets for a unit"""
        if not unit.position:
            return []

        row, col = unit.position
        attacks = []

        # Normal adjacent attacks
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)

            if (0 <= new_row < self.board_size and
                    0 <= new_col < self.board_size and
                    new_pos in self.board_state):

                target = self.board_state[new_pos]
                if unit.can_attack(target):
                    attacks.append(new_pos)

        # LONG RANGE: Sniper can attack at range 2
        if (unit.special_ability == 'long_range' and self.long_range_mode):
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    if abs(dr) + abs(dc) <= 2 and not (dr == 0 and dc == 0):
                        new_row, new_col = row + dr, col + dc
                        new_pos = (new_row, new_col)
                        
                        if (0 <= new_row < self.board_size and
                                0 <= new_col < self.board_size and
                                new_pos in self.board_state):
                            
                            target = self.board_state[new_pos]
                            if unit.can_attack(target):
                                attacks.append(new_pos)

        return attacks

    def _get_rally_moves(self, warlord):
        """Get valid rally moves for warlord"""
        if not warlord.position:
            return []
        
        rally_moves = []
        row, col = warlord.position
        
        # Check adjacent allies
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ally_row, ally_col = row + dr, col + dc
            ally_pos = (ally_row, ally_col)
            
            if (ally_pos in self.board_state and 
                self.board_state[ally_pos].owner == warlord.owner):
                
                ally = self.board_state[ally_pos]
                # Check where this ally can move
                for adr, adc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_ally_row, new_ally_col = ally_row + adr, ally_col + adc
                    new_ally_pos = (new_ally_row, new_ally_col)
                    
                    if (0 <= new_ally_row < self.board_size and 
                        0 <= new_ally_col < self.board_size and
                        new_ally_pos not in self.board_state):
                        rally_moves.append(new_ally_pos)
        
        return rally_moves

    def move_unit(self, unit, new_position):
        """Move a unit to a new position"""
        # Check if we have actions remaining
        if self.actions_remaining <= 0:
            return False
            
        valid_moves = self.get_valid_moves(unit)
        if new_position not in valid_moves:
            return False

        # Handle RALLY movement
        if (unit.special_ability == 'rally' and self.rally_mode):
            return self._handle_rally_movement(unit, new_position)

        # Handle INFILTRATION movement
        if (unit.special_ability == 'infiltration' and self.infiltration_mode):
            return self._handle_infiltration_movement(unit, new_position)

        # Normal movement
        return self._execute_move(unit, new_position)

    def _handle_rally_movement(self, warlord, target_position):
        """Handle warlord rally movement"""
        # Find which ally should move to target position
        row, col = warlord.position
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ally_row, ally_col = row + dr, col + dc
            ally_pos = (ally_row, ally_col)
            
            if (ally_pos in self.board_state and 
                self.board_state[ally_pos].owner == warlord.owner):
                
                ally = self.board_state[ally_pos]
                ally_moves = []
                
                # Check where this ally can move
                for adr, adc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_ally_row, new_ally_col = ally_row + adr, ally_col + adc
                    new_ally_pos = (new_ally_row, new_ally_col)
                    if (0 <= new_ally_row < self.board_size and 
                        0 <= new_ally_col < self.board_size and
                        new_ally_pos not in self.board_state):
                        ally_moves.append(new_ally_pos)
                
                if target_position in ally_moves:
                    # Move the ally - don't double consume actions
                    old_position = ally.position
                    if old_position in self.board_state:
                        del self.board_state[old_position]
                    
                    self.board_state[target_position] = ally
                    ally.position = target_position
                    
                    # Apply special tile effects for ally
                    if target_position in self.special_tiles:
                        tile = self.special_tiles[target_position]
                        tile.apply_effect(ally)
                        
                        # Check for goldmine reward
                        if tile.check_goldmine_reward():
                            if ally.owner == 'human':
                                self.gold_human += 1
                            else:
                                self.gold_ai += 1
                    
                    # Remove from old tile tracking
                    if old_position in self.special_tiles:
                        old_tile = self.special_tiles[old_position]
                        if old_tile.unit_on_tile == ally:
                            old_tile.unit_on_tile = None
                            old_tile.goldmine_turns = 0
                    
                    self.rally_mode = False
                    self.actions_remaining -= 1  # Only consume action once
                    return True
        
        return False

    def _handle_infiltration_movement(self, scout, target_position):
        """Handle scout infiltration movement"""
        row, col = scout.position
        
        # Find the path through enemy
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            enemy_row, enemy_col = row + dr, col + dc
            enemy_pos = (enemy_row, enemy_col)
            beyond_row, beyond_col = enemy_row + dr, enemy_col + dc
            beyond_pos = (beyond_row, beyond_col)
            
            if (beyond_pos == target_position and
                enemy_pos in self.board_state and
                self.board_state[enemy_pos].owner != scout.owner):
                
                # Execute the infiltration move - don't double consume actions
                old_position = scout.position
                if old_position in self.board_state:
                    del self.board_state[old_position]
                
                self.board_state[target_position] = scout
                scout.position = target_position
                
                # Apply special tile effects
                if target_position in self.special_tiles:
                    tile = self.special_tiles[target_position]
                    tile.apply_effect(scout)
                    
                    # Check for goldmine reward
                    if tile.check_goldmine_reward():
                        if scout.owner == 'human':
                            self.gold_human += 1
                        else:
                            self.gold_ai += 1
                
                # Remove from old tile tracking
                if old_position in self.special_tiles:
                    old_tile = self.special_tiles[old_position]
                    if old_tile.unit_on_tile == scout:
                        old_tile.unit_on_tile = None
                        old_tile.goldmine_turns = 0
                
                self.infiltration_mode = False
                self.actions_remaining -= 1  # Only consume action once
                return True
        
        return False

    def _execute_move(self, unit, new_position):
        """Execute the actual movement"""
        # Check if we have actions remaining (double check)
        if self.actions_remaining <= 0:
            return False
            
        # Remove from old position
        old_position = unit.position
        if old_position in self.board_state:
            del self.board_state[old_position]

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

        # Remove unit from old special tile tracking
        if old_position in self.special_tiles:
            old_tile = self.special_tiles[old_position]
            if old_tile.unit_on_tile == unit:
                old_tile.unit_on_tile = None
                old_tile.goldmine_turns = 0

        # Consume action
        self.actions_remaining -= 1
        return True

    def attack_unit(self, attacker, target_position):
        """Perform an attack between two units"""
        # Check if we have actions remaining
        if self.actions_remaining <= 0:
            return False
            
        valid_attacks = self.get_valid_attacks(attacker)
        if target_position not in valid_attacks:
            return False

        target = self.board_state[target_position]

        # Calculate effective ranks (including tile bonuses)
        attacker_rank = attacker.rank
        target_rank = target.rank

        # Apply tile bonuses
        if attacker.position in self.special_tiles:
            tile = self.special_tiles[attacker.position]
            attacker_rank += tile.get_combat_bonus()

        if target_position in self.special_tiles:
            tile = self.special_tiles[target_position]
            target_rank += tile.get_combat_bonus()

        # SHIELD PROTECTION: Protected units get +1 rank
        if hasattr(target, 'protected_by_shield') and target.protected_by_shield:
            target_rank += 1

        # Determine winner
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

        # Remove loser from board and special tile tracking
        loser_position = loser.position
        if loser_position in self.board_state:
            del self.board_state[loser_position]
        
        if loser_position in self.special_tiles:
            tile = self.special_tiles[loser_position]
            if tile.unit_on_tile == loser:
                tile.unit_on_tile = None
                tile.goldmine_turns = 0

        # Move winner to target position if attacker won
        if winner == attacker:
            # Remove attacker from old position and special tile tracking
            old_position = attacker.position
            if old_position in self.board_state:
                del self.board_state[old_position]
            
            if old_position in self.special_tiles:
                old_tile = self.special_tiles[old_position]
                if old_tile.unit_on_tile == attacker:
                    old_tile.unit_on_tile = None
                    old_tile.goldmine_turns = 0

            # Place attacker at target position
            self.board_state[target_position] = attacker
            attacker.position = target_position

            # Apply special tile effects
            if target_position in self.special_tiles:
                tile = self.special_tiles[target_position]
                tile.apply_effect(attacker)

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

        # Reset special ability modes after attack
        self.long_range_mode = False
        
        # Consume action
        self.actions_remaining -= 1
        return True

    def activate_special_ability(self, unit):
        """Activate a special ability"""
        if unit.special_used or not unit.special_ability:
            return False
        
        # Check if on cover tile (blocks special abilities)
        if unit.position and unit.position in self.special_tiles:
            tile = self.special_tiles[unit.position]
            if tile.blocks_special_abilities():
                return False
        
        success = False
        
        if unit.special_ability == 'stealth':
            # Commando stealth - becomes invisible for 1 turn
            unit.stealth_active = True
            unit.special_used = True
            success = True
            
        elif unit.special_ability == 'protection':
            # Shield protection - protects adjacent allies
            success = unit.use_special_ability(self)
            
        elif unit.special_ability == 'infiltration':
            # Scout infiltration - enable infiltration mode
            self.infiltration_mode = True
            unit.special_used = True
            success = True
            
        elif unit.special_ability == 'long_range':
            # Sniper long range - enable long range mode
            self.long_range_mode = True
            unit.special_used = True
            success = True
            
        elif unit.special_ability == 'rally':
            # Warlord rally - enable rally mode
            self.rally_mode = True
            unit.special_used = True
            success = True
        
        if success:
            # Recalculate valid moves/attacks with new mode
            if self.selected_unit == unit:
                self.valid_moves = self.get_valid_moves(unit)
                self.valid_attacks = self.get_valid_attacks(unit)
        
        return success

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
            # Check if player has actions remaining
            if self.actions_remaining <= 0:
                return False
                
            if not self.selected_unit:
                return self.select_unit(position)
            else:
                if position in self.valid_moves:
                    success = self.move_unit(self.selected_unit, position)
                    if success:
                        self.clear_selection()
                        # Auto-end turn if no actions remaining
                        if self.actions_remaining <= 0:
                            self.end_turn()
                    return success
                elif position in self.valid_attacks:
                    success = self.attack_unit(self.selected_unit, position)
                    if success:
                        self.clear_selection()
                        # Auto-end turn if no actions remaining
                        if self.actions_remaining <= 0:
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
        
        # Reset special ability modes
        self.rally_mode = False
        self.infiltration_mode = False
        self.long_range_mode = False

        if self.game_phase == 'playing':
            # Reset special effects for current player's units
            current_units = [unit for unit in self.board_state.values() 
                           if unit.owner == self.current_player]
            for unit in current_units:
                unit.reset_special_effects()
            
            if self.current_player == 'human':
                self.current_player = 'ai'
                self.actions_remaining = self.max_actions_per_turn
                # Autosave before AI turn
                self.autosave()
                # AI will make moves automatically
                self.ai_turn()
            else:
                self.current_player = 'human'
                self.actions_remaining = self.max_actions_per_turn
                self.turn_counter += 1
                # Autosave after AI turn
                self.autosave()

    def ai_turn(self):
        """AI makes multiple moves"""
        if self.game_phase != 'playing' or self.current_player != 'ai':
            return

        actions_taken = 0
        max_actions = self.max_actions_per_turn

        while actions_taken < max_actions and self.current_player == 'ai':
            # Smart AI: prioritize attacks, then strategic moves
            ai_units = [unit for unit in self.board_state.values() if unit.owner == 'ai']
            random.shuffle(ai_units)

            action_taken = False

            # First pass: try attacks
            for unit in ai_units:
                attacks = self.get_valid_attacks(unit)
                if attacks:
                    # Prioritize attacking flag
                    flag_targets = [pos for pos in attacks 
                                  if self.board_state[pos].unit_type == 'flag']
                    if flag_targets:
                        target_pos = flag_targets[0]
                    else:
                        # Attack highest rank enemy
                        target_pos = max(attacks, 
                                       key=lambda pos: self.board_state[pos].rank)
                    
                    if self.attack_unit(unit, target_pos):
                        actions_taken += 1
                        action_taken = True
                        break

            # Second pass: try special abilities
            if not action_taken:
                for unit in ai_units:
                    if (unit.special_ability and not unit.special_used and
                        random.random() < 0.3):  # 30% chance to use ability
                        if self.activate_special_ability(unit):
                            action_taken = True
                            # Don't count ability activation as full action
                            break

            # Third pass: try moves
            if not action_taken:
                for unit in ai_units:
                    moves = self.get_valid_moves(unit)
                    if moves:
                        # Move towards center or towards enemy
                        move_pos = self._ai_select_best_move(unit, moves)
                        if self.move_unit(unit, move_pos):
                            actions_taken += 1
                            action_taken = True
                            break

            if not action_taken:
                break  # No more valid actions

        # End AI turn
        self.end_turn()

    def _ai_select_best_move(self, unit, moves):
        """AI selects the best move from available options"""
        if not moves:
            return None
        
        # Simple strategy: move towards center and towards enemies
        best_move = None
        best_score = -999
        
        for move in moves:
            score = 0
            row, col = move
            
            # Prefer moving towards center
            center_distance = abs(row - 4.5) + abs(col - 4.5)
            score -= center_distance
            
            # Prefer moves that get closer to enemies
            enemy_units = [u for u in self.board_state.values() if u.owner != unit.owner]
            if enemy_units:
                min_enemy_distance = min(
                    abs(row - u.position[0]) + abs(col - u.position[1])
                    for u in enemy_units if u.position
                )
                score -= min_enemy_distance * 2
            
            # Prefer special tiles
            if move in self.special_tiles:
                tile = self.special_tiles[move]
                if tile.tile_type in ['elevated', 'goldmine']:
                    score += 5
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move or random.choice(moves)

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

    def can_end_turn(self):
        """Check if current player can end their turn"""
        return self.actions_remaining < self.max_actions_per_turn

    def has_actions_remaining(self):
        """Check if current player has actions remaining"""
        return self.actions_remaining > 0