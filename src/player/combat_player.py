from player.player import Player
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
import random
import sys
sys.path.append('src')


class CombatPlayer(Player):
    def __init__(self, position, grid_size, player_number, player_color):
        super().__init__(position, grid_size, player_number, player_color)
        self.type = 'Combat Player'
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
        self.colonies = [Colony(self, 1, position, grid_size)]
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

    def upgrade(self, turn):  # actual function should be in here because you can only upgrade new ships not ones in the field
        print('upgrading')
        if turn == 1:
            if self.ship_size_tech < 6:  # biggest ship size that you can build
                self.ship_size_tech += 1
                self.creds -= 5 * self.ship_size_tech + 10
                print('Player', self.player_number, "upgraded their max building size from", self.ship_size_tech - 1, 'to', self.ship_size_tech)
        else:
            while self.can_upgrade():
                stat_to_upgrade = random.randint(1, 6)
                print('stat_to_upgrade', stat_to_upgrade)
                if stat_to_upgrade == 1 and self.attack_tech < 3:  # offense
                    self.attack_tech += 1
                    self.creds -= 10 * self.attack_tech
                    print('Player', self.player_number, 'upgraded their attack strength from', self.attack_tech - 1, 'to', self.attack_tech)
                elif stat_to_upgrade == 2 and self.defense_tech < 3:  # defense
                    self.defense_tech += 1
                    self.creds -= 10 * self.defense_tech
                    print('Player', self.player_number, 'upgraded their defense strength from', self.defense_tech - 1, 'to', self.defense_tech)
                elif stat_to_upgrade == 3 and self.fighting_class_tech < 3:  # tactics
                    self.fighting_class_tech += 1
                    self.creds -= 5 * self.fighting_class_tech + 10
                    print('Player', self.player_number, 'upgraded their fighting class from', self.fighting_class_tech - 1, 'to', self.fighting_class_tech)
                elif stat_to_upgrade == 4 and self.movement_tech_upgrade_number < 5:  # speed
                    self.upgrade_movement_tech()
                elif stat_to_upgrade == 5 and self.ship_yard_tech < 2:  # ship yard
                    self.ship_yard_tech += 0.5
                    self.creds -= 10 * self.ship_yard_tech
                    print('Player', self.player_number, "upgraded their ship-yard's building size from", self.ship_yard_tech - 1, 'to', self.ship_yard_tech)
                elif stat_to_upgrade == 6 and self.terraform_tech < 2:  # terraform
                    self.terraform_tech += 1
                    self.creds -= 15 * self.terraform_tech
                    print('Player', self.player_number, "upgraded their ablility to terraform from", self.terraform_tech - 1, 'to', self.terraform_tech)
                else:
                    break
 
    def move(self):
        for ship in self.ships: ship.move_to_centre()

    # helper functions
    def determine_availible_ship_classes(self):
        if self.ship_to_build == 2 and self.creds >= 6: self.ship_to_build = 1
        elif self.ship_to_build == 1 and self.creds >= 12: self.ship_to_build = 2
        else: return None
        return self.ship_to_build

    def create_ship(self, ship_class, ID, position):
        if ship_class == 1: return Scout(self, ID, position, self.grid_size, True)
        elif ship_class == 2: return Destroyer(self, ID, position, self.grid_size, True)
