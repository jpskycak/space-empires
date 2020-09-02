import random
import sys
sys.path.append('src')
from unit.carrier import Carrier
from unit.decoy import Decoy
from unit.miner import Miner
from unit.base import Base
from unit.ship_yard import Ship_Yard
from unit.colony import Colony
from unit.colony_ship import Colony_Ship
from unit.dreadnaught import Dreadnaught
from unit.battleship import Battleship
from unit.battle_cruiser import BattleCruiser
from unit.cruiser import Cruiser
from unit.destroyer import Destroyer
from unit.scout import Scout
from unit.unit import Unit
from board import Board
from player.player import Player




class DumbPlayer(Player):
    def __init__(self, position, grid_size, player_number, player_color):
        super().__init__(position, grid_size, player_number, player_color)
        self.type = 'Dumb Player'
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        self.player_number = player_number
        self.player_color = player_color
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
        self.colonies = [Colony(self, 1, position, grid_size)]
        self.starting_position = position
        self.build_fleet()
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.terraform_tech = 0
        self.ship_size_tech = 0
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0

    def upgrade(self):
        self.build_fleet()

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

    def move(self):
        for ship in self.ships:
            ship.dumb_move()

    # helper functions
    def determine_availible_ship_classes(self, creds):
        if self.creds >= 6 and self.ship_size_tech >= 0:
            return 1
            
        else:
            return None

    def create_ship(self, ship_class, ID, position):
        return Scout(self, ID, position, self.grid_size, True)
