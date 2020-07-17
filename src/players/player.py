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


class Player(Board):
    def __init__(self, position, grid_size, player_number, player_color):
        super().__init__(grid_size)
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        self.player_number = player_number
        self.player_color = player_color
        # starts out with 3 scouts and 3 colony ships later it would be 3 miners
        self.ships = [
            Scout(1, position, self.grid_size, True),
            Scout(2, position, self.grid_size, True),
            Scout(3, position, self.grid_size, True),
            Colony_Ship(4, position, self.grid_size, True),
            Colony_Ship(5, position, self.grid_size, True),
            Colony_Ship(6, position, self.grid_size, True)
        ]
        self.ship_yards = [
            Ship_Yard(1, position, self.grid_size, False),
            Ship_Yard(2, position, self.grid_size, False),
            Ship_Yard(3, position, self.grid_size, False),
            Ship_Yard(4, position, self.grid_size, False)
        ]
        self.colonies = [Colony(1, position, grid_size)]
        self.starting_position = position
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.terraform_tech = 0
        self.ship_size_tech = 0
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0

    def find_amount_of_hull_size_building_capiblity(self, position):
        total_ship_yards_at_position = 0
        for ship_yard in self.ship_yards:
            if ship_yard.position == position:
                total_ship_yards_at_position += self.ship_yard_tech

    def upgrade_movement_tech(self):
        self.movement_tech_upgrade_number += 1
        if self.movement_tech_upgrade_number == 1:
            self.movement_tech[2] == 2

        if self.movement_tech_upgrade_number == 2:
            self.movement_tech[1] == 2

        if self.movement_tech_upgrade_number == 3:
            self.movement_tech[0] == 2

        if self.movement_tech_upgrade_number == 4:
            self.movement_tech[2] == 3

        if self.movement_tech_upgrade_number == 5:
            self.movement_tech[1] == 3

    def maintenance(self):
        for ship in self.ships:
            if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                cost = ship.defense_tech + ship.defense + ship.armor

                if self.creds >= cost:
                    self.creds -= cost

                else:
                    self.ships.remove(ship)
                    print('Player', self.player_number,
                          "couldn't maintain their", ship.name)

    # helper functions
    def determine_availible_ship_classes(self, creds):
        if self.creds > 30 and self.ship_size_tech >= 6:
            return random.randint(1, 7)
        elif self.creds < 30 and self.creds >= 25 and self.ship_size_tech >= 5:
            return random.randint(1, 6)
        elif self.creds < 25 and self.creds >= 20 and self.ship_size_tech >= 4:
            return random.randint(1, 5)
        elif self.creds < 20 and self.creds >= 15 and self.ship_size_tech >= 3:
            return random.randint(1, 4)
        elif self.creds < 15 and self.creds >= 12 and self.ship_size_tech >= 2:
            return random.randint(1, 3)
        elif self.creds < 12 and self.creds >= 9 and self.ship_size_tech >= 1:
            return random.randint(1, 2)
        elif self.creds < 9 and self.creds >= 6 and self.ship_size_tech >= 0:
            return 1
        else:
            return None

    def create_ship(self, ship_class, ID, position):
        if ship_class == 1:
            scout_colony_ship_decoy_or_miner = random.randint(1, 4)
            if scout_colony_ship_decoy_or_miner == 1:
                return Scout(ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 2:
                return Colony_Ship(ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 3:
                return Decoy(ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 4:
                return Miner(ID, position, self.grid_size, True)
        elif ship_class == 2:
            return Destroyer(ID, position, self.grid_size, True)
        elif ship_class == 3:
            return Cruiser(ID, position, self.grid_size, True)
        elif ship_class == 4:
            return BattleCruiser(ID, position, self.grid_size, True)
        elif ship_class == 5:
            return Battleship(ID, position, self.grid_size, True)
        elif ship_class == 6:
            return Dreadnaught(ID, position, self.grid_size, True)
        elif ship_class == 7:
            return Carrier(ID, position, self.grid_size, True)
        elif ship_class == 8:
            return Colony_Ship(ID, position, self.grid_size, True)
        else:
            return Scout(ID, position, self.grid_size, True)
