import random
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy


class Board:
    # board_size is grid size and player_positions is the array of the home bases of players
    def __init__(self, game, board_size, asc_or_dsc):
        self.board_size = board_size
        self.game = game
        self.player_home_bases = [[self.board_size[0] // 2, 0], [self.board_size[0] // 2, self.board_size[1]], [0, self.board_size[1] // 2], [
            self.board_size[0], self.board_size[1] // 2]]
        self.ships_dict = {}
        self.misc_dict = {}
        self.dice_roll_index = 0
        if asc_or_dsc == 'asc':
            self.rolls = [1, 2, 3, 4, 5, 6]
        elif asc_or_dsc == 'dsc':
            self.rolls = [6, 5, 4, 3, 2, 1]
        self.planets = []
        self.asteroids = []
        #print('asc_or_dsc', asc_or_dsc)

    def update_board(self):
        for x in range(0, self.board_size[0] + 1):
            for y in range(0, self.board_size[1] + 1):
                ships_arr = []
                for player in self.game.players:
                    player_ships = player.ships + player.ship_yards + [player.home_base]
                    for ship in player_ships:
                        if ship.x == x and ship.y == y:
                            ships_arr.append(ship)
                if len(ships_arr) > 0:
                    self.ships_dict[(x, y)] = self.simple_sort(ships_arr)

    # create <instert thing here> stuffs
    def create_planets_and_asteroids(self):
        #print('create planets and asteroids')
        self.planets = []
        self.asteroids = []
        positions = [(x,y) for x in range(0, self.board_size[0]) for y in range(0, self.board_size[1])]
        for (x,y) in positions:
            # 1,2 is a planet and 3,4, are asteroids and 5,6 are None
            if [x, y] != self.player_home_bases[0] and [x, y] != self.player_home_bases[1]:
                planet_or_asteroid = 1  # self.get_die_roll()
                if planet_or_asteroid <= 2:
                    self.misc_dict[(x, y)] = [self.create_planet([x, y])]
                    self.planets.append((x,y))
                    self.planets.append(self.create_planet([x, y]))
                elif planet_or_asteroid > 2 and planet_or_asteroid <= 4:
                    self.misc_dict[(x, y)] = [self.create_asteroid([x, y])]
                    self.asteroids.append(self.create_asteroid([x, y]))

    def create_planet(self, position):
        return Planet(position, random.randint(0,1))

    def create_asteroid(self, position):
        return Asteroid(position, random.randint(1,2))

    def create_colony(self, player, planet, position, turn_built):
        planet.is_colonized = True
        player.colonies.append(Colony(self, len(player.colonies) + 1, position, self.board_size, turn_built))

    def get_die_roll(self):
        if self.dice_roll_index == 5:
            self.dice_roll_index = 0
        else:
            self.dice_roll_index += 1
        return self.rolls[self.dice_roll_index]

    def simple_sort(self, arr):
        fixed_arr, sorted_arr = [ship for ship in arr if ship.type != 'Colony' and ship.type != 'Colony Ship' and ship.type != 'Decoy' and ship.type != 'Miner'], []
        for ship in [ship for ship in arr if ship not in fixed_arr]:
            if ship.type == 'Colony':
                ship.player.colonies.remove(ship)
            else:
                ship.player.ships.remove(ship)
        while len(fixed_arr) > 0:
            strongest_ship = max(fixed_arr, key=lambda ship: ship.technology['tactics'] + ship.technology['attack'] + ship.attack)
            sorted_arr.append(strongest_ship)
            fixed_arr.remove(strongest_ship)
        return sorted_arr

class Planet:
    def __init__(self, position, tier, is_colonized = False):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.tier = tier  # habitiblity
        self.is_colonized = False
        self.ship_yards_at_planet = []
        self.is_claimed = False  # for colony ships finding nearest planet

class Asteroid:
    def __init__(self, position, tier):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.income = 5 * tier
