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
'''
class DumbStrategy:
    def __init__(self, wutever we need):
        self......
        ...
        ..
        .
        .
        .
    
class CombatStrategy:
    def __init__(self, wutever we need):
        self......
        ...
        ..
        .
        .
        .
'''
class BestStrategy:
    def __init__(self, player_dict): #wutever els we need):
        self.player = player #not gonna be actual player it gonna be the player class for the functions its not gonna have any actual data

    def will_colonize_planet(self, colony_ship, game_state): #game not yet inputed cause infinite import loop bad
        return True#isinstance(colony_ship, Colony_Ship) and colony_ship.x == planet.x and colony_ship.y == planet.y and not planet.is_colonized

    def decide_ship_movement(self, ship, game_state):
        new_ship = ship
        if isinstance(new_ship, Colony_Ship): new_ship.move_to_nearest_planet(board)
        elif isinstance(new_ship, Scout) and self.scouts_in_correct_half_line_position(scouts):
            half_way_line_index = [ship for ship in self.ships if isinstance(ship, Scout)].index(new_ship)
            new_ship.move_to_position(self.half_way_line[half_way_line_index], move_round)
        return new_ship.position
    
    def decide_purchases(self, game_state):
        if not self.finished_basic_upgrades() and not self.other_player_is_attacking():
            return self.upgrade()
        elif self.finished_basic_upgrades() and not self.other_player_is_attacking():
            if self.player.decoys_in_correct_half_line_position(): return Colony_Ship
            else: return Decoy
        elif self.finished_basic_upgrades() and self.other_player_is_attacking(): return Dreadnaught

    def decide_removals(game_state):
        return self.simple_sort(game_state[self.player])[-1]


    def decide_which_ship_to_attack(self, attacking_ship, position, game_state):
        return self.strongest_enemy_ship(game_state[position])

    def find_closest_ship_yard_to_decoy_death(self):
        closest_ship_yard = self.ship_yards[0]
        for sy in self.ship_yards[1:]:
            if self.distance(sy.position, self.dead_decoy_position) < self.distance(closest_ship_yard.position, self.dead_decoy_position):
                closest_ship_yard = sy
        return closest_ship_yard

    def distance(self, pos_1, pos_2):
        return ((pos_2[0]-pos_1[0]) ** 2 + (pos_2[1]-pos_1[1]) ** 2) ** 0.5

    def decoys_in_correct_half_line_position(self, decoys):
        if len(decoys) < 14:
            for decoy in decoys:
                if decoy.position not in self.half_way_line: return False
            return True
        else: return False

    def simple_sort(self, arr):
        fixed_arr, sorted_arr = [], []
        for ship in arr:
            if self.if_it_can_fight(ship):
                fixed_arr.append(ship)
            else:
                ship.player.ships.remove(ship)
        while len(fixed_arr) > 0:
            sorted_arr.append(self.max_value(fixed_arr))
            fixed_arr.remove(self.max_value(fixed_arr))
        return sorted_arr

    def max_value(self, arr):
        max_value = arr[0]
        for ship in arr[1:]:
            if self.ship_1_fires_first(ship, max_value):
                max_value = ship
        return max_value

    def strongest_enemy_ship(self, game_state_ship_list):
        for ship_attributes in game_state_ship_list:
            if ship['player']['player_number'] != self.player