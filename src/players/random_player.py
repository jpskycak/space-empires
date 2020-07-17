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

    def find_random_ship_yard(self):
        return self.ship_yards[random.randint(0, len(self.ship_yards) - 1)]

    def build_fleet(self):
        print('building a fleet')
        ship_yard = self.find_random_ship_yard()
        position = ship_yard.position
        self.find_amount_of_hull_size_building_capiblity(position)
        while self.creds >= 6:
            print(self.creds)
            ship_class = self.determine_availible_ship_classes(self.creds)
            if ship_class == None:
                break
            else:
                print('ship_class', ship_class)

                ship_ID = len(self.ships) + 1

                ship = self.create_ship(ship_class, ship_ID, position)
                print('ship name', ship.name)
                if ship.cost <= self.creds:
                    self.ships.append(ship)
                    self.creds -= ship.cost
                    print('Player', self.player_number, 'just bought a',
                          ship.name)

    def upgrade(self):  # actual function should be in here because you can only upgrade new ships not ones in the field
        print('upgrading')
        while self.creds > 10 * self.attack_tech and self.creds > 10 * self.defense_tech and self.creds > 5 * self.fighting_class_tech + 10 and self.creds > 10 * self.movement_tech_upgrade_number + 10 and self.creds > 10 * self.ship_yard_tech and self.creds > 15 * self.terraform_tech and self.creds > 5 * self.ship_size_tech + 10:
            stat_to_upgrade = random.randint(1, 7)
            print('stat_to_upgrade', stat_to_upgrade)
            if stat_to_upgrade == 1 and self.attack_tech < 3:  # offense
                self.attack_tech += 1
                self.creds -= 10 * self.attack_tech
                print('Player', self.player_number,
                      'upgraded their attack strength from',
                      self.attack_tech - 1, 'to', self.attack_tech)

            elif stat_to_upgrade == 2 and self.defense_tech < 3:  # defense
                self.defense_tech += 1
                self.creds -= 10 * self.defense_tech
                print('Player', self.player_number,
                      'upgraded their defense strength from',
                      self.defense_tech - 1, 'to', self.defense_tech)

            elif stat_to_upgrade == 3 and self.fighting_class_tech < 3:  # tactics
                self.fighting_class_tech += 1
                self.creds -= 5 * self.fighting_class_tech + 10
                print('Player', self.player_number,
                      'upgraded their fighting class from',
                      self.fighting_class_tech - 1, 'to',
                      self.fighting_class_tech)

            elif stat_to_upgrade == 4 and self.movement_tech_upgrade_number < 5:  # speed
                self.upgrade_movement_tech()

            elif stat_to_upgrade == 5 and self.ship_yard_tech < 2:  # ship yard
                self.ship_yard_tech += 0.5
                self.creds -= 10 * self.ship_yard_tech
                print('Player', self.player_number,
                      "upgraded their ship-yard's building size from",
                      self.ship_yard_tech - 1, 'to', self.ship_yard_tech)

            elif stat_to_upgrade == 6 and self.terraform_tech < 2:  # terraform
                self.terraform_tech += 1
                self.creds -= 15 * self.terraform_tech
                print('Player', self.player_number,
                      "upgraded their ablility to terraform from",
                      self.terraform_tech - 1, 'to', self.terraform_tech)

            elif stat_to_upgrade == 7 and self.ship_size_tech < 6:  # biggest ship size that you can build
                self.ship_size_tech += 1
                self.creds -= 5 * self.ship_size_tech + 10
                print('Player', self.player_number,
                      "upgraded their max building size from",
                      self.ship_size_tech - 1, 'to', self.ship_size_tech)

            else:
                break

    def move(self):
        # print('moving')
        # 0 is up   1 is right    2 is down   3 is left
        for ship in self.ships:
            direction = random.randint(0, 3)
            if ship.can_move:
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