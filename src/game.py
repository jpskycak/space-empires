import random
from board import Board
from board import Planet
from logger import Logger
from player.player import Player
from combat_engine import CombatEngine
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from unit.unit import Unit
from unit.scout import Scout
from unit.destroyer import Destroyer
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.battleship import Battleship
from unit.dreadnaught import Dreadnaught
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.ship_yard import Ship_Yard
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy
from unit.carrier import Carrier


class Game:
    def __init__(self, player_strats, board_size, asc_or_dsc, type_of_player, print_state_obsolete = True, max_turns=1000, generate_planets = False, number_of_movement_rounds = 1, economic_phase = False, screen_ships = False, can_log = True):
        self.board_size = board_size  # ex [5,5]
        self.game_won = False
        self.board = Board(self, board_size, asc_or_dsc)
        self.max_turns = max_turns
        self.type_of_player = type_of_player
        self.combat_engine = CombatEngine(
            self.board, self, self.board_size, asc_or_dsc)
        self.movement_engine = MovementEngine(self.board, self)
        self.economic_engine = EconomicEngine(self.board, self)
        self.log = Logger()
        self.can_log = can_log
        self.game_state = {}
        self.hidden_game_state_state = {}
        self.hidden_game_state_for_combat_state = {}
        self.player_strats = player_strats
        self.starting_positions = [[self.board_size[0] // 2, 0], [self.board_size[0] // 2, self.board_size[1] - 1], [0, self.board_size[1] // 2], [
            self.board_size[0] - 1, self.board_size[1] // 2]] # players now start at the axis' and not the corners
        self.print_state_obsolete = print_state_obsolete
        self.generate_planets = generate_planets
        self.number_of_movement_rounds = number_of_movement_rounds
        self.economic_phase = economic_phase
        self.screen_ships = screen_ships

    # main functions
    def initialize_game(self):
        self.players = self.create_players()
        if self.generate_planets: 
            self.board.create_planets_and_asteroids()
        else: 
            for i, _ in enumerate(self.player_strats): 
                self.board.misc_dict[(self.starting_positions[i][0], self.starting_positions[i][1])] = Planet(self.starting_positions[i], random.randint(0, 1), is_colonized=True)
        self.turn = 1
        self.generate_full_state(initial_state=True)
        if self.can_log: self.log.get_next_active_file('logs')

    def create_players(self):
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i, strategy in enumerate(self.player_strats):
            players.append(
                Player(strategy, self.starting_positions[i], self.board_size, i, colors[i]))
        '''for i in range(0, 2):
            if self.type_of_player == 1:
                players.append(DumbPlayer(self.starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 2:
                players.append(RandomPlayer(self.starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 3:
                players.append(CombatPlayer(self.starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 4:
                players.append(ColbyStrategyPlayer(self.starting_positions[i], self.board_size, i + 1, colors[i]))'''
        return players

    def play(self):
        self.generate_full_state()
        self.player_has_not_won = True
        if self.print_state_obsolete: 
            print('Initial State')
            self.state_obsolete()
            print('--------------------------------------------------')
        while not self.game_won and not self.check_if_player_has_won() and self.turn <= self.max_turns:
            self.complete_turn()
            if self.can_log: self.log.log_info(self.game_state, log_ship_yards=True)
            self.turn += 1
        player_won = self.player_has_won()
        return player_won

    def player_has_won(self):
        is_alive = []
        for player in self.players:
            if player.home_base.is_alive:
                player.is_alive = True
                is_alive.append(True)
            else:
                player.is_alive = False
                is_alive.append(False)
        for i, aliveness in enumerate(is_alive):
            if aliveness:
                if self.print_state_obsolete: print('Player', i, 'WINS!')
                return i

    def check_if_player_has_won(self):
        is_alive = []
        for player in self.players:
            if player.home_base.is_alive:
                player.is_alive = True
                is_alive.append(True)
            else:
                player.is_alive = False
                is_alive.append(False)
        if is_alive.count(True) <= 1:
            self.game_won = True
            return True
        else:
            self.game_won = False
            return False

    def complete_turn(self):
        if self.print_state_obsolete: print('Turn', self.turn)
        self.check_if_player_has_won()
        if not self.game_won:
            self.generate_full_state(phase='Movement')
            if self.print_state_obsolete: 
                print('--------------------------------------------------')
                print('Move Phase')
            self.movement_engine.complete_all_movements(self.board, self.hidden_game_state_state, self.number_of_movement_rounds)
            if self.print_state_obsolete: self.state_obsolete()
        if not self.game_won:
            self.generate_full_state(phase='Combat')
            if self.print_state_obsolete: 
                print('--------------------------------------------------')
                print('Combat Phase')
            self.combat_engine.complete_all_fights(self.hidden_game_state_for_combat_state, self.screen_ships)
            if self.print_state_obsolete: self.state_obsolete()
        if self.turn < self.max_turns and not self.game_won and self.economic_phase:
            self.generate_full_state(phase='Economic')
            if self.print_state_obsolete: 
                print('--------------------------------------------------')
                print('Economic Phase')
            self.economic_engine.complete_all_taxes(self.hidden_game_state_state)
            for player in self.players:
                if self.print_state_obsolete: print('Player', player.player_index, 'Has', player.creds, 'creds extra after the economic phase.')
            if self.print_state_obsolete: self.state_obsolete()
                    
        self.board.update_board()

    def generate_full_state(self, phase=None, movement_round=0, initial_state=False):
        self.hidden_game_state(phase=phase, movement_round=movement_round, initial_state=initial_state)
        self.hidden_game_state_for_combat(phase=phase, movement_round=movement_round, initial_state=initial_state)
        movement_state = self.movement_engine.generate_movement_state(movement_round)
        self.game_state['unit_data'] = {
            'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5, 'tactics': 5, 'attack': 5, 'defense': 2, 'maintenance': 3},
            'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4, 'tactics': 4, 'attack': 5, 'defense': 1, 'maintenance': 2},
            'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 3, 'tactics': 3, 'attack': 4, 'defense': 1, 'maintenance': 2},
            'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2, 'tactics': 2, 'attack': 4, 'defense': 0, 'maintenance': 1},
            'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6, 'tactics': 5, 'attack': 6, 'defense': 3, 'maintenance': 3},
            'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 1, 'attack': 3, 'defense': 0, 'maintenance': 1},
            'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 3, 'attack': 3, 'defense': 0, 'maintenance': 0},
            'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
            'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
            'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2, 'tactics': 5, 'attack': 7, 'defense': 2, 'maintenance': 0},
        }
        self.game_state['technology_data'] = {
            'shipsize': [0, 10, 15, 20, 25, 30],
            'attack': [20, 30, 40],
            'defense': [20, 30, 40],
            'movement': [0, 20, 30, 40, 40, 40],
            'shipyard': [0, 20, 30]
        }
        self.hidden_game_state_state['unit_data'] = self.game_state['unit_data']
        self.hidden_game_state_for_combat_state['unit_data'] = self.game_state['unit_data']
        self.hidden_game_state_state['technology_data'] = self.game_state['technology_data']
        self.hidden_game_state_for_combat_state['technology_data'] = self.game_state['technology_data']
        self.game_state['board_size'] = self.board_size
        self.game_state['turn'] = self.turn
        self.game_state['phase'] = phase
        self.game_state['round'] = movement_state['round']
        self.game_state['player_turn'] = 0
        self.game_state['winner'] = None
        self.game_state['combat'] = self.combat_engine.generate_combat_array()
        if initial_state: self.game_state['players'] = {}
        for i, player in enumerate(self.players):
            self.game_state['players'][i] = {'cp': player.creds, 'home_coords': (player.home_base.x, player.home_base.y), 'Is Alive': player.is_alive, 'units': [], 'colonies': [], 'shipyards': [], 'technology': player.technology}
            for unit in player.ships: self.game_state['players'][i]['units'].append({'coords': (unit.x, unit.y), 'type': unit.type, 'ID': unit.ID, 'hits_left': unit.hits_left, 'technology': unit.technology})
            for colonies in player.colonies: self.game_state['players'][i]['colonies'].append({'coords': (colonies.x, colonies.y), 'type': colonies.type, 'ID': colonies.ID, 'hits_left': colonies.hits_left, 'technology': colonies.technology})
            for shipyards in player.ship_yards: self.game_state['players'][i]['shipyards'].append({'coords': (shipyards.x, shipyards.y), 'type': shipyards.type, 'ID': shipyards.ID, 'hits_left': shipyards.hits_left, 'technology': shipyards.technology})
            self.game_state['players'][i]['economic_state'] = self.economic_engine.generate_economic_state(player, self.game_state)
        self.game_state['planets'] = self.board.planets

    def hidden_game_state(self, phase=None, movement_round=0, initial_state=False):
        movement_state = self.movement_engine.generate_movement_state(movement_round)
        self.hidden_game_state_state['board_size'] = self.board_size
        self.hidden_game_state_state['turn'] = self.turn
        self.hidden_game_state_state['phase'] = phase
        self.hidden_game_state_state['round'] = movement_state['round']
        self.hidden_game_state_state['player_turn'] = 0
        self.hidden_game_state_state['winner'] = None
        self.hidden_game_state_state['combat'] = self.combat_engine.generate_combat_array()
        if initial_state: self.hidden_game_state_state['players'] = {}
        for i, player in enumerate(self.players):
            self.hidden_game_state_state['players'][i] = {'home_coords': (player.home_base.x, player.home_base.y), 'Is Alive': player.is_alive, 'units': [], 'colonies': []}
            for unit in player.ships: self.hidden_game_state_state['players'][i]['units'].append({'coords': (unit.x, unit.y)})
            for shipyards in player.ship_yards: self.hidden_game_state_state['players'][i]['units'].append({'coords': (shipyards.x, shipyards.y)})
            for colonies in player.colonies: self.hidden_game_state_state['players'][i]['colonies'].append({'coords': (colonies.x, colonies.y), 'type': colonies.type})

    def hidden_game_state_for_combat(self, phase=None, movement_round=0, initial_state=False):
        movement_state = self.movement_engine.generate_movement_state(movement_round)
        self.hidden_game_state_for_combat_state['board_size'] = self.board_size
        self.hidden_game_state_for_combat_state['turn'] = self.turn
        self.hidden_game_state_for_combat_state['phase'] = phase
        self.hidden_game_state_for_combat_state['round'] = movement_state['round']
        self.hidden_game_state_for_combat_state['player_turn'] = 0
        self.hidden_game_state_for_combat_state['winner'] = None
        self.hidden_game_state_for_combat_state['combat'] = self.combat_engine.generate_combat_array()
        if initial_state: self.hidden_game_state_for_combat_state['players'] = {}
        for i, player in enumerate(self.players):
            self.hidden_game_state_for_combat_state['players'][i] = {'home_coords': (player.home_base.x, player.home_base.y), 'Is Alive': player.is_alive, 'units': [], 'colonies': [], 'shipyards': [], 'technology': player.technology}
            for unit in player.ships: self.hidden_game_state_for_combat_state['players'][i]['units'].append({'coords': (unit.x, unit.y), 'type': unit.type, 'ID': unit.ID, 'hits_left': unit.hits_left, 'technology': unit.technology})
            for colonies in player.colonies: self.hidden_game_state_for_combat_state['players'][i]['colonies'].append({'coords': (colonies.x, colonies.y), 'type': colonies.type, 'ID': colonies.ID, 'hits_left': colonies.hits_left, 'technology': colonies.technology})
            for shipyards in player.ship_yards: self.hidden_game_state_for_combat_state['players'][i]['shipyards'].append({'coords': (shipyards.x, shipyards.y), 'type': shipyards.type, 'ID': shipyards.ID, 'hits_left': shipyards.hits_left, 'technology': shipyards.technology})

    def state_obsolete(self, print_planets_and_asteroids=False):
        if print_planets_and_asteroids:
            print('Asteroids')
            print('')

            for asteroid in self.board.asteroids:
                print('     position:', asteroid.position)

            print('')
            print('Planets')
            print('')

            for planet in self.board.planets:
                print('     Tier:', planet.tier, '| Position:',
                      planet.position, '| Colonized:', planet.is_colonized)

        print('')
        print('Players')
        print('')

        for player in self.players:
            print('     Player:', player.player_index, '| Type:',
                  player.strategy.__name__, '| Is Alive:', player.is_alive)
            print('')
            print('          Player Ships')
            for ship in player.ships:
                print('              ', ship.type, ':', 'Ship ID:',
                      ship.ID, ':', [ship.x, ship.y])

            if player.colonies != []:
                print('')
                print('          Player Colonies')
                for colony in player.colonies:
                    print('              ', colony.type, ':', 'Colony ID:',
                          colony.ID, ':', [colony.x, colony.y])

            print('')
            print('          Player Home Base',
                  '| Is Alive:', player.home_base.is_alive)
            print('              ', player.home_base.type, ':', 'Colony ID:',
                  player.home_base.ID, ':', [player.home_base.x, player.home_base.y])

            print('')
            print('          Player Ship Yards')
            for ship_yard in player.ship_yards:
                print('              ', 'Ship Yard ID:', ship_yard.ID,
                      ':', [ship_yard.x, ship_yard.y])
            print('')
            print('')
