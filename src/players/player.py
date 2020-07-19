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
    def __init__(self, position, grid_size, player_number, player_color):
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
        self.colonies = [Colony(self, 1, position, self.grid_size)]
        self.starting_position = position
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.terraform_tech = 0
        self.ship_size_tech = 0
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0

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

    def find_random_ship_yard(self):
        return self.ship_yards[random.randint(0, len(self.ship_yards) - 1)]

    def find_amount_of_hull_size_building_capiblity(self, position):
        total_ship_yards_at_position = 0
        for ship_yard in self.ship_yards:
            if ship_yard.position == position:
                total_ship_yards_at_position += self.ship_yard_tech

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

    

    

    def screen_ship_combat(self, data):
        for position in data:
            players = []

            for player in position[1][1]:
                players.append(players)

            for player_1 in player:

                for player_2 in player:

                    if player_1 != player_2:

                        if len(player_1.ships) > len(player_2.ships):

                            for i in range(len(player_1.ships), len(player_2.ships), -1):
                                player_1.ships.pop()

                        elif len(player_1.ships) < len(player_2.ships):

                            for i in range(len(player_2.ships), len(player_1.ships), -1):
                                player_2.ships.pop()

        return data

    # check stuffs
    def check_colonization(self, board):
        print('check colonization')
        for ship in self.ships:

            if isinstance(ship, Colony_Ship):

                for planet in board.planets:

                    if ship.x == planet.x and ship.y == planet.y and not planet.is_colonized:
                        print('it do be colonized')
                        if ship.terraform_tech >= 4 - planet.tier:  # if the colony ship can colonize the planet
                            print('Player', self.player_number,
                                    'just colonized a tier', planet.tier,
                                    'planet at co-ords:',
                                    (planet.x, planet.y))
                            board.create_colony(
                                self, planet, planet.position)
                            index = self.ships.index(ship)
                            self.ships.remove(self.ships[index])

                        else:
                            print('Player', self.player_number,
                                    "can't colonize a tier", planet.tier,
                                    'planet at co-ords:',
                                    (planet.x, planet.y),
                                    'because their terraform tech is',
                                    ship.terraform_tech)

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
                return Scout(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 2:
                return Colony_Ship(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 3:
                return Decoy(self, ID, position, self.grid_size, True)
            if scout_colony_ship_decoy_or_miner == 4:
                return Miner(self, ID, position, self.grid_size, True)
        elif ship_class == 2:
            return Destroyer(self, ID, position, self.grid_size, True)
        elif ship_class == 3:
            return Cruiser(self, ID, position, self.grid_size, True)
        elif ship_class == 4:
            return BattleCruiser(self, ID, position, self.grid_size, True)
        elif ship_class == 5:
            return Battleship(self, ID, position, self.grid_size, True)
        elif ship_class == 6:
            return Dreadnaught(self, ID, position, self.grid_size, True)
        elif ship_class == 7:
            return Carrier(self, ID, position, self.grid_size, True)
        elif ship_class == 8:
            return Colony_Ship(self, ID, position, self.grid_size, True)
        else:
            return Scout(self, ID, position, self.grid_size, True)
