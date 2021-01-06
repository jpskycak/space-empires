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
    def __init__(self, player_strats, grid_size, asc_or_dsc, type_of_player, max_turns=1000):
        self.grid_size = grid_size  # ex [5,5]
        self.game_won = False
        self.players_dead = 0
        self.board = Board(self, grid_size, asc_or_dsc)
        self.max_turns = max_turns
        self.type_of_player = type_of_player
        self.player = Player(BasicStrategy, (0, 0),
                             self.grid_size, '0', 'black')
        self.combat_engine = CombatEngine(
            self.board, self, self.grid_size, asc_or_dsc)
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
        self.generate_state()
        self.log.get_next_active_file('logs')

    def create_players(self):
        starting_positions = [[self.grid_size // 2, 0], [self.grid_size // 2, self.grid_size], [0, self.grid_size // 2], [
            self.grid_size, self.grid_size // 2]]  # players now start at the axis' and not the corners
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i, strategy in enumerate(self.player_strats):
            players.append(
                Player(strategy, starting_positions[i], self.grid_size, i + 1, colors[i]))
        '''for i in range(0, 2):
            if self.type_of_player == 1:
                players.append(DumbPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 2:
                players.append(RandomPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 3:
                players.append(CombatPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 4:
                players.append(ColbyStrategyPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))'''
        return players

    def play(self):
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
                print('Player', player.player_number, 'WINS!')

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
        self.generate_state()
        print('--------------------------------------------------')
        print('Combat Phase')
        self.combat_engine.complete_all_fights()
        self.state_obsolete()
        self.generate_state()
        print('--------------------------------------------------')
        if self.turn < self.max_turns:
            print('Economic Phase')
            self.economic_engine.complete_all_taxes(self.turn)
            for player in self.players:
                print('Player', player.player_number, 'Has',
                      player.creds, 'creds extra after the economic phase.')
            self.state_obsolete()
            self.generate_state()
            print('--------------------------------------------------')
        self.board.update_board()

    def generate_state(self, phase=None, movement_round=0):
        movement_state = self.movement_engine.generate_movement_state(movement_round)
        self.game_state['grid_size'] = self.grid_size
        self.game_state['turn'] = self.turn
        self.game_state['phase'] = phase
        self.game_state['round'] = movement_state['round'],
        self.game_state['combat'] = self.combat_engine.generate_combat_array()
        players = []
        for player in self.players:
            player_attributes = {}
            for attribute, value in player.__dict__.items():
                if isinstance(value, list):
                    if len(value) > 0:
                        if isinstance(value[0], int):
                            player_attributes[attribute] = value
                        elif not isinstance(value[0], int):
                            ships = {}
                            for ship in value:
                                ship_attributes = {}
                                for key, value in ship.__dict__.items(): 
                                    if key != 'player':
                                        ship_attributes[key] = value
                                ships[(ship.name, ship.ID)] = ship_attributes
                            player_attributes[attribute] = ships
                    else:
                        player_attributes[attribute] = value
                else:
                    player_attributes[attribute] = value
            player_attributes['economic_state'] = self.economic_engine.generate_economic_state(
                player, self.turn)
            players.append(player_attributes)
        self.game_state['players'] = players
        self.game_state['misc_dict'] = self.board.misc_dict

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
            print('     Player:', player.player_number, '| Type:',
                  player.strategy.__name__, '| Status:', player.status)
            print('')
            print('          Player Ships')
            for ship in player.ships:
                print('              ', ship.name, ':', 'Ship ID:',
                      ship.ID, ':', [ship.x, ship.y])

            if player.colonies != []:
                print('')
                print('          Player Colonies')
                for colony in player.colonies:
                    print('              ', colony.name, ':', 'Colony ID:',
                          colony.ID, ':', [colony.x, colony.y])

            print('')
            print('          Player Home Base')
            print('              ', player.home_base.name, ':', 'Colony ID:',
                  player.home_base.ID, ':', [player.home_base.x, player.home_base.y])

            print('')
            print('          Player Ship Yards')
            for ship_yard in player.ship_yards:
                print('              ', 'Ship Yard ID:', ship_yard.ID,
                      ':', [ship_yard.x, ship_yard.y])
            print('')
            print('')
