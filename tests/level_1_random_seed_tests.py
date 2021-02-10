import sys
sys.path.append('src')
from strategies.level_1.berserker_strategy_level_1 import BerserkerStrategyLevel1
from strategies.level_1.random_strategy_level_1 import RandomStrategyLevel1
from strategies.level_1.dumb_strategy_level_1 import DumbStrategyLevel1
from strategies.level_1.colby_strategy_level_1 import ColbyStrategyLevel1
from strategies.level_1.flanker_strategy_level_1 import FlankerStrategyLevel1
from game import Game
from logger import Logger
import random
import math

strat_choices = [[BerserkerStrategyLevel1, FlankerStrategyLevel1], [FlankerStrategyLevel1, BerserkerStrategyLevel1]]
winner_for_first_half = []
winner_for_second_half = []

for seed_number in range(1,10):
    random.seed(seed_number)
    game = Game(strat_choices[0], (5,5), 'random', 4, max_turns = 4, print_state_obsolete=False, can_log=True)
    game.initialize_game()
    winner_for_first_half.append(game.play())

for seed_number in range(11,21):
    random.seed(seed_number)
    game = Game(strat_choices[1], (5,5), 'random', 4, max_turns = 4, print_state_obsolete=False, can_log=True)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won games', [index for index, player_index in enumerate(winner_for_first_half) if player_index == 0] + [index+5 for index, player_index in enumerate(winner_for_second_half) if player_index == 1], 'against Flanker!')