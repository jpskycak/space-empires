import sys
sys.path.append('src')
from strategies.berserker_strategy_level_1 import BerserkerStrategyLevel1
from strategies.colby_strategy_level_1 import ColbyStrategyLevel1
from game import Game
from logger import Logger
import random

winner = []
strat_choices = [[ColbyStrategyLevel1, BerserkerStrategyLevel1], [BerserkerStrategyLevel1, ColbyStrategyLevel1]]
for _ in range(0,100):
    game = Game(random.choice(strat_choices), (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner.append(game.play())

print('\nColby Won', winner.count(0), 'percent of the time against Berserker Strategy!')