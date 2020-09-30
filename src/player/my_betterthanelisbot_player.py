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
import random
import sys
sys.path.append('src')


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
        self.half_way_line = [(i, self.grid_size // 2)
                              for i in range(0, self.grid_size + 1)]

    def screen_ships(self, ships_at_x_y, board):
        return board.simple_sort(ships_at_x_y)

    def build_fleet(self, turn=0):
        #print('building a fleet')
        if self.other_player_not_attacking():  # if other player is not attacking
            while self.can_build_colony_ships():
                position = self.find_random_ship_yard().position
                ship_ID = len(self.ships) + 1
                ship = Colony_Ship(self, ship_ID, position,
                                   self.grid_size, True)
                self.ships.append(ship)
                self.creds -= ship.cost
                print('Player', self.player_number, 'just bought a', ship.name)
        else:  # if other player is attacking
            while self.can_build_dreadnaughts():
                position = self.find_closest_ship_yard_to_scout_death().position
                ship_ID = len(self.ships) + 1
                ship = Dreadnaught(self, ship_ID, position,
                                   self.grid_size, True)
                self.ships.append(ship)
                self.creds -= ship.cost
                print('Player', self.player_number, 'just bought a', ship.name)

    def can_build_colony_ships(self):
        return self.finished_basic_upgrades and self.creds >= 8

    def can_build_dreadnaughts(self):
        return self.finished_basic_upgrades and self.creds >= 24

    def find_closest_ship_yard_to_scout_death(self):
        closest_ship_yard = self.ship_yards[0]
        for sy in self.ship_yards[1:]:
            if self.distance(sy.position, self.dead_scout_position) < self.distance(closest_ship_yard.position, self.dead_scout_position):
                closest_ship_yard = sy
        return closest_ship_yard

    def distance(self, pos_1, pos_2):
        return ((pos_2[0]-pos_1[0]) ** 2 + (pos_2[1]-pos_1[1]) ** 2) ** 0.5

    def will_colonize(self):
        return True

    def move(self, move_round, board):
        scouts = [ship for ship in self.ships if isinstance(ship, Scout)]
        if not self.scouts_in_correct_half_line_position(scouts):
            for i, scout in enumerate(scouts):
                scout.move_to_position(self.half_way_line[i], move_round)
        for ship in self.ships not in scouts:
            if isinstance(ship, Colony_Ship):
                ship.move_to_nearest_planet(board)

    def scouts_in_correct_half_line_position(self, scouts):
        if len(scouts) < 14:
            for scout in scouts:
                if scout.position not in self.half_way_line:
                    return False
            return True
        else: return False

    def decide_ship_movement(self, ship, board, move_round, game = None):
        new_ship = ship
        if isinstance(new_ship, Colony_Ship):
            new_ship.move_to_nearest_planet(board)
        elif isinstance(new_ship, Scout):
            half_way_line_index = [ship for ship in self.ships if isinstance(ship, Scout)].index(new_ship)
            new_ship.move_to_position(self.half_way_line[half_way_line_index], move_round)
        return new_ship.position




