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
import random
import sys
sys.path.append('src')


class Player:
    def __init__(self, game, strategy, position, board_size, player_index, player_color, colony_ships = False, ship_yards = False):
        self.game = game
        self.creds = 10
        self.is_alive = True
        self.death_count = 0  # if winCount = amount of units self.lose = true
        self.player_index = player_index
        self.player_color = player_color
        # starts out with 8 scouts later it would be 3 miners
        self.board_size = board_size
        self.new_ship_index = 4
        if ship_yards: self.ship_yards = [Ship_Yard(self, position, self.board_size, 1), Ship_Yard(self, position, self.board_size, 2), Ship_Yard(self, position, self.board_size, 3), Ship_Yard(self, position, self.board_size, 4)]
        else: self.ship_yards = []
        self.technology = {'attack': 0, 'defense': 0, 'movement': 1, 'shipsize': 1, 'shipyard': 1, 'terraform': 0, 'tactics': 0, 'exploration': 0}
        if colony_ships: self.ships = [Scout(self, position, self.board_size, 1), Scout(self, position, self.board_size, 2), Scout(self, position, self.board_size, 3), Colony_Ship(self, position, self.board_size, 4), Colony_Ship(self, position, self.board_size, 5), Colony_Ship(self, position, self.board_size, 6)]
        else: self.ships = [Scout(self, position, self.board_size, 1), Scout(self, position, self.board_size, 2), Scout(self, position, self.board_size, 3)]
        self.home_base = Colony(self, position, self.board_size, 1, home_base=True, turn_built = -1)
        self.colonies = []
        self.starting_position = position
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0
        self.strategy = strategy(int(player_index))

    def find_random_ship_yard(self):
        return self.ship_yards[random.randint()].position

    def find_amount_of_hull_size_building_capibility(self, position):
        total_hull_size_building_capibility_at_position = 0
        for ship_yard in self.ship_yards:
            if tuple(ship_yard.position) == position:
                total_hull_size_building_capibility_at_position += self.technology['shipyard']
        return total_hull_size_building_capibility_at_position

    def can_build_ships(self):
        return self.creds >= 6

    def upgrade(self, stat_to_upgrade, game_state):
        _, can_upgrade_bool = self.can_upgrade(stat_to_upgrade, game_state)
        if can_upgrade_bool:
            # offense
            if stat_to_upgrade == 'attack' and self.technology['attack'] < 3:
                self.technology['attack'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, 'upgraded their attack strength from', self.technology['attack'] - 1, 'to', self.technology['attack'])

            # defense
            elif stat_to_upgrade == 'defense' and self.technology['defense'] < 3:
                self.technology['defense'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, 'upgraded their defense strength from', self.technology['defense'] - 1, 'to', self.technology['defense'])

            # tactics
            elif stat_to_upgrade == 'tactics' and self.technology['tactics'] < 3:
                self.technology['tactics'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, 'upgraded their fighting class from', self.technology['tactics'] - 1, 'to', self.technology['tactics'])

            # speed
            elif stat_to_upgrade == 'movement' and self.technology['movement'] < 6:
                self.technology['movement'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, 'upgraded their movement speed from', self.technology['movement'] - 1, 'to', self.technology['movement'])

            # ship yard
            elif stat_to_upgrade == 'shipyard' and self.technology['shipyard'] < 2:
                self.technology['shipyard'] += 0.5
                if self.game.print_state_obsolete: print('Player', self.player_index, "upgraded their ship-yard's building size from", self.technology['shipyard'] - 0.5, 'to', self.technology['shipyard'])

            # terraform
            elif stat_to_upgrade == 'terraform' and self.technology['terraform'] < 2:
                self.technology['terraform'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, "upgraded their ablility to terraform from", self.technology['terraform'] - 1, 'to', self.technology['terraform'])

            # biggest ship size that you can build
            elif stat_to_upgrade == 'shipsize' and self.technology['shipsize'] < 6:
                self.technology['shipsize'] += 1
                if self.game.print_state_obsolete: print('Player', self.player_index, "upgraded their max building size from", self.technology['shipsize'] - 1, 'to', self.technology['shipsize'])

    def can_upgrade(self, stat_to_upgrade, game_state):
        return self.upgrade_cost(stat_to_upgrade, game_state), self.creds >= self.upgrade_cost(stat_to_upgrade, game_state)

    def upgrade_cost(self, stat_to_upgrade, game_state):
        return game_state['technology_data'][stat_to_upgrade][self.technology[stat_to_upgrade]]

    def screen_ships(self, ships_at_x_y, board):
        players = self.get_players_in_list(ships_at_x_y)
        player_ships = [[ship for ship in ships_at_x_y] for player in players]
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

    def generate_state(self, current_player=True, combat=False):
        if current_player:
            return {
                'name': self.strategy.__name__,
                'Is Alive': self.is_alive,
                'cp': self.creds,
                'id': self.player_index,
                'units': [unit.generate_state(current_player, combat) for unit in self.ships],
                'colonies': [colony.generate_state(current_player, combat) for colony in self.colonies], 
                'ship_yards': [ship_yard.generate_state(current_player, combat) for ship_yard in self.ship_yards],
                'technology': self.technology,
                'home_base': self.home_base.generate_state(current_player, combat),
                'home_coords': (self.home_base.x, self.home_base.y)
            }
        else:
            return {
                'name': self.strategy.__name__,
                'Is Alive': self.is_alive,
                'id': self.player_index,
                'units': [unit.generate_state(current_player, combat) for unit in self.ships],
                'colonies': [colony.generate_state(current_player, combat) for colony in self.colonies], 
                'ship_yards': [ship_yard.generate_state(current_player, combat) for ship_yard in self.ship_yards],
                'home_base': self.home_base.generate_state(current_player, combat),
                'home_coords': self.starting_position
            }

    # check stuffs
    def check_colonization(self, ship, board, hidden_game_state):
        for planet in board.planets:
            if self.can_colonize_planet(ship, planet) and self.strategy.will_colonize_planet((ship.x, ship.y), hidden_game_state):
                if ship.terraform_tech >= planet.tier - 1:
                    print('Player', self.player_index, 'just colonized a tier', planet.tier, 'planet at co-ords:', (planet.x, planet.y))
                    board.create_colony(self, planet, planet.position, hidden_game_state['turn'])
                    self.ships.remove(ship)
                    return True
                else:
                    print('Player', self.player_index, "can't colonize a tier", planet.tier, 'planet at co-ords:', (planet.x, planet.y), 'because their terraform tech is', ship.terraform_tech)
                    return False

    # game not yet inputed cause infinite import loop bad
    def can_colonize_planet(self, ship, planet, game=None):
        return ship.type == Colony_Ship and ship.x == planet.x and ship.y == planet.y and not planet.is_colonized
