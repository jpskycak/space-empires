import sys
sys.path.append('src')
from player.player import Player
from board import Board
from board import Planet
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
from player.strategies import BasicStrategy



class ColbyStrategyPlayer(Player):
    def __init__(self, position, grid_size, player_number, player_color):
        super().__init__(position, grid_size, player_number, player_color)
        self.type = "'Better than Eli's bot' Player"
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        # starts out with 3 scouts and 3 colony ships later it would be 3 miners
        self.ships = [
            Scout(self, 1, position, self.grid_size, True),
            Scout(self, 2, position, self.grid_size, True),
            Scout(self, 3, position, self.grid_size, True),
            Colony_Ship(self, 4, position, self.grid_size, True),
            Colony_Ship(self, 5, position, self.grid_size, True),
            Colony_Ship(self, 6, position, self.grid_size, True)
        ]
        self.ship_yards = [
            Ship_Yard(self, 1, position, self.grid_size, False),
            Ship_Yard(self, 2, position, self.grid_size, False),
            Ship_Yard(self, 3, position, self.grid_size, False),
            Ship_Yard(self, 4, position, self.grid_size, False)
        ]
        self.home_base = Colony(
            self, 1, position, self.grid_size, home_base=True)
        self.colonies = []
        self.starting_position = position
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.terraform_tech = 0
        self.ship_size_tech = 0
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0
        self.ship_to_build = 2
        self.half_way_line = [(i, self.grid_size // 2) for i in range(0, self.grid_size + 1)]
        self.strategy = BestStrategy(Player(self.starting_position, self.grid_size, self.player_number, player_color))

    def screen_ships(self, ships_at_x_y, board):
        return board.simple_sort(ships_at_x_y)

    def build_fleet(self, turn=0):
        #print('building a fleet')
        if self.other_player_not_attacking():  # if other player is not attacking
            while self.can_build_colony_ships():
                position = self.find_random_ship_yard().position
                ship = Colony_Ship(self, position, self.grid_size, True)
                self.ships.append(ship)
                self.creds -= ship.cost
                print('Player', self.player_number, 'just bought a', ship.name)
        else:  # if other player is attacking
            while self.can_build_dreadnaughts():
                position = self.find_closest_ship_yard_to_scout_death().position
                ship = Dreadnaught(self, position, self.grid_size, True)
                self.ships.append(ship)
                self.creds -= ship.cost
                print('Player', self.player_number, 'just bought a', ship.name)

    def can_build_colony_ships(self):
        return self.finished_basic_upgrades and self.creds >= 8

    def can_build_dreadnaughts(self):
        return self.finished_basic_upgrades and self.creds >= 24

    def will_colonize(self):
        return True




