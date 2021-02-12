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
    def __init__(self, player_strats, board_size, asc_or_dsc, print_state_obsolete=True, max_turns=10000, generate_planets=False, number_of_movement_rounds=3, economic_phase=True, number_of_economic_phases=10000, can_log=True, build_player_ship_yards=True):
        self.board_size = board_size  # ex [5,5]
        self.game_won = False
        self.board = Board(self, board_size, asc_or_dsc)
        self.max_turns = max_turns
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
            self.board_size[0] - 1, self.board_size[1] // 2]]  # players now start at the axis' and not the corners
        self.print_state_obsolete = print_state_obsolete
        self.generate_planets = generate_planets
        self.number_of_movement_rounds = number_of_movement_rounds
        self.economic_phase = economic_phase
        self.number_of_economic_phases = number_of_economic_phases
        self.build_player_ship_yards = build_player_ship_yards

    # main functions
    def initialize_game(self):
        self.players = self.create_players()
        if self.generate_planets:
            self.board.create_planets_and_asteroids()
        else:
            for i, _ in enumerate(self.player_strats):
                self.board.misc_dict[tuple(self.starting_positions[i])] = Planet(
                    self.starting_positions[i], 0, is_colonized=True)
        self.turn = 1
        self.generate_state(initial_state=True)
        if self.can_log:
            self.log.get_next_active_file('logs')

    def create_players(self):
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i, strategy in enumerate(self.player_strats):
            players.append(Player(
                self, strategy, self.starting_positions[i], self.board_size, i, colors[i], ship_yards=self.build_player_ship_yards))
        return players

    def play(self):
        self.generate_state()
        self.player_has_not_won = True
        if self.print_state_obsolete:
            print('Initial State')
            self.state_obsolete()
            print('--------------------------------------------------')
        while not self.game_won and not self.check_if_player_has_won() and self.turn <= self.max_turns:
            self.generate_state(current_player=None)
            if self.can_log: self.log.log_turn(self.game_state)
            self.complete_turn()
            self.turn += 1
        player_won = self.player_has_won()
        return player_won

    def player_has_won(self):
        is_alive = self.aliveness()
        if is_alive.count(True) == 1:
            for i, aliveness in enumerate(is_alive):
                if aliveness:
                    if self.print_state_obsolete: print(self.players[i].strategy.__name__, 'WINS!')
                    if self.can_log:
                        self.log.end_logs(player_who_won = self.players[i].generate_state(current_player=True))
                    return i
        return None

    def check_if_player_has_won(self):
        is_alive = self.aliveness()
        if is_alive.count(True) == 1:
            self.game_won = True
            return True
        else:
            self.game_won = False
            return False

    def aliveness(self):
        is_alive = []
        for player in self.players:
            if player.home_base.is_alive:
                player.is_alive = True
                is_alive.append(True)
            else:
                player.is_alive = False
                is_alive.append(False)
        return is_alive

    def complete_turn(self):
        if self.print_state_obsolete:
            print('Turn', self.turn)
        self.check_if_player_has_won()
        if not self.game_won:
            if self.turn < self.max_turns and self.economic_phase and self.turn <= self.number_of_economic_phases:
                self.generate_state(phase='Economic')
                if self.print_state_obsolete:
                    print('--------------------------------------------------')
                    print('Economic Phase')
                self.economic_engine.complete_all_taxes()
                for player in self.players:
                    if self.print_state_obsolete:
                        print('Player', player.player_index, 'Has', player.creds, 'creds extra after the economic phase.')
                if self.print_state_obsolete:
                    self.state_obsolete()
            self.generate_state(phase='Movement')
            if self.print_state_obsolete:
                print('--------------------------------------------------')
                print('Move Phase')
            self.movement_engine.complete_all_movements(self.number_of_movement_rounds)
            if self.print_state_obsolete:
                self.state_obsolete()
            self.generate_state(phase='Combat')
            if self.print_state_obsolete:
                print('--------------------------------------------------')
                print('Combat Phase')
            self.combat_engine.complete_all_fights()
            if self.print_state_obsolete:
                self.state_obsolete()
            
        self.board.update_board()

    def generate_state(self, current_player=None, phase=None, movement_round=0, initial_state=False):
        movement_state = self.movement_engine.generate_movement_state(
            movement_round)
        self.game_state = {
            'turn': self.turn,
            'winner': None,
            'board_size':  self.board_size,
            'phase': phase,
            'round': movement_state['round'],
            'unit_data': {
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
            },
            'technology_data': {
                'shipsize': [0, 10, 15, 20, 25, 30],
                'attack': [20, 30, 40],
                'defense': [20, 30, 40],
                'movement': [0, 20, 30, 40, 40, 40],
                'shipyard': [0, 20, 30]
            },
        }
        if current_player == None:
            self.game_state['players'] = [player.generate_state(current_player=True, combat=(phase == 'Combat')) for player in self.players]
        else:
            self.game_state['players'] = [player.generate_state(current_player=(current_player==player), combat=(phase == 'Combat')) for player in self.players]
        if phase == 'Combat':
            self.game_state['combat'] = self.combat_engine.generate_combat_array()

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
