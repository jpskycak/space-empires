import random
from board import Board
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


class Player:
    def __init__(self, position, grid_size, player_number, player_color, board):
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        self.player_number = player_number
        self.player_color = player_color
        # starts out with 8 scouts later it would be 3 miners
        self.grid_size = grid_size
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
        self.home_base = Colony(self, 1, position, self.grid_size, home_base = True)
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
        self.board = board

    def find_random_ship_yard(self):
        return self.ship_yards[random.randint(0, len(self.ship_yards) - 1)]

    def find_amount_of_hull_size_building_capiblity(self, position):
        total_ship_yards_at_position = 0
        for ship_yard in self.ship_yards:
            if ship_yard.position == position:
                total_ship_yards_at_position += self.ship_yard_tech

    def build_fleet(self, turn = 0):
        print('building a fleet')
        position = self.find_random_ship_yard().position
        while self.can_build_ships():
            self.ship_to_build = self.determine_availible_ship_classes()
            ship_ID = len(self.ships) + 1
            ship = self.create_ship(self.ship_to_build, ship_ID, position)
            if ship.cost <= self.creds:
                self.ships.append(ship)
                self.creds -= ship.cost
                print('Player', self.player_number, 'just bought a', ship.name)
    
    def can_build_ships(self):
        if self.creds >= 6:
            return True
        else:
            return False

    def income(self):
        income = 0
        for colony in self.colonies: income += colony.income
        income += self.home_base.income
        return income

    def upgrade_movement_tech(self):
        self.movement_tech_upgrade_number += 1
        if self.movement_tech_upgrade_number == 1:
            self.movement_tech[2] == 2
        elif self.movement_tech_upgrade_number == 2:
            self.movement_tech[1] == 2
        elif self.movement_tech_upgrade_number == 3:
            self.movement_tech[0] == 2
        elif self.movement_tech_upgrade_number == 4:
            self.movement_tech[2] == 3
        elif self.movement_tech_upgrade_number == 5:
            self.movement_tech[1] == 3
        print('Player', self.player_number, "upgraded their max movement speed from", self.movement_tech_upgrade_number - 1, 'to', self.movement_tech_upgrade_number)

    def maintenance(self):
        for ship in self.ships:
            if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                cost = ship.defense_tech + ship.defense + ship.armor
                if self.creds >= cost: self.creds -= cost
                else:
                    self.ships.remove(ship)
                    print('Player', self.player_number, "couldn't maintain their", ship.name)

    def screen_ships(self, ships_at_x_y, board):
        print('ships_at_x_y', ships_at_x_y)
        players = self.get_players_in_list(ships_at_x_y)
        player_ships = [[ship for ship in ships_at_x_y] for player in players]
        print('player_ships', player_ships)
        for ships_1 in player_ships:
            for ships_2 in player_ships[player_ships.index(ships_1):player_ships.index(ships_1) + 1]:
                while len(ships_1) > len(ships_2):
                    ships_1.pop(-1)
        ships_arr = []
        for ships in player_ships:
            for ship in ships:
                ships_arr.append(ship)
        return board.simple_sort(ships_arr)

    def get_players_in_list(self, ships):
        players = []
        for ship in ships:
            if ship.player not in players:
                players.append(ship.player)

        return players

    # check stuffs
    def check_colonization(self, board):
        print('check colonization')
        for ship in self.ships:
            if isinstance(ship, Colony_Ship):
                for planet in board.planets:
                    if ship.x == planet.x and ship.y == planet.y and not planet.is_colonized:
                        print('it do be colonized')
                        if ship.terraform_tech >= planet.tier - 1:  # if the colony ship can colonize the planet
                            print('Player', self.player_number, 'just colonized a tier', planet.tier, 'planet at co-ords:', (planet.x, planet.y))
                            board.create_colony(self, planet, planet.position)
                            self.ships.remove(ship)
                        else:
                            print('Player', self.player_number, "can't colonize a tier", planet.tier, 'planet at co-ords:', (planet.x, planet.y), 'because their terraform tech is', ship.terraform_tech)

    # helper functions
    def determine_availible_ship_classes(self):
        if self.creds > 30 and self.ship_size_tech >= 6: return random.randint(1, 7)
        elif self.creds < 30 and self.creds >= 25 and self.ship_size_tech >= 5: return random.randint(1, 6)
        elif self.creds < 25 and self.creds >= 20 and self.ship_size_tech >= 4: return random.randint(1, 5)
        elif self.creds < 20 and self.creds >= 15 and self.ship_size_tech >= 3: return random.randint(1, 4)
        elif self.creds < 15 and self.creds >= 12 and self.ship_size_tech >= 2: return random.randint(1, 3)
        elif self.creds < 12 and self.creds >= 9 and self.ship_size_tech >= 1: return random.randint(1, 2)
        elif self.creds < 9 and self.creds >= 6 and self.ship_size_tech >= 0: return 1
        else: return None

    def create_ship(self, ship_class, ID, position):
        if ship_class == 1:
            scout_colony_ship_decoy_or_miner = random.randint(1, 4)
            if scout_colony_ship_decoy_or_miner == 1: return Scout(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 2: return Colony_Ship(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 3: return Decoy(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 4: return Miner(self, ID, position, self.grid_size, True)
        elif ship_class == 2: return Destroyer(self, ID, position, self.grid_size, True)
        elif ship_class == 3: return Cruiser(self, ID, position, self.grid_size, True)
        elif ship_class == 4: return BattleCruiser(self, ID, position, self.grid_size, True)
        elif ship_class == 5: return Battleship(self, ID, position, self.grid_size, True)
        elif ship_class == 6: return Dreadnaught(self, ID, position, self.grid_size, True)
        elif ship_class == 7: return Carrier(self, ID, position, self.grid_size, True)
        elif ship_class == 8: return Colony_Ship(self, ID, position, self.grid_size, True)
        else: return Scout(self, ID, position, self.grid_size, True)
