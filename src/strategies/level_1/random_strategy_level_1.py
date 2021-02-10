import sys
sys.path.append('src')
import random
from strategies.basic_strategy import BasicStrategy

class RandomStrategyLevel1(BasicStrategy):
    def __init__(self, player_index):
        self.player_index = player_index
        self.__name__ = 'RandomStrategyLevel1'

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        grid_size = hidden_game_state['board_size'][0]
        while True:
            translation = random.choice(translations)
            delta_x, delta_y = translation
            x_new = x_unit + delta_x
            y_new = y_unit + delta_y
            if 0 <= x_new and 0 <= y_new and x_new <= grid_size-1 and y_new <= grid_size-1:
                return translation
