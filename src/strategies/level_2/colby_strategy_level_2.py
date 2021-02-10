import sys
sys.path.append('src')
import random
from strategies.basic_strategy import BasicStrategy

class ColbyStrategyLevel2(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'ColbyStrategyLevel2'

    def decide_purchases(self, hidden_game_state):
        purchases = {'units': [], 'technology': []}
        total_cost = 0
        while hidden_game_state['players'][self.player_index]['cp'] >= total_cost:
            purchases['units'].append({'type': 'Scout', 'coords': hidden_game_state['players'][self.player_index]['home_coords']})
            total_cost += 6
        return purchases

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent = hidden_game_state['players'][1 - self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if unit_index == 0 and unit['coords'][0] != 1:
            return (-1,0)
        elif unit_index == 1 and unit['coords'][0] != 3:
            return (1,0)
        elif (unit_index == 0 or unit_index == 1) and (unit['coords'][0] != 1 or unit['coords'][0] != 3) and unit['coords'][1] < 4:
            return (0,1)
        else:
            translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
            best_translation = (0,0)
            smallest_distance_to_opponent = 999999999999
            for translation in translations:
                delta_x, delta_y = translation
                x = x_unit + delta_x
                y = x_unit + delta_y
                dist = abs(x - x_opp) + abs(y - y_opp)
                if dist < smallest_distance_to_opponent:
                    best_translation = translation
                    smallest_distance_to_opponent = dist
            return best_translation
