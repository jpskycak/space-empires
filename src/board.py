import random
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


class Board:
    # grid_size is grid size and player_positions is the array of the home bases of players
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.players = []
        self.player_home_bases = [
            [1, 1], [self.grid_size - 1, self.grid_size - 1]]

    # create <instert thing here> stuffs
    def create_planets_and_asteroids(self):
        print('create planets and asteroids')
        self.planets = []
        self.asteroids = []
        for player_position in self.player_home_bases:  # create home base
            self.create_planet(player_position)

        for i in range(0, self.grid_size + 1):

            for j in range(0, self.grid_size + 1):
                # 1,2 is a planet and 3,4,5,6,7,8 are asteroids
                planet_or_asteroid = random.randint(1, 8)

                if planet_or_asteroid <= 2:
                    self.planets.append(self.create_planet([i, j]))

                elif planet_or_asteroid > 2:
                    self.asteroids.append(self.create_asteroid([i, j]))

    def create_planet(self, position):
        tier = random.randint(1, 3)
        return Planet(position, tier)

    def create_asteroid(self, position):
        size = random.randint(1, 3)
        tier = random.randint(1, 5)
        return Asteroid(position, size, tier)

    def create_colony(self, player, planet, position):
        planet.is_colonized = True
        player.colonies.append(
            Colony(self, len(player.colonies) + 1, position, self.grid_size))

    # combat stuffs
    def list_of_ships_at_x_y(self, players, x, y):
        all_data = []
        temp = []
        ships_arr = []
        print('x, y', x, y)
        ships_arr = []
        for player in players:  # array of ships
            
            for ship in player.ships:
                
                if ship.x == x and ship.y == y:
        
                    if ship.name != Colony_Ship or ship.name != Decoy or ship.name != Miner:  # if it can fight
                        print('yes 1')
                        ships_arr.append(ship)

                    else:  # if not then die
                        player.ships.remove(ship)

        print('ships', ships_arr)

            #for player in self.players:
                #print('yes 1.5')
                #ships_arr = player.screen_ships(ships_arr, self)

        if len(ships_arr) > 0:
            print('yes 2')
            temp.append((x, y))
            temp.append(len(ships_arr))
            temp.append(ships_arr)
            all_data.append(temp)

        print('all_data', all_data)
        # ex --> ((0,0), (3, [ship_1, ship_2, ship_1], (1,0), (3, ([player_1, (ship_1)], [player_2, (ship_1, ship_2)]
        return all_data


class Planet:
    def __init__(self, position, tier):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        # self.size = size #max number of ship yards
        self.tier = tier  # habitiblity
        self.is_colonized = False
        self.ship_yards_at_planet = []


class Asteroid:
    def __init__(self, position, size, tier):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        # self.size = size #max number of ship yards
        self.tier = random.randint(0, 5)  # type of ore
        self.size = size  # scalar for tier
        # ex a tier 5 size 3 asteroird gives 15 creds while a tier 3 size 2 asteroid give 6 creds
