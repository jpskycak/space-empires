'''
from strategies.basic_strategy import BasicStrategy
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
import sys
import random
sys.path.append('src')

W.I.P.
class ColbyStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index

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