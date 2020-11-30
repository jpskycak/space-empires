import sys
import random
sys.path.append('src')
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

class BasicStrategy: #no movement or actual strategy, just funcitons like decide_removals or decide_which_ship_to_attack or simple_sort
    def __init__(self, player_dict, player):#wutever we need):
        self.player_dict = player_dict
        self.player = player #just an empty class to call functions and stuffs
        self.__name__ = 'BasicStrategy'

    def decide_removals(self, game_state, turn):
        if turn == 1: return None
        else: return self.simple_sort(game_state['players'][self.player_dict['player_number']-1]['ships'])[-1]

    def decide_which_ship_to_attack(self, attacking_ship, position, game_state):
        return self.strongest_enemy_ship(game_state[position])

    def simple_sort(self, ship_dict):
        fixed_arr, sorted_arr = [], []
        for _, ship_attributes in ship_dict.items():
            if ship_attributes['name'] != 'Decoy' and ship_attributes['name'] != 'Colony Ship' and ship_attributes['name'] != 'Miner' and ship_attributes['name'] != 'Colony':
                fixed_arr.append(ship_attributes)
        while len(fixed_arr) > 0:
            sorted_arr.append(self.max_value(fixed_arr))
            fixed_arr.remove(self.max_value(fixed_arr))
        return sorted_arr

    def max_value(self, arr):
        strongest_ship = arr[0]
        for ship in arr[1:]:
            if self.ship_1_fires_first(ship, strongest_ship):
                strongest_ship = ship
        return strongest_ship

    def ship_1_fires_first(self, ship_1, ship_2):
        if ship_1['fighting_class'] > ship_2['fighting_class']: return True
        elif ship_1['fighting_class'] < ship_2['fighting_class']: return False
        else:
            if ship_1['attack_tech'] > ship_2['attack_tech']: return True
            elif ship_1['attack_tech'] < ship_2['attack_tech']: return False
            else:
                if ship_1['attack'] > ship_2['attack']: return True
                elif ship_1['attack'] < ship_2['attack']: return False
                else: return True

    def strongest_enemy_ship(self, game_state_ship_list):
        for ship_attributes in game_state_ship_list:
            if ship_attributes['player']['player_number'] != self.player_dict['player_number']: return ship_attributes

    def decide_ship_placement(self, game_state):
        return self.player_dict['ship_yards']['Ship Yard', random.randint(1, len(self.player_dict['ship_yards']))]['x'], self.player_dict['ship_yards']['Ship Yard', random.randint(1, len(self.player_dict['ship_yards']))]['y']

    def will_colonize(self, game_state):
        return False

class DumbStrategy(BasicStrategy):
    def __init__(self, player_dict, player):#wutever else we need):
        self.player_dict = player_dict
        self.player = player #just an empty class to call functions and stuffs
        self.__name__ = 'DumbStrategy'

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return Scout(None, (0,0), 0, 0, True)

    def decide_ship_movement(self, ship, game_state, movement_round):
        x,y = ship['x'], ship['y']
        if ship['x'] < self.player_dict['grid_size']:
            x += ship['movement_tech'][movement_round]
        return x, y

class CombatStrategy(BasicStrategy):
    def __init__(self, player_dict, player):#wutever else we need):
        self.player_dict = player_dict
        self.player = player #just an empty class to call functions and stuffs
        self.__name__ = 'CombatStrategy'
        self.previous_buy = Scout(None, (0,0), 0, 0, True)

    def decide_purchases(self, game_state):
        if game_state['turn'] == 1 and game_state['players'][self.player_dict['player_number']-1]['ship_size_tech'] == 0: return 7
        else: return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        if self.check_previous_buy() == 2: 
            self.previous_buy = Scout(None, (0,0), 0, 0, True)
            return Scout(None, (0,0), 0, 0, True)
        if self.check_previous_buy() == 1: 
            self.previous_buy = Destroyer(None, (0,0), 0, 0, True)
            return Destroyer(None, (0,0), 0, 0, True)


    def check_previous_buy(self):
        if isinstance(self.previous_buy, Scout): return 1
        elif isinstance(self.previous_buy, Destroyer): return 2

    def decide_ship_movement(self, ship, game_state, movement_round):
        center_point_x, center_point_y = game_state['grid_size'] // 2, game_state['grid_size'] // 2
        x, y = ship['x'], ship['y']
        if x != center_point_x:
            if x < center_point_x:
                x += ship['movement_tech'][movement_round]
            elif x > center_point_x:
                x -= ship['movement_tech'][movement_round]  
        if y != center_point_y:
            if y < center_point_y:
                y += ship['movement_tech'][movement_round]
            elif y > center_point_y:
                y -= ship['movement_tech'][movement_round]
        return x, y

''' W.I.P.
class BestStrategy(BasicStrategy):
    def __init__(self, player_dict, Player): #wutever els we need):
        self.player_dict = player_dict #not gonna be actual player it gonna be the player class for the functions its not gonna have any actual data
        self.player = Player((0, 0), player_dict['grid_size'], '0', 'black') #just an empty class to call functions and stuffs

    def will_colonize_planet(self, colony_ship, game_state): #game not yet inputed cause infinite import loop bad
        return True#isinstance(colony_ship, Colony_Ship) and colony_ship.x == planet.x and colony_ship.y == planet.y and not planet.is_colonized

    def decide_ship_movement(self, ship, game_state, movement_round):
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
            if self.player.decoys_in_correct_half_line_position(): return Colony_Ship(None, (0,0), 0, 0, True)
            else: return Decoy
        elif self.finished_basic_upgrades() and self.other_player_is_attacking(): return Dreadnaught(None, (0,0), 0, 0, True)

    def decide_ship_purchases(self, game_state):
        if self.finished_basic_upgrades() and not self.other_player_is_attacking():
            if self.player.decoys_in_correct_half_line_position(): return Colony_Ship
            else: return Decoy
        elif self.finished_basic_upgrades() and self.other_player_is_attacking(): return Dreadnaught

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
        '''