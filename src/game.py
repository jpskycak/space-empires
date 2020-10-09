import random
from board import Board
from board import Planet
from logger import Logger
from player.player import Player
from player.deprecated_dumb_player import DumbPlayer
from player.random_player import RandomPlayer
from player.deprecated_combat_player import CombatPlayer
from player.mybotisbetterthanelisbot_player import ColbyStrategyPlayer
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
    def __init__(self, grid_size, asc_or_dsc, type_of_player, max_turns=1000):
        self.grid_size = grid_size  # ex [5,5]
        self.game_won = False
        self.players_dead = 0
        self.board = Board(grid_size, asc_or_dsc)
        self.max_turns = max_turns
        self.type_of_player = type_of_player
        self.player = Player((0, 0), self.grid_size, '0',
                             'black')
        self.combat_engine = CombatEngine(
            self.board, self, self.grid_size, asc_or_dsc)
        self.log = Logger(self.board)

    # main functions
    def initialize_game(self):
        self.players = self.create_players()
        self.board.create_planets_and_asteroids()
        self.log.get_next_active_file('logs')

    def create_players(self):
        starting_positions = [[self.grid_size // 2, 0], [self.grid_size // 2, self.grid_size], [0, self.grid_size // 2], [self.grid_size, self.grid_size // 2]]  # players now start at the axis' and not the corners
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i in range(0, 2):
            if self.type_of_player == 1: players.append(DumbPlayer(starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 2: players.append(RandomPlayer(starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 3: players.append(CombatPlayer(starting_positions[i], self.grid_size, i + 1, colors[i]))
            if self.type_of_player == 4: players.append(ColbyStrategyPlayer((starting_positions[i], self.grid_size, i + 1, colors[i])))
        return players

    def play(self):
        self.turn = 1
        self.state_obsolete()
        self.player_has_not_won = True
        print('---------------------------------------------')
        while self.check_if_player_has_won() and self.turn <= self.max_turns:
            self.complete_turn(self.turn)
            self.log.log_info(self.turn)
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
        self.complete_move_phase(self.turn)
        self.state_obsolete()
        self.generate_state()
        print('--------------------------------------------------')
        print('Combat Phase')
        self.complete_combat_phase()
        self.state_obsolete()
        self.generate_state()
        print('--------------------------------------------------')
        if self.turn < self.max_turns:
            print('Economic Phase')
            self.complete_economic_phase(self.turn)
            for player in self.players:
                print('Player', player.player_number, 'Has',
                      player.creds, 'creds extra after the economic phase.')
            self.state_obsolete()
            self.generate_state()
            print('--------------------------------------------------')
        self.board.update_board()

    def generate_state(self, phase, round_ = 0, first_player):
        self.game_state = {'turn': self.turn, 'phase': phase, 'round': round_, 'player': first_player, 'combat': 'coming soon to a dank river valley near you | if you get the reference u will soon date a thicc e-girl'}
        players = {}
        for i, player in enumerate(self.players):
            player_attributes = {}
            for attribute, value in player.__dict__.items():
                for unit in value:
                    if isinstance(value, list) and not isinstance(value[0], int): player_attributes[attribute] = {unit.name: {unit_attribute: unit_value for unit_attribute, unit_value in unit.__dict__.items()} for unit in value}
                    else: player_attributes[attribute] = value
                    players.apend(player_attributes)
        self.game_state['players'] = players
        planets = []
        for x in range(0, self.grid_size + 1):
            for y in range(0, self.grid_size + 1):
                if self.has_planets(self.board.misc_dict[(x,y)]):
                    for planet in [planet for planet in self.board.misc_dict[(x,y)] if isinstance(planet, Planet)]:
                        planets.append(self.board.misc_dict[(x,y)]) #get asteroids and etc stuff
        self.game_state['planets'] = planets

    def complete_move_phase(self):
        for player in self.players:
            player.check_colonization(self.board)
            for move_round in range(0, 3):  # 3 rounds of movements
                for ship in player.ships:
                    ship.position = player.strategy.decide_ship_movement(ship, self.game_state)

    def complete_combat_phase(self):
        possible_fights = self.combat_engine.possible_fights()
        for _, ships in possible_fights.items():
            self.combat_engine.complete_all_combats(ships)
    
    def complete_economic_phase(self):
        for player in self.players:
            player.creds += self.income(player)
            self.maintenance(player)
            purchase = player.strategy.decide_purchases(self.game_state)
            if not isinstance(purchase, int): #if its not an upgrade
                while player.creds >= purchase.cost: player.ships.append(purchase)
            else: #if it iss an upgrade
                while self.can_upgrade():
                    upgrade = player.strategy.decide_purchases(self.game_state)
                    player.upgrade(upgrade)

    def can_upgrade(self):
        return self.creds > 10 * self.attack_tech and self.creds > 10 * self.defense_tech and self.creds > 5 * self.fighting_class_tech + 10 and self.creds > 10 * self.movement_tech_upgrade_number + 10 and self.creds > 10 * self.ship_yard_tech and self.creds > 15 * self.terraform_tech

    def income(self, player):
        income = 0
        for colony in player.colonies:
            income += colony.income
        income += player.home_base.income
        return income

    def maintenance(self, player)
        for ship in player.ships:
                if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                    cost = ship.defense_tech + ship.defense + ship.armor
                    if player.creds >= cost:
                        player.creds -= cost
                    else:
                        player.strategy.decide_removals(self.game_state)
                        print('Player', self.player_number, "couldn't maintain their", ship.name)

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
