import random
import sys
sys.path.append('src')
from strategies.basic_strategy import BasicStrategy


class DumbStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'DumbStrategy'

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return 'Scout'

    def decide_ship_movement(self, ship, game_state, movement_round):
        x, y = 0, 0
        if ship['coords'][0] < game_state['players'][self.player_index]['board_size']:
            x += ship['technology']['movement'][movement_round]
        return x, y
