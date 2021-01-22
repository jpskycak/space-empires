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
from strategies.basic_strategy import BasicStrategy
from strategies.dumb_strategy import DumbStrategy
from strategies.combat_strategy import CombatStrategy


class Game:
    def __init__(self, player_strats, board_size, asc_or_dsc, type_of_player, max_turns=1000):
        self.board_size = board_size  # ex [5,5]
        self.game_won = False
        self.players_dead = 0
        self.board = Board(self, board_size, asc_or_dsc)
        self.max_turns = max_turns
        self.type_of_player = type_of_player
        self.player = Player(BasicStrategy, (0, 0),
                             self.board_size, '0', 'black')
        self.combat_engine = CombatEngine(
            self.board, self, self.board_size, asc_or_dsc)
        self.movement_engine = MovementEngine(self.board, self)
        self.economic_engine = EconomicEngine(self.board, self)
        self.log = Logger()
        self.game_state = {}
        self.player_strats = player_strats

    # main functions
    def initialize_game(self):
        self.players = self.create_players()
        self.board.create_planets_and_asteroids()
        self.turn = 1
        self.generate_state(initial_state=True)
        self.log.get_next_active_file('logs')

    def create_players(self):
        starting_positions = [[self.board_size[0] // 2, 0], [self.board_size[0] // 2, self.board_size[1] - 1], [0, self.board_size[1] // 2], [
            self.board_size[0] - 1, self.board_size[1] // 2]]  # players now start at the axis' and not the corners
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i, strategy in enumerate(self.player_strats):
            players.append(
                Player(strategy, starting_positions[i], self.board_size, i, colors[i]))
        '''for i in range(0, 2):
            if self.type_of_player == 1:
                players.append(DumbPlayer(
                    starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 2:
                players.append(RandomPlayer(
                    starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 3:
                players.append(CombatPlayer(
                    starting_positions[i], self.board_size, i + 1, colors[i]))
            if self.type_of_player == 4:
                players.append(ColbyStrategyPlayer(
                    starting_positions[i], self.board_size, i + 1, colors[i]))'''
        return players

    def play(self):
        print('Initial State')
        self.generate_state()
        self.state_obsolete()
        self.player_has_not_won = True
        print('---------------------------------------------')
        while self.check_if_player_has_won() and self.turn <= self.max_turns:
            self.complete_turn()
            self.log.log_info(self.game_state)
            self.turn += 1
        self.player_has_won()

    def player_has_won(self):
        self.state_obsolete()
        for player in self.players:
            if player.status == 'Playing':
                self.game_won = True
                print('Player', player.player_index, 'WINS!')

    def check_if_player_has_won(self):
        for player in self.players:
            if player.home_base.status == 'Deceased':
                player.status = 'Deceased'
                return False
            else:
                return True

    def complete_turn(self):
        print('Turn', self.turn)
        self.check_if_player_has_won()
        print('Move Phase')
        self.movement_engine.complete_all_movements(
            self.board, self.game_state)
        self.state_obsolete()
        self.generate_state(phase='Combat')
        print('--------------------------------------------------')
        print('Combat Phase')
        self.combat_engine.complete_all_fights()
        self.state_obsolete()
        self.generate_state(phase='Economic')
        print('--------------------------------------------------')
        if self.turn < self.max_turns:
            print('Economic Phase')
            self.economic_engine.complete_all_taxes(self.game_state)
            for player in self.players:
                print('Player', player.player_index, 'Has',
                      player.creds, 'creds extra after the economic phase.')
            self.state_obsolete()
            self.generate_state(phase='Movement')
            print('--------------------------------------------------')
        self.board.update_board()

    def generate_state(self, phase=None, movement_round=0, initial_state=False):
        movement_state = self.movement_engine.generate_movement_state(
            movement_round)
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
            'shipsize': [10, 25, 45, 70, 95],
            'attack': [20, 50, 90],
            'defense': [20, 50, 90],
            'movement': [20, 50, 90, 130, 170],
            'shipyard': [20, 50]
        }
        self.game_state['board_size'] = self.board_size
        self.game_state['turn'] = self.turn
        self.game_state['phase'] = phase
        self.game_state['round'] = movement_state['round']
        self.game_state['player_turn'] = 0
        self.game_state['winner'] = None
        self.game_state['combat'] = self.combat_engine.generate_combat_array()
        if initial_state:
            self.game_state['players'] = {}
        for i, player in enumerate(self.players):
            player_attributes = {'cp': player.creds, 'home_coords': (player.home_base.x, player.home_base.y), 'status': player.status, 'units': [
            ], 'colonies': [], 'shipyards': [], 'technology': player.technology}
            for unit in player.ships:
                player_attributes['units'].append({'coords': (
                    unit.x, unit.y), 'type': unit.type, 'ID': unit.ID, 'hits_left': unit.hits_left, 'technology': unit.technology})
            for colonies in player.colonies:
                player_attributes['colonies'].append({'coords': (colonies.x, colonies.y), 'type': colonies.type,
                                                      'ID': colonies.ID, 'hits_left': colonies.hits_left, 'technology': colonies.technology})
            for shipyards in player.ship_yards:
                player_attributes['shipyards'].append({'coords': (shipyards.x, shipyards.y), 'type': shipyards.type,
                                                       'ID': shipyards.ID, 'hits_left': shipyards.hits_left, 'technology': shipyards.technology})
            player_attributes['economic_state'] = self.economic_engine.generate_economic_state(
                player, self.game_state)
            self.game_state['players'][i] = player_attributes
        self.game_state['planets'] = self.board.planets

    # misc functions

    # obsolete but can be used for debugging

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
                  player.strategy.__name__, '| Status:', player.status)
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
            print('          Player Home Base')
            print('              ', player.home_base.type, ':', 'Colony ID:',
                  player.home_base.ID, ':', [player.home_base.x, player.home_base.y])

            print('')
            print('          Player Ship Yards')
            for ship_yard in player.ship_yards:
                print('              ', 'Ship Yard ID:', ship_yard.ID,
                      ':', [ship_yard.x, ship_yard.y])
            print('')
            print('')
