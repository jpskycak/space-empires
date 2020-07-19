import random
from players.player import Player
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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# no functions because it inherits from the player class and is already random so ¯\_(ツ)_/¯
class RandomPlayer(Player):
    def __init__(self, position, grid_size, player_number, player_color):
        super().__init__(position, grid_size, player_number, player_color)
        self.type = 'Random Player'
        self.creds = 0
        self.death_count = 0  # if winCount = amount of units self.lose = true
        # starts out with 3 scouts and 3 colony ships later it would be 3 miners
        self.ships = [
            Scout(1, position, self.grid_size, True),
            Scout(2, position, self.grid_size, True),
            Scout(3, position, self.grid_size, True),
            Colony_Ship(4, position, self.grid_size, True),
            Colony_Ship(5, position, self.grid_size, True),
            Colony_Ship(6, position, self.grid_size, True)
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

    def move(self, dumb_player = False):
        # print('moving')
        # 0 is up   1 is right    2 is down   3 is left
        direction = random.randint(0, 3)
        for ship in self.ships:
            if self.can_move and not dumb_player:
                # print(direction)
                for i in range(0, len(self.movement_tech)):
                    for _ in range(0, self.movement_tech[i]):
                        if direction == UP:
                            if ship.y > 0:
                                ship.y -= 1
                            elif ship.y <= 0:
                                ship.y += 1
                        elif direction == DOWN:
                            if ship.y < self.grid_size:
                                ship.y += 1
                            elif ship.y >= self.grid_size:
                                ship.y -= 1
                        elif direction == RIGHT:
                            if ship.x < self.grid_size:
                                ship.x += 1
                            elif ship.x >= self.grid_size:
                                ship.x -= 1
                        elif direction == LEFT:
                            if ship.x > 0:
                                ship.x -= 1
                            elif ship.x <= 0:
                                ship.x += 1
