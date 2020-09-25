import random
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator
from board import Board
from logger import Logger
from player.player import Player
from player.dumb_player import DumbPlayer
from player.random_player import RandomPlayer
from player.combat_player import CombatPlayer
from combat_engine import CombatEngine
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
    def __init__(self, grid_size, asc_or_dsc, type_of_player, will_colonize=False, max_turns=1000):
        self.grid_size = grid_size  # ex [5,5]
        self.game_won = False
        self.players_dead = 0
        self.board = Board(grid_size, asc_or_dsc)
        self.max_turns = max_turns
        self.type_of_player = type_of_player
        self.player = Player((0, 0), self.grid_size, '0',
                             'black', self.board, will_colonize)
        self.combat_engine = CombatEngine(
            self.board, self, self.grid_size, asc_or_dsc)
        self.log = Logger(self.board)

    # main functions
    def initialize_game(self):
        self.board.players = self.create_players()
        self.board.create_planets_and_asteroids()
        self.log.get_next_active_file('logs')

    def create_players(self):
        starting_positions = [[self.grid_size // 2, 0], [self.grid_size // 2, self.grid_size], [0, self.grid_size // 2], [
            self.grid_size, self.grid_size // 2]]  # players now start at the axis' and not the corners
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i in range(0, 2):
            #print('type_of_player', type_of_player)
            if self.type_of_player == 1:
                players.append(DumbPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i], self.board, self.player.will_colonize))
            if self.type_of_player == 2:
                players.append(RandomPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 3:
                players.append(CombatPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i], self.board, self.player.will_colonize))
            players[i].build_fleet()

        return players

    def play(self):
        turn = 1
        self.state_obsolete()
        self.player_has_not_won = True
        print('---------------------------------------------')
        while self.check_if_player_has_won() and turn <= self.max_turns:
            self.complete_turn(turn)
            self.log.log_info(turn)
            turn += 1
        self.player_has_won()

    def player_has_won(self):
        self.state_obsolete()
        for player in self.board.players:
            if player.status == 'Playing':
                self.game_won = True
                print('Player', player.player_number, 'WINS!')

    def check_if_player_has_won(self):
        for player in self.board.players:
            if player.home_base.status == 'Deceased':
                player.status = 'Deceased'
                return False
            else:
                return True

    def complete_turn(self, turn):
        print('Turn', turn)
        self.check_if_player_has_won()
        print('Move Phase')
        self.complete_move_phase(turn)
        self.state_obsolete()
        print('--------------------------------------------------')
        print('Combat Phase')
        self.complete_combat_phase()
        self.state_obsolete()
        print('--------------------------------------------------')
        if turn < self.max_turns:
            print('Economic Phase')
            self.complete_economic_phase(turn)
            for player in self.board.players:
                print('Player', player.player_number, 'Has',
                      player.creds, 'creds extra after the economic phase.')
            self.state_obsolete()
            print('--------------------------------------------------')
        self.board.update_board()

    # combat functions
    def complete_combat_phase(self):
        #print('fighting (combat)')
        possible_fights = self.combat_engine.possible_fights()
        #print('possible_fights', possible_fights)
        for _, ships in possible_fights.items():
            #print('ships', [ship.name for ship in ships])
            self.combat_engine.complete_all_combats(ships)

    def complete_move_phase(self, turn):
        for player in self.board.players:
            player.check_colonization(self.board)
            for _ in range(0, 3):  # 3 rounds of movements
                player.move()

    def complete_economic_phase(self, turn):
        for player in self.board.players:
            player.creds += player.income()
            player.maintenance()
            if turn == 1:
                player.upgrade(turn)
            player.build_fleet(turn)

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

        for player in self.board.players:
            print('     Player:', player.player_number, '| Type:',
                  player.type, '| Status:', player.status)
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
