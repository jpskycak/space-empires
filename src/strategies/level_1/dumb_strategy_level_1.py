import sys
sys.path.append('src')
import random
from strategies.basic_strategy import BasicStrategy

class DumbStrategyLevel1(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'DumbStrategyLevel1'

    def decide_purchases(self, hidden_game_state):
        return self.decide_ship_purchases(hidden_game_state)

    def decide_ship_purchases(self, hidden_game_state):
        return {'units': [{'type': 'Scout', 'coords': hidden_game_state['players'][self.player_index]['home_coords']}] * (hidden_game_state['players'][self.player_index]['cp'] // 6), 'technology': []}

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        grid_size = hidden_game_state['board_size'][0]
        unit_is_at_edge = (x_unit == grid_size-1)
        if unit_is_at_edge:
            return (0,0)
        else:
            return (1,0)
