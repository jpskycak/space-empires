import random
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
from player.strategies import DumbStrategy
import sys
sys.path.append('src')


class DumbPlayer(Player):
    def __init__(self, position, board_size, player_index, player_color):
        super().__init__(position, board_size, player_index, player_color)
        self.type = 'Dumb Player'
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        self.player_index = player_index
        self.player_color = player_color
        self.ships = [
            Scout(self, position, self.board_size, 1, True),
            Scout(self, position, self.board_size, 2, True),
            Scout(self, position, self.board_size, 3, True),
            Colony_Ship(self, position, self.board_size, 4, True),
            Colony_Ship(self, position, self.board_size, 5, True),
            Colony_Ship(self, position, self.board_size, 6, True)
        ]
        self.ship_yards = [
            Ship_Yard(self, position, self.board_size, 1, False),
            Ship_Yard(self, position, self.board_size, 2, False),
            Ship_Yard(self, position, self.board_size, 3, False),
            Ship_Yard(self, position, self.board_size, 4, False)
        ]
        self.home_base = Colony(
            self, position, self.board_size, 1, home_base=True)
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
        data_dict = {}
        for attribute, value in self.__dict__.items():
            if isinstance(value, list) and len(value) == 0:
                data_dict[attribute] = value
            elif isinstance(value, list) and not isinstance(value[0], int) and len(value) > 0:
                for _ in value:
                    data_dict[attribute] = {(ship.name, ship.ID): {
                        key: value for key, value in ship.__dict__.items() if key != 'player'} for ship in value}
            else:
                data_dict[attribute] = value
        self.strategy = DumbStrategy(data_dict, Player(
            (0, 0), self.board_size, '0', 'black'))
